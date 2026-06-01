"""Self-contained game-like benchmark environments.

The environments are deliberately lightweight so that budgeted scheduler logic,
logging, strict/relaxed timing, and reproducibility can be tested without an
external game engine. Each environment exposes complete metadata required by the
manuscript revision.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Tuple, Any, Optional
import numpy as np


@dataclass
class EnvMetadata:
    environment_name: str
    environment_version: str
    benchmark_family: str
    task_name: str
    observation_definition: str
    observation_preprocessing: str
    action_definition: str
    action_space_type: str
    action_space_size: int
    reward_definition: str
    episode_termination: str
    opponent_policy: str
    stochasticity_sources: str
    max_steps: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BaseGameEnv:
    metadata: EnvMetadata
    obs_dim: int
    action_dim: int
    max_steps: int

    def reset(self, seed: Optional[int] = None) -> np.ndarray:
        raise NotImplementedError

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        raise NotImplementedError

    def clone(self, seed: Optional[int] = None) -> "BaseGameEnv":
        raise NotImplementedError


class LineDuelEnv(BaseGameEnv):
    """A one-dimensional real-time pursuit/target game.

    The agent must reach a target while avoiding an opponent that moves toward it.
    Actions: left, stay, right. Observations are normalized positions and distances.
    """

    obs_dim = 8
    action_dim = 3

    def __init__(self, length: int = 9, max_steps: int = 24, slip_prob: float = 0.05, seed: int = 0):
        self.length = int(length)
        self.max_steps = int(max_steps)
        self.slip_prob = float(slip_prob)
        self.rng = np.random.default_rng(seed)
        self.seed_value = seed
        self.metadata = EnvMetadata(
            environment_name="LineDuelEnv",
            environment_version="1.0-local",
            benchmark_family="self-contained-game-ai",
            task_name=f"line-duel-length-{length}",
            observation_definition="[agent_pos, target_pos, opponent_pos, normalized_step, dist_target, dist_opponent, bias, slip_prob]",
            observation_preprocessing="All positions and distances normalized to [0,1]; bias term included.",
            action_definition="0=left, 1=stay, 2=right",
            action_space_type="discrete",
            action_space_size=3,
            reward_definition="+1.0 for reaching target, -1.0 if caught, -0.01 per step, small shaping toward target.",
            episode_termination="Target reached, opponent catches agent, or max_steps reached.",
            opponent_policy="Greedy one-step move toward agent with stochastic slip/no-move probability.",
            stochasticity_sources="Initial positions and action slip controlled by seeded NumPy RNG.",
            max_steps=max_steps,
        )
        self.reset(seed)

    def clone(self, seed: Optional[int] = None) -> "LineDuelEnv":
        return LineDuelEnv(self.length, self.max_steps, self.slip_prob, self.seed_value if seed is None else seed)

    def reset(self, seed: Optional[int] = None) -> np.ndarray:
        if seed is not None:
            self.rng = np.random.default_rng(seed)
            self.seed_value = int(seed)
        self.agent = int(self.rng.integers(1, self.length - 1))
        self.target = int(self.rng.choice([0, self.length - 1]))
        self.opp = int(self.length - 1 - self.agent)
        if self.opp == self.agent:
            self.opp = 0
        self.t = 0
        return self._obs()

    def _obs(self) -> np.ndarray:
        L = max(1, self.length - 1)
        return np.array([
            self.agent / L,
            self.target / L,
            self.opp / L,
            self.t / max(1, self.max_steps),
            abs(self.target - self.agent) / L,
            abs(self.opp - self.agent) / L,
            1.0,
            self.slip_prob,
        ], dtype=np.float64)

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        self.t += 1
        action = int(action)
        if self.rng.random() < self.slip_prob:
            action = 1
        move = {0: -1, 1: 0, 2: 1}.get(action, 0)
        old_dist = abs(self.target - self.agent)
        self.agent = int(np.clip(self.agent + move, 0, self.length - 1))

        # Opponent moves greedily toward the agent, sometimes waits.
        if self.rng.random() > self.slip_prob:
            if self.opp < self.agent:
                self.opp += 1
            elif self.opp > self.agent:
                self.opp -= 1
        new_dist = abs(self.target - self.agent)
        reward = -0.01 + 0.02 * (old_dist - new_dist)
        done = False
        win = False
        if self.agent == self.target:
            reward += 1.0
            done = True
            win = True
        elif self.agent == self.opp:
            reward -= 1.0
            done = True
        elif self.t >= self.max_steps:
            done = True
        return self._obs(), float(reward), bool(done), {"win": win, "step": self.t}


class GridTreasureEnv(BaseGameEnv):
    """A small grid treasure-collection game with an adversarial chaser."""

    obs_dim = 10
    action_dim = 5

    def __init__(self, size: int = 5, max_steps: int = 32, hazard_prob: float = 0.08, seed: int = 0):
        self.size = int(size)
        self.max_steps = int(max_steps)
        self.hazard_prob = float(hazard_prob)
        self.rng = np.random.default_rng(seed)
        self.seed_value = seed
        self.metadata = EnvMetadata(
            environment_name="GridTreasureEnv",
            environment_version="1.0-local",
            benchmark_family="self-contained-game-ai",
            task_name=f"grid-treasure-size-{size}",
            observation_definition="[agent_xy, treasure_xy, chaser_xy, normalized_step, manhattan_treasure, manhattan_chaser, bias]",
            observation_preprocessing="Coordinates and distances normalized to [0,1]; bias term included.",
            action_definition="0=stay, 1=up, 2=down, 3=left, 4=right",
            action_space_type="discrete",
            action_space_size=5,
            reward_definition="+1.0 for treasure, -1.0 when caught, -0.01 per step, shaping toward treasure, random hazard penalty.",
            episode_termination="Treasure reached, chaser catches agent, or max_steps reached.",
            opponent_policy="Chaser greedily reduces Manhattan distance every other step with seeded randomness.",
            stochasticity_sources="Initial positions, hazard penalty, and chaser tie-breaking controlled by seeded NumPy RNG.",
            max_steps=max_steps,
        )
        self.reset(seed)

    def clone(self, seed: Optional[int] = None) -> "GridTreasureEnv":
        return GridTreasureEnv(self.size, self.max_steps, self.hazard_prob, self.seed_value if seed is None else seed)

    def reset(self, seed: Optional[int] = None) -> np.ndarray:
        if seed is not None:
            self.rng = np.random.default_rng(seed)
            self.seed_value = int(seed)
        cells = [(i, j) for i in range(self.size) for j in range(self.size)]
        idx = self.rng.choice(len(cells), size=3, replace=False)
        self.agent = list(cells[int(idx[0])])
        self.treasure = list(cells[int(idx[1])])
        self.chaser = list(cells[int(idx[2])])
        self.t = 0
        return self._obs()

    def _norm_xy(self, xy):
        denom = max(1, self.size - 1)
        return [xy[0] / denom, xy[1] / denom]

    def _manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _obs(self) -> np.ndarray:
        denom = max(1, 2 * (self.size - 1))
        return np.array(
            self._norm_xy(self.agent)
            + self._norm_xy(self.treasure)
            + self._norm_xy(self.chaser)
            + [
                self.t / max(1, self.max_steps),
                self._manhattan(self.agent, self.treasure) / denom,
                self._manhattan(self.agent, self.chaser) / denom,
                1.0,
            ],
            dtype=np.float64,
        )

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        self.t += 1
        moves = {0: (0, 0), 1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}
        old_dist = self._manhattan(self.agent, self.treasure)
        dx, dy = moves.get(int(action), (0, 0))
        self.agent[0] = int(np.clip(self.agent[0] + dx, 0, self.size - 1))
        self.agent[1] = int(np.clip(self.agent[1] + dy, 0, self.size - 1))

        if self.t % 2 == 0:
            options = []
            if self.chaser[0] < self.agent[0]:
                options.append((1, 0))
            elif self.chaser[0] > self.agent[0]:
                options.append((-1, 0))
            if self.chaser[1] < self.agent[1]:
                options.append((0, 1))
            elif self.chaser[1] > self.agent[1]:
                options.append((0, -1))
            if options:
                cdx, cdy = options[int(self.rng.integers(0, len(options)))]
                self.chaser[0] = int(np.clip(self.chaser[0] + cdx, 0, self.size - 1))
                self.chaser[1] = int(np.clip(self.chaser[1] + cdy, 0, self.size - 1))

        new_dist = self._manhattan(self.agent, self.treasure)
        reward = -0.01 + 0.03 * (old_dist - new_dist)
        if self.rng.random() < self.hazard_prob:
            reward -= 0.05
        done = False
        win = False
        if self.agent == self.treasure:
            reward += 1.0
            done = True
            win = True
        elif self.agent == self.chaser:
            reward -= 1.0
            done = True
        elif self.t >= self.max_steps:
            done = True
        return self._obs(), float(reward), bool(done), {"win": win, "step": self.t}



class ResourceDefenseEnv(BaseGameEnv):
    """A lightweight RTS-inspired resource-defense micro-domain.

    The agent manages workers, resources, base health, and enemy pressure under
    a short decision horizon. This task is included to diversify the local
    validation harness beyond pursuit and navigation: it stresses delayed
    rewards, resource allocation, and adversarial pressure.
    """

    obs_dim = 11
    action_dim = 5

    def __init__(self, max_steps: int = 36, wave_prob: float = 0.20, seed: int = 0):
        self.max_steps = int(max_steps)
        self.wave_prob = float(wave_prob)
        self.rng = np.random.default_rng(seed)
        self.seed_value = seed
        self.metadata = EnvMetadata(
            environment_name="ResourceDefenseEnv",
            environment_version="1.0-local",
            benchmark_family="self-contained-rts-micro",
            task_name="resource-defense-micro",
            observation_definition="[resources, workers, soldiers, base_health, enemy_pressure, normalized_step, last_wave, cooldown, stockpile_ratio, defense_ratio, bias]",
            observation_preprocessing="Counts and health normalized to fixed caps; bias term included.",
            action_definition="0=gather, 1=train_worker, 2=train_soldier, 3=attack_pressure, 4=repair_base",
            action_space_type="discrete",
            action_space_size=5,
            reward_definition="Incremental reward for survival, soldiers, and pressure reduction; penalties for base damage and defeat; terminal win bonus if base survives.",
            episode_termination="Base destroyed or max_steps reached.",
            opponent_policy="Seeded enemy pressure process with stochastic waves; pressure damages base unless countered by soldiers/attack actions.",
            stochasticity_sources="Initial stockpile, enemy wave arrivals, and wave magnitudes controlled by seeded NumPy RNG.",
            max_steps=max_steps,
        )
        self.reset(seed)

    def clone(self, seed: Optional[int] = None) -> "ResourceDefenseEnv":
        return ResourceDefenseEnv(self.max_steps, self.wave_prob, self.seed_value if seed is None else seed)

    def reset(self, seed: Optional[int] = None) -> np.ndarray:
        if seed is not None:
            self.rng = np.random.default_rng(seed)
            self.seed_value = int(seed)
        self.resources = float(self.rng.integers(2, 5))
        self.workers = float(2)
        self.soldiers = float(1)
        self.base_health = float(10)
        self.enemy_pressure = float(self.rng.integers(1, 4))
        self.cooldown = 0.0
        self.last_wave = 0.0
        self.t = 0
        return self._obs()

    def _obs(self) -> np.ndarray:
        return np.array([
            min(self.resources / 20.0, 1.0),
            min(self.workers / 10.0, 1.0),
            min(self.soldiers / 10.0, 1.0),
            self.base_health / 10.0,
            min(self.enemy_pressure / 12.0, 1.0),
            self.t / max(1, self.max_steps),
            min(self.last_wave / 6.0, 1.0),
            min(self.cooldown / 3.0, 1.0),
            min(self.resources / max(1.0, 2.0 + self.enemy_pressure), 1.0),
            min(self.soldiers / max(1.0, self.enemy_pressure), 1.0),
            1.0,
        ], dtype=np.float64)

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        self.t += 1
        action = int(action)
        reward = 0.01  # survival tick
        self.last_wave = 0.0

        # Economy production occurs before the chosen action, reflecting workers
        # gathering between decision intervals.
        self.resources += 0.35 * self.workers

        if action == 0:  # gather focus
            self.resources += 0.50 * self.workers
            reward += 0.01
        elif action == 1 and self.resources >= 3.0:  # train worker
            self.resources -= 3.0
            self.workers = min(10.0, self.workers + 1.0)
            reward += 0.025
        elif action == 2 and self.resources >= 4.0:  # train soldier
            self.resources -= 4.0
            self.soldiers = min(10.0, self.soldiers + 1.0)
            reward += 0.035
        elif action == 3:  # attack pressure
            reduction = min(self.enemy_pressure, 0.75 + 0.45 * self.soldiers)
            self.enemy_pressure -= reduction
            reward += 0.015 * reduction
            self.cooldown = 2.0
        elif action == 4 and self.resources >= 2.0:  # repair base
            self.resources -= 2.0
            before = self.base_health
            self.base_health = min(10.0, self.base_health + 1.5)
            reward += 0.02 * (self.base_health - before)

        # Enemy pressure process.
        wave_chance = self.wave_prob + 0.05 * (self.t / max(1, self.max_steps))
        if self.rng.random() < wave_chance:
            self.last_wave = float(self.rng.integers(1, 4))
            self.enemy_pressure += self.last_wave
        if self.cooldown > 0:
            self.cooldown -= 1.0

        defense = 0.22 * self.soldiers
        damage = max(0.0, self.enemy_pressure - defense) * 0.12
        self.base_health -= damage
        reward -= 0.03 * damage
        self.enemy_pressure = max(0.0, self.enemy_pressure - 0.04 * self.soldiers)

        done = False
        win = False
        if self.base_health <= 0.0:
            self.base_health = 0.0
            reward -= 1.0
            done = True
        elif self.t >= self.max_steps:
            win = self.base_health > 0.0
            reward += 1.0 if win else -1.0
            done = True

        reward += 0.002 * self.resources + 0.005 * self.soldiers - 0.002 * self.enemy_pressure
        return self._obs(), float(reward), bool(done), {"win": bool(win), "step": self.t}

def make_env(task: str, seed: int = 0) -> BaseGameEnv:
    if task == "line-duel":
        return LineDuelEnv(seed=seed)
    if task == "grid-treasure":
        return GridTreasureEnv(seed=seed)
    if task == "resource-defense":
        return ResourceDefenseEnv(seed=seed)
    if task == "gym-frozenlake-4x4":
        import gymnasium as gym
        from .external_adapters import GymnasiumDiscreteAdapter
        metadata = EnvMetadata(
            environment_name="Gymnasium/FrozenLake-v1",
            environment_version="1.3.0",
            benchmark_family="gymnasium-toy-text",
            task_name="FrozenLake-v1-4x4-slippery",
            observation_definition="Discrete grid state encoded as a 16-dimensional one-hot vector.",
            observation_preprocessing="Gymnasium discrete observation converted to one-hot vector; no additional feature engineering.",
            action_definition="Discrete, 4 actions: left, down, right, up.",
            action_space_type="discrete",
            action_space_size=4,
            reward_definition="+1.0 for reaching the goal, 0 otherwise; slippery transition dynamics enabled.",
            episode_termination="Goal reached, hole reached, or Gymnasium time-limit truncation.",
            opponent_policy="No opponent; environment transition model is stochastic because the slippery map changes intended motion.",
            stochasticity_sources="Gymnasium reset seed and slippery transition dynamics.",
            max_steps=100,
        )
        return GymnasiumDiscreteAdapter(lambda s: gym.make("FrozenLake-v1", is_slippery=True), metadata, seed)
    if task == "gym-frozenlake-4x4-deterministic":
        import gymnasium as gym
        from .external_adapters import GymnasiumDiscreteAdapter
        metadata = EnvMetadata(
            environment_name="Gymnasium/FrozenLake-v1",
            environment_version="1.3.0",
            benchmark_family="gymnasium-toy-text",
            task_name="FrozenLake-v1-4x4-deterministic",
            observation_definition="Discrete grid state encoded as a 16-dimensional one-hot vector.",
            observation_preprocessing="Gymnasium discrete observation converted to one-hot vector; no additional feature engineering.",
            action_definition="Discrete, 4 actions: left, down, right, up.",
            action_space_type="discrete",
            action_space_size=4,
            reward_definition="+1.0 for reaching the goal, 0 otherwise; deterministic transition dynamics.",
            episode_termination="Goal reached, hole reached, or Gymnasium time-limit truncation.",
            opponent_policy="No opponent; deterministic grid transition dynamics.",
            stochasticity_sources="Gymnasium reset seed controls initial RNG state; transition dynamics are deterministic.",
            max_steps=100,
        )
        return GymnasiumDiscreteAdapter(lambda s: gym.make("FrozenLake-v1", is_slippery=False), metadata, seed)
    if task == "gym-cliffwalking":
        import gymnasium as gym
        from .external_adapters import GymnasiumDiscreteAdapter
        metadata = EnvMetadata(
            environment_name="Gymnasium/CliffWalking-v1",
            environment_version="1.3.0",
            benchmark_family="gymnasium-toy-text",
            task_name="CliffWalking-v1",
            observation_definition="Discrete grid state encoded as a 48-dimensional one-hot vector.",
            observation_preprocessing="Gymnasium discrete observation converted to one-hot vector; no additional feature engineering.",
            action_definition="Discrete, 4 actions: up, right, down, left.",
            action_space_type="discrete",
            action_space_size=4,
            reward_definition="-1 per step and -100 for stepping into the cliff; episode ends at the goal.",
            episode_termination="Goal reached or Gymnasium time-limit truncation.",
            opponent_policy="No opponent; deterministic grid transition dynamics.",
            stochasticity_sources="Gymnasium reset seed; transition dynamics are deterministic.",
            max_steps=200,
        )
        return GymnasiumDiscreteAdapter(lambda s: gym.make("CliffWalking-v1"), metadata, seed)
    if task == "gym-blackjack":
        import gymnasium as gym
        from .external_adapters import GymnasiumDiscreteAdapter
        metadata = EnvMetadata(
            environment_name="Gymnasium/Blackjack-v1",
            environment_version="1.3.0",
            benchmark_family="gymnasium-toy-text-card",
            task_name="Blackjack-v1",
            observation_definition="Tuple observation [player_sum, dealer_showing_card, usable_ace] represented as a normalized numeric vector.",
            observation_preprocessing="Tuple fields flattened to a three-dimensional numeric vector and normalized by the largest absolute field value.",
            action_definition="Discrete, 2 actions: stick or hit.",
            action_space_type="discrete",
            action_space_size=2,
            reward_definition="+1 for win, 0 for draw, -1 for loss under the Gymnasium Blackjack rules.",
            episode_termination="Player sticks or goes bust; dealer then resolves the hand according to the built-in policy.",
            opponent_policy="Built-in dealer policy: draw until reaching 17, then stick.",
            stochasticity_sources="Gymnasium reset seed controls card draws and initial hands.",
            max_steps=100,
        )
        return GymnasiumDiscreteAdapter(lambda s: gym.make("Blackjack-v1", natural=False, sab=False), metadata, seed)
    if task == "minigrid-empty-5x5":
        import gymnasium as gym
        import minigrid  # noqa: F401 - importing registers MiniGrid environments
        from .external_adapters import GymnasiumDiscreteAdapter
        metadata = EnvMetadata(
            environment_name="MiniGrid/MiniGrid-Empty-5x5-v0",
            environment_version="3.1.0",
            benchmark_family="minigrid",
            task_name="MiniGrid-Empty-5x5-v0",
            observation_definition="Partial-observation MiniGrid dictionary with 7x7x3 symbolic image and agent direction.",
            observation_preprocessing="Image and direction fields flattened and normalized; mission string omitted from the numeric policy input.",
            action_definition="Discrete, 7 MiniGrid actions: left, right, forward, pickup, drop, toggle, done.",
            action_space_type="discrete",
            action_space_size=7,
            reward_definition="MiniGrid sparse goal reward with built-in time penalty; zero for non-goal transitions.",
            episode_termination="Goal reached or MiniGrid time-limit truncation.",
            opponent_policy="No opponent; partial observability and randomized start/goal placement define task variation.",
            stochasticity_sources="MiniGrid reset seed controls layout/start orientation and any environment randomization.",
            max_steps=100,
        )
        return GymnasiumDiscreteAdapter(lambda s: gym.make("MiniGrid-Empty-5x5-v0"), metadata, seed)
    if task == "minigrid-empty-5x5-fullyobs":
        import gymnasium as gym
        import minigrid  # noqa: F401 - importing registers MiniGrid environments
        from minigrid.wrappers import FullyObsWrapper
        from .external_adapters import GymnasiumDiscreteAdapter, minigrid_fully_observable_goal_features
        metadata = EnvMetadata(
            environment_name="MiniGrid/MiniGrid-Empty-5x5-v0/FullyObsWrapper",
            environment_version="3.1.0",
            benchmark_family="minigrid",
            task_name="MiniGrid-Empty-5x5-v0-fullyobs-goal-features",
            observation_definition="[agent_xy, goal_xy, relative_goal_xy, direction_onehot, bias] extracted from the FullyObsWrapper symbolic grid.",
            observation_preprocessing="MiniGrid FullyObsWrapper exposes the compact symbolic full grid. The adapter extracts normalized agent and goal coordinates, normalized relative coordinates, a four-value direction one-hot vector, and a bias term.",
            action_definition="Adapter-restricted discrete action set: 0=left, 1=right, 2=forward. MiniGrid Empty's unused pickup, drop, toggle, and done actions are intentionally omitted.",
            action_space_type="discrete",
            action_space_size=3,
            reward_definition="MiniGrid sparse goal reward with built-in time penalty; zero for non-goal transitions.",
            episode_termination="Goal reached or MiniGrid time-limit truncation.",
            opponent_policy="No opponent; the regular Empty-5x5 task places the agent in the corner opposite the goal.",
            stochasticity_sources="MiniGrid reset seed controls environment RNG state. The regular Empty-5x5 task uses a fixed room layout; the disclosed adapter retains the seeded reset schedule.",
            max_steps=100,
        )
        return GymnasiumDiscreteAdapter(
            lambda s: FullyObsWrapper(gym.make("MiniGrid-Empty-5x5-v0")),
            metadata,
            seed,
            obs_formatter=minigrid_fully_observable_goal_features,
            action_map=(0, 1, 2),
        )
    raise ValueError(f"Unknown task: {task}")
