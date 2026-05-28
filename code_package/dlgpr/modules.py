"""GA, PSO, and RL atomic update modules."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
import time
import numpy as np

from .envs import BaseGameEnv
from .policies import LinearSoftmaxPolicy, repair_theta
from .evaluation import evaluate_theta, run_episode


@dataclass
class AtomicResult:
    module: str
    theta: np.ndarray
    value: float
    score: float
    win_rate: float
    charged_ms: float
    cpu_ms: float
    learning_progress: float = 0.0
    diversity: float = 0.0
    improvement_rate: float = 0.0
    note: str = ""


class BaseModule:
    name: str

    def atomic_step(self, best_value: float) -> AtomicResult:
        raise NotImplementedError

    def best_theta(self) -> np.ndarray:
        raise NotImplementedError

    def diversity(self) -> float:
        return 0.0


def charged_duration_ms(rng: np.random.Generator, delta_min: float, delta_max: float, module_bias: float = 1.0) -> float:
    raw = rng.uniform(delta_min, delta_max) * module_bias
    return float(np.clip(raw, delta_min, delta_max))


class GAModule(BaseModule):
    name = "GA"

    def __init__(self, policy: LinearSoftmaxPolicy, env_factory: Callable[[int], BaseGameEnv], rng: np.random.Generator,
                 eval_seeds: List[int], horizon: int, delta_min_ms: float, delta_max_ms: float,
                 population_size: int = 10, mutation_sigma: float = 0.25):
        self.policy = policy
        self.env_factory = env_factory
        self.rng = rng
        self.eval_seeds = eval_seeds
        self.horizon = horizon
        self.delta_min_ms = delta_min_ms
        self.delta_max_ms = delta_max_ms
        self.population_size = population_size
        self.mutation_sigma = mutation_sigma
        self.population = [repair_theta(rng.normal(0, 0.5, policy.param_dim)) for _ in range(population_size)]
        self.fitness = np.full(population_size, -np.inf, dtype=np.float64)
        for i in range(population_size):
            self.fitness[i] = evaluate_theta(env_factory, policy, self.population[i], eval_seeds[:1], horizon)["return"]

    def best_theta(self) -> np.ndarray:
        return self.population[int(np.argmax(self.fitness))].copy()

    def _tournament(self) -> np.ndarray:
        idx = self.rng.choice(self.population_size, size=3, replace=False)
        return self.population[int(idx[np.argmax(self.fitness[idx])])]

    def diversity(self) -> float:
        desc = [self.policy.behavioral_descriptor(p) for p in self.population]
        if len(desc) < 2:
            return 0.0
        total = 0.0
        count = 0
        for i in range(len(desc)):
            for j in range(i + 1, len(desc)):
                total += float(np.linalg.norm(desc[i] - desc[j]))
                count += 1
        return total / max(1, count)

    def inject_candidate(self, theta: np.ndarray, always: bool = False) -> Dict[str, float]:
        """Inject an externally generated candidate into the GA population.

        This implements the RL-to-population handoff used by the full DLGPR
        configuration. The candidate is evaluated with the same short evaluation
        operator as normal GA children and replaces the current worst individual
        when it improves on that individual, or when ``always`` is requested.
        """
        cand = repair_theta(theta)
        metrics = evaluate_theta(self.env_factory, self.policy, cand, self.eval_seeds[:2], self.horizon)
        worst = int(np.argmin(self.fitness))
        replaced = bool(always or metrics["return"] > self.fitness[worst])
        if replaced:
            self.population[worst] = cand.copy()
            self.fitness[worst] = metrics["return"]
        return {"return": float(metrics["return"]), "replaced": float(replaced)}

    def atomic_step(self, best_value: float) -> AtomicResult:
        t0 = time.perf_counter()
        p1 = self._tournament()
        p2 = self._tournament()
        alpha = self.rng.uniform(0.25, 0.75)
        child = alpha * p1 + (1 - alpha) * p2
        child += self.rng.normal(0, self.mutation_sigma, self.policy.param_dim)
        child = repair_theta(child)
        metrics = evaluate_theta(self.env_factory, self.policy, child, self.eval_seeds[:2], self.horizon)
        worst = int(np.argmin(self.fitness))
        if metrics["return"] > self.fitness[worst]:
            self.population[worst] = child
            self.fitness[worst] = metrics["return"]
        cpu_ms = (time.perf_counter() - t0) * 1000.0
        charged = charged_duration_ms(self.rng, self.delta_min_ms, self.delta_max_ms, module_bias=1.0)
        gain = max(0.0, metrics["return"] - best_value)
        return AtomicResult("GA", child, metrics["return"], metrics["score"], metrics["win_rate"], charged, cpu_ms,
                            diversity=self.diversity(), improvement_rate=gain / max(charged, 1e-9))


class PSOModule(BaseModule):
    name = "PSO"

    def __init__(self, policy: LinearSoftmaxPolicy, env_factory: Callable[[int], BaseGameEnv], rng: np.random.Generator,
                 eval_seeds: List[int], horizon: int, delta_min_ms: float, delta_max_ms: float,
                 swarm_size: int = 8):
        self.policy = policy
        self.env_factory = env_factory
        self.rng = rng
        self.eval_seeds = eval_seeds
        self.horizon = horizon
        self.delta_min_ms = delta_min_ms
        self.delta_max_ms = delta_max_ms
        self.swarm_size = swarm_size
        self.positions = [repair_theta(rng.normal(0, 0.5, policy.param_dim)) for _ in range(swarm_size)]
        self.velocities = [rng.normal(0, 0.1, policy.param_dim) for _ in range(swarm_size)]
        self.pbest = [p.copy() for p in self.positions]
        self.pbest_value = np.array([evaluate_theta(env_factory, policy, p, eval_seeds[:1], horizon)["return"] for p in self.positions])
        self.cursor = 0

    def best_theta(self) -> np.ndarray:
        return self.pbest[int(np.argmax(self.pbest_value))].copy()

    def inject_candidate(self, theta: np.ndarray, always: bool = False) -> Dict[str, float]:
        """Inject a candidate into the PSO elite memory.

        This keeps the scheduler-baseline and full-DLGPR comparisons honest by
        making cross-layer handoff an actual executable operation rather than a
        paper-only description.
        """
        cand = repair_theta(theta)
        metrics = evaluate_theta(self.env_factory, self.policy, cand, self.eval_seeds[:2], self.horizon)
        worst = int(np.argmin(self.pbest_value))
        replaced = bool(always or metrics["return"] > self.pbest_value[worst])
        if replaced:
            self.positions[worst] = cand.copy()
            self.pbest[worst] = cand.copy()
            self.pbest_value[worst] = metrics["return"]
        return {"return": float(metrics["return"]), "replaced": float(replaced)}

    def atomic_step(self, best_value: float) -> AtomicResult:
        t0 = time.perf_counter()
        i = self.cursor % self.swarm_size
        self.cursor += 1
        gbest = self.best_theta()
        r1 = self.rng.random(self.policy.param_dim)
        r2 = self.rng.random(self.policy.param_dim)
        inertia, c1, c2 = 0.55, 1.2, 1.2
        self.velocities[i] = inertia * self.velocities[i] + c1 * r1 * (self.pbest[i] - self.positions[i]) + c2 * r2 * (gbest - self.positions[i])
        self.positions[i] = repair_theta(self.positions[i] + self.velocities[i])
        metrics = evaluate_theta(self.env_factory, self.policy, self.positions[i], self.eval_seeds[:2], self.horizon)
        if metrics["return"] > self.pbest_value[i]:
            self.pbest[i] = self.positions[i].copy()
            self.pbest_value[i] = metrics["return"]
        cpu_ms = (time.perf_counter() - t0) * 1000.0
        charged = charged_duration_ms(self.rng, self.delta_min_ms, self.delta_max_ms, module_bias=0.9)
        gain = max(0.0, metrics["return"] - best_value)
        return AtomicResult("PSO", self.positions[i].copy(), metrics["return"], metrics["score"], metrics["win_rate"], charged, cpu_ms,
                            improvement_rate=gain / max(charged, 1e-9))


class RLModule(BaseModule):
    name = "RL"

    def __init__(self, policy: LinearSoftmaxPolicy, env_factory: Callable[[int], BaseGameEnv], rng: np.random.Generator,
                 train_seeds: List[int], eval_seeds: List[int], horizon: int, delta_min_ms: float, delta_max_ms: float,
                 lr: float = 0.05):
        self.policy = policy
        self.env_factory = env_factory
        self.rng = rng
        self.train_seeds = train_seeds
        self.eval_seeds = eval_seeds
        self.horizon = horizon
        self.delta_min_ms = delta_min_ms
        self.delta_max_ms = delta_max_ms
        self.lr = lr
        self.theta = repair_theta(rng.normal(0, 0.3, policy.param_dim))
        self.cursor = 0
        self.last_loss = 0.0

    def best_theta(self) -> np.ndarray:
        return self.theta.copy()

    def distill_toward(self, teacher_theta: np.ndarray, alpha: float = 0.04) -> float:
        """Move the RL parameter vector toward a population/swarm teacher.

        The lightweight harness uses a linear policy, so behavioral distillation
        can be represented as a conservative parameter-space interpolation.
        The returned value is a nonnegative progress proxy based on distance
        reduction to the teacher. External benchmark integrations can replace
        this with behavior-cloning updates over an elite replay buffer.
        """
        teacher = repair_theta(teacher_theta)
        before = float(np.linalg.norm(self.theta - teacher))
        self.theta = repair_theta((1.0 - alpha) * self.theta + alpha * teacher)
        after = float(np.linalg.norm(self.theta - teacher))
        return max(0.0, before - after)

    def atomic_step(self, best_value: float) -> AtomicResult:
        t0 = time.perf_counter()
        seed = self.train_seeds[self.cursor % len(self.train_seeds)]
        self.cursor += 1
        env = self.env_factory(seed)
        obs = env.reset(seed)
        traj = []
        total = 0.0
        for _ in range(self.horizon):
            probs = self.policy.probs(self.theta, obs)
            act = int(self.rng.choice(self.policy.action_dim, p=probs))
            next_obs, reward, done, _info = env.step(act)
            traj.append((obs.copy(), act, probs.copy(), float(reward)))
            total += float(reward)
            obs = next_obs
            if done:
                break
        # REINFORCE-style update with return-to-go.
        G = 0.0
        grad = np.zeros((self.policy.obs_dim, self.policy.action_dim), dtype=np.float64)
        gamma = 0.97
        for obs_i, act_i, probs_i, reward_i in reversed(traj):
            G = reward_i + gamma * G
            onehot = np.zeros(self.policy.action_dim)
            onehot[act_i] = 1.0
            grad += np.outer(obs_i, onehot - probs_i) * G
        if traj:
            grad /= max(1, len(traj))
        old_loss = self.last_loss
        self.theta = repair_theta(self.theta + self.lr * grad.reshape(-1))
        self.last_loss = -float(total)
        lp = max(0.0, old_loss - self.last_loss)
        metrics = evaluate_theta(self.env_factory, self.policy, self.theta, self.eval_seeds[:2], self.horizon)
        cpu_ms = (time.perf_counter() - t0) * 1000.0
        charged = charged_duration_ms(self.rng, self.delta_min_ms, self.delta_max_ms, module_bias=1.1)
        gain = max(0.0, metrics["return"] - best_value)
        return AtomicResult("RL", self.theta.copy(), metrics["return"], metrics["score"], metrics["win_rate"], charged, cpu_ms,
                            learning_progress=lp / max(charged, 1e-9), improvement_rate=gain / max(charged, 1e-9))
