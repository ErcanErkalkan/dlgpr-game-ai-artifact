"""Evaluation helpers with fixed seed schedules."""
from __future__ import annotations

from typing import Callable, Dict, List, Tuple
import numpy as np
from .policies import LinearSoftmaxPolicy
from .envs import BaseGameEnv


def run_episode(env: BaseGameEnv, policy: LinearSoftmaxPolicy, theta: np.ndarray, seed: int, horizon: int, deterministic: bool = True) -> Dict[str, float]:
    rng = np.random.default_rng(seed + 991)
    obs = env.reset(seed)
    total = 0.0
    win = 0
    steps = 0
    for step in range(horizon):
        action = policy.act(theta, obs, rng, deterministic=deterministic)
        obs, reward, done, info = env.step(action)
        total += float(reward)
        steps = step + 1
        if done:
            win = int(bool(info.get("win", False)))
            break
    return {"return": total, "score": total, "win": win, "steps": steps}


def evaluate_theta(env_factory: Callable[[int], BaseGameEnv], policy: LinearSoftmaxPolicy, theta: np.ndarray, eval_seeds: List[int], horizon: int, deterministic: bool = True) -> Dict[str, float]:
    rows = []
    for seed in eval_seeds:
        env = env_factory(seed)
        rows.append(run_episode(env, policy, theta, seed, horizon, deterministic))
    returns = np.array([r["return"] for r in rows], dtype=np.float64)
    scores = np.array([r["score"] for r in rows], dtype=np.float64)
    wins = np.array([r["win"] for r in rows], dtype=np.float64)
    steps = np.array([r["steps"] for r in rows], dtype=np.float64)
    return {
        "return": float(np.mean(returns)),
        "score": float(np.mean(scores)),
        "win_rate": float(np.mean(wins)),
        "mean_steps": float(np.mean(steps)),
    }


def estimate_steps_to_threshold(history_scores: List[float], threshold: float, step_cap_per_interval: int) -> int:
    for i, score in enumerate(history_scores):
        if score >= threshold:
            return int((i + 1) * step_cap_per_interval)
    return -1
