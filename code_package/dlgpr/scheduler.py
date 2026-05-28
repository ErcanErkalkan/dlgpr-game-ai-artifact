"""Schedulers for allocating atomic steps under a per-interval budget."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence
import math
import numpy as np


@dataclass
class SchedulerState:
    ema_improvement: Dict[str, float] = field(default_factory=dict)
    ema_learning: float = 0.0
    diversity: float = 0.0
    selection_counts: Dict[str, int] = field(default_factory=dict)
    total_selections: int = 0

    def ensure(self, modules: Sequence[str]) -> None:
        for m in modules:
            self.ema_improvement.setdefault(m, 0.0)
            self.selection_counts.setdefault(m, 0)


class BaseScheduler:
    def __init__(self, modules: Sequence[str], rng: np.random.Generator, n_min: int = 1, ema_lambda: float = 0.75):
        self.modules = list(modules)
        self.rng = rng
        self.n_min = int(n_min)
        self.ema_lambda = float(ema_lambda)
        self.state = SchedulerState()
        self.state.ensure(self.modules)

    def select(self, interval_counts: Dict[str, int]) -> str:
        raise NotImplementedError

    def update(self, module: str, improvement_rate: float, diversity: float, learning_progress: float) -> None:
        self.state.ensure(self.modules)
        lam = self.ema_lambda
        self.state.ema_improvement[module] = lam * self.state.ema_improvement[module] + (1 - lam) * float(improvement_rate)
        self.state.diversity = lam * self.state.diversity + (1 - lam) * float(diversity)
        self.state.ema_learning = lam * self.state.ema_learning + (1 - lam) * float(learning_progress)
        self.state.selection_counts[module] += 1
        self.state.total_selections += 1

    def index_values(self) -> Dict[str, float]:
        return {m: 0.0 for m in self.modules}


class DLGPRScheduler(BaseScheduler):
    def __init__(self, modules: Sequence[str], rng: np.random.Generator,
                 w_improvement: float = 1.0, w_diversity: float = 0.25, w_learning: float = 0.25,
                 w_ucb: float = 0.15, n_min: int = 1, ema_lambda: float = 0.75):
        super().__init__(modules, rng, n_min=n_min, ema_lambda=ema_lambda)
        self.w_improvement = float(w_improvement)
        self.w_diversity = float(w_diversity)
        self.w_learning = float(w_learning)
        self.w_ucb = float(w_ucb)

    def select(self, interval_counts: Dict[str, int]) -> str:
        if self.n_min > 0:
            missing = [m for m in self.modules if interval_counts.get(m, 0) < self.n_min]
            if missing:
                return sorted(missing)[0]
        idx = self.index_values()
        return max(self.modules, key=lambda m: (idx[m], -self.modules.index(m)))

    def index_values(self) -> Dict[str, float]:
        out = {}
        total = max(1, self.state.total_selections)
        for m in self.modules:
            ucb = math.sqrt(math.log(1 + total) / (1 + self.state.selection_counts.get(m, 0)))
            val = self.w_improvement * self.state.ema_improvement.get(m, 0.0)
            if m == "GA":
                val += self.w_diversity * self.state.diversity
            if m == "RL":
                val += self.w_learning * self.state.ema_learning
            val += self.w_ucb * ucb
            out[m] = float(val)
        return out


class RoundRobinScheduler(BaseScheduler):
    def __init__(self, modules: Sequence[str], rng: np.random.Generator, n_min: int = 0, ema_lambda: float = 0.75):
        super().__init__(modules, rng, n_min=n_min, ema_lambda=ema_lambda)
        self.cursor = 0

    def select(self, interval_counts: Dict[str, int]) -> str:
        m = self.modules[self.cursor % len(self.modules)]
        self.cursor += 1
        return m


class FixedSplitScheduler(BaseScheduler):
    def __init__(self, modules: Sequence[str], rng: np.random.Generator, pattern: Sequence[str] = ("GA", "PSO", "RL"), ema_lambda: float = 0.75):
        super().__init__(modules, rng, n_min=0, ema_lambda=ema_lambda)
        self.pattern = [m for m in pattern if m in modules]
        if not self.pattern:
            self.pattern = list(modules)
        self.cursor = 0

    def select(self, interval_counts: Dict[str, int]) -> str:
        m = self.pattern[self.cursor % len(self.pattern)]
        self.cursor += 1
        return m


class GreedyImprovementScheduler(BaseScheduler):
    def select(self, interval_counts: Dict[str, int]) -> str:
        # Use EMA improvement only; if all equal at start, deterministic fallback.
        return max(self.modules, key=lambda m: (self.state.ema_improvement.get(m, 0.0), -self.modules.index(m)))
