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

    def __init__(self, env_factory: Callable[[int], Any], metadata: EnvMetadata, seed: int = 0):
        self.env_factory = env_factory
        self.metadata = metadata
        self.seed_value = seed
        self.env = env_factory(seed)
        # Infer dimensions conservatively.
        obs, _info = self._reset_raw(seed)
        self.obs_dim = int(np.asarray(obs, dtype=np.float64).size)
        self.action_dim = int(getattr(getattr(self.env, "action_space", None), "n"))
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
        return np.asarray(obs, dtype=np.float64).reshape(-1)

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        out = self.env.step(int(action))
        if len(out) == 5:
            obs, reward, terminated, truncated, info = out
            done = bool(terminated or truncated)
        else:
            obs, reward, done, info = out
        info = dict(info or {})
        info.setdefault("win", bool(reward > 0 and done))
        return np.asarray(obs, dtype=np.float64).reshape(-1), float(reward), bool(done), info

    def clone(self, seed: Optional[int] = None) -> "GymnasiumDiscreteAdapter":
        return GymnasiumDiscreteAdapter(self.env_factory, self.metadata, self.seed_value if seed is None else seed)


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
