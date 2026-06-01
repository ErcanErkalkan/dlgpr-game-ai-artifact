"""Optional external benchmark adapter interfaces.

The local package is self-contained, but journal-grade evidence should be run on
recognized Game AI benchmarks. This module provides a thin adapter contract so
GVGAI, MicroRTS, Procgen, Gymnasium, or other environments can be integrated
without changing the scheduler/evaluation code.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable, Dict, Optional, Protocol, Tuple
import numpy as np

from .envs import BaseGameEnv, EnvMetadata


class ExternalEnvLike(Protocol):
    """Minimal interface expected from an external environment wrapper."""

    obs_dim: int
    action_dim: int
    metadata: EnvMetadata

    def reset(self, seed: Optional[int] = None) -> np.ndarray: ...

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]: ...

    def clone(self, seed: Optional[int] = None) -> "ExternalEnvLike": ...


@dataclass
class AdapterChecklist:
    environment_name: str
    environment_version: str
    task_name: str
    observation_defined: bool
    action_defined: bool
    reward_defined: bool
    termination_defined: bool
    opponent_defined: bool
    stochasticity_defined: bool
    evaluation_cadence_defined: bool

    def complete(self) -> bool:
        return all(v for k, v in asdict(self).items() if isinstance(v, bool))


class GymnasiumDiscreteAdapter(BaseGameEnv):
    """Adapter for optional Gymnasium-style discrete-action environments.

    This class is intentionally dependency-light: pass an already constructed
    factory, e.g. ``lambda seed: gym.make('CartPole-v1')``. It assumes the
    environment returns vector observations and has a discrete action space.
    The adapter is not used by the local smoke tests because external packages
    may not be installed in every review environment.
    """

    def __init__(
        self,
        env_factory: Callable[[int], Any],
        metadata: EnvMetadata,
        seed: int = 0,
        obs_formatter: Optional[Callable[[Any], np.ndarray]] = None,
        action_map: Optional[Tuple[int, ...]] = None,
    ):
        self.env_factory = env_factory
        self.metadata = metadata
        self.seed_value = seed
        self.obs_formatter = obs_formatter
        self.action_map = tuple(action_map) if action_map is not None else None
        self.env = env_factory(seed)
        obs_space = getattr(self.env, "observation_space", None)
        self._discrete_obs_n = getattr(obs_space, "n", None)
        obs, _info = self._reset_raw(seed)
        self.obs_dim = int(self._format_obs(obs).size)
        self.action_dim = len(self.action_map) if self.action_map is not None else int(getattr(getattr(self.env, "action_space", None), "n"))
        self.max_steps = metadata.max_steps

    def _reset_raw(self, seed: Optional[int] = None):
        out = self.env.reset(seed=seed) if seed is not None else self.env.reset()
        if isinstance(out, tuple) and len(out) == 2:
            return out
        return out, {}

    def reset(self, seed: Optional[int] = None) -> np.ndarray:
        if seed is not None:
            self.seed_value = int(seed)
        obs, _info = self._reset_raw(seed)
        return self._format_obs(obs)

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        raw_action = self.action_map[int(action)] if self.action_map is not None else int(action)
        out = self.env.step(raw_action)
        if len(out) == 5:
            obs, reward, terminated, truncated, info = out
            done = bool(terminated or truncated)
        else:
            obs, reward, done, info = out
        info = dict(info or {})
        if "win" not in info:
            info["win"] = bool(done and reward > 0)
        return self._format_obs(obs), float(reward), bool(done), info

    def _format_obs(self, obs: Any) -> np.ndarray:
        if self.obs_formatter is not None:
            return np.asarray(self.obs_formatter(obs), dtype=np.float64).reshape(-1)
        if self._discrete_obs_n is not None:
            out = np.zeros(int(self._discrete_obs_n), dtype=np.float64)
            out[int(obs)] = 1.0
            return out
        if isinstance(obs, dict):
            parts = []
            for key in sorted(obs.keys()):
                value = obs[key]
                if isinstance(value, str):
                    continue
                arr = np.asarray(value, dtype=np.float64).reshape(-1)
                if arr.size and np.max(np.abs(arr)) > 1.0:
                    arr = arr / max(float(np.max(np.abs(arr))), 1.0)
                parts.append(arr)
            if not parts:
                return np.zeros(1, dtype=np.float64)
            return np.concatenate(parts).astype(np.float64)
        arr = np.asarray(obs, dtype=np.float64).reshape(-1)
        if arr.size and np.max(np.abs(arr)) > 1.0:
            arr = arr / max(float(np.max(np.abs(arr))), 1.0)
        return arr

    def clone(self, seed: Optional[int] = None) -> "GymnasiumDiscreteAdapter":
        return GymnasiumDiscreteAdapter(
            self.env_factory,
            self.metadata,
            self.seed_value if seed is None else seed,
            obs_formatter=self.obs_formatter,
            action_map=self.action_map,
        )


def minigrid_fully_observable_goal_features(obs: Any) -> np.ndarray:
    """Extract a compact, disclosed MiniGrid Empty-task feature vector.

    The FullyObsWrapper image encodes the agent and goal cells explicitly. This
    helper keeps the controller lightweight while avoiding an uninformative raw
    flattening of the symbolic grid for the MiniGrid Empty performance run.
    """
    from minigrid.core.constants import OBJECT_TO_IDX

    image = np.asarray(obs["image"])
    objects = image[..., 0]
    agent = np.argwhere(objects == OBJECT_TO_IDX["agent"])
    goal = np.argwhere(objects == OBJECT_TO_IDX["goal"])
    if agent.size == 0:
        raise ValueError("Fully observable MiniGrid observation must contain the agent cell")
    agent_xy = agent[0].astype(np.float64)
    # At successful termination the agent occupies and replaces the encoded
    # goal cell in the compact grid representation.
    goal_xy = (goal[0] if goal.size else agent[0]).astype(np.float64)
    scale = np.maximum(np.asarray(objects.shape, dtype=np.float64) - 1.0, 1.0)
    direction = int(obs.get("direction", 0))
    direction_onehot = np.zeros(4, dtype=np.float64)
    direction_onehot[direction % 4] = 1.0
    delta = (goal_xy - agent_xy) / scale
    return np.concatenate([agent_xy / scale, goal_xy / scale, delta, direction_onehot, [1.0]])


def validate_adapter_metadata(metadata: EnvMetadata, evaluation_cadence_defined: bool = True) -> AdapterChecklist:
    """Return a reviewer-facing completeness checklist for an adapter."""
    return AdapterChecklist(
        environment_name=metadata.environment_name,
        environment_version=metadata.environment_version,
        task_name=metadata.task_name,
        observation_defined=bool(metadata.observation_definition),
        action_defined=bool(metadata.action_definition),
        reward_defined=bool(metadata.reward_definition),
        termination_defined=bool(metadata.episode_termination),
        opponent_defined=bool(metadata.opponent_policy),
        stochasticity_defined=bool(metadata.stochasticity_sources),
        evaluation_cadence_defined=bool(evaluation_cadence_defined),
    )
