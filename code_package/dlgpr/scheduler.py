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

    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
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

    def update_timing(self, module: str, charged_ms: float, cpu_ms: float) -> None:
        return None

    def required_budget(self, module: str, delta_min_ms: float, delta_max_ms: float) -> float:
        return float(delta_max_ms)

    def threshold_snapshot(self, delta_min_ms: float, delta_max_ms: float) -> Dict[str, float]:
        return {m: self.required_budget(m, delta_min_ms, delta_max_ms) for m in self.modules}


class DLGPRScheduler(BaseScheduler):
    def __init__(self, modules: Sequence[str], rng: np.random.Generator,
                 w_improvement: float = 1.0, w_diversity: float = 0.25, w_learning: float = 0.25,
                 w_ucb: float = 0.15, n_min: int = 1, ema_lambda: float = 0.75):
        super().__init__(modules, rng, n_min=n_min, ema_lambda=ema_lambda)
        self.w_improvement = float(w_improvement)
        self.w_diversity = float(w_diversity)
        self.w_learning = float(w_learning)
        self.w_ucb = float(w_ucb)

    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
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

    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
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

    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
        m = self.pattern[self.cursor % len(self.pattern)]
        self.cursor += 1
        return m


class GreedyImprovementScheduler(BaseScheduler):
    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
        # Use EMA improvement only; if all equal at start, deterministic fallback.
        return max(self.modules, key=lambda m: (self.state.ema_improvement.get(m, 0.0), -self.modules.index(m)))


class RiskAwareDLGPRScheduler(DLGPRScheduler):
    """DLGPR with learned module-specific do-not-start thresholds.

    The scheduler keeps the strict global atomic-step cap as a hard upper bound,
    but learns a conservative per-module duration requirement from observed
    charged durations. This reduces wasted budget when some modules are
    consistently shorter than the worst-case delta_max contract.
    """

    def __init__(
        self,
        modules: Sequence[str],
        rng: np.random.Generator,
        w_improvement: float = 1.0,
        w_diversity: float = 0.25,
        w_learning: float = 0.25,
        w_ucb: float = 0.15,
        n_min: int = 1,
        ema_lambda: float = 0.75,
        risk_quantile: float = 0.75,
        risk_margin: float = 0.10,
        latency_weight: float = 0.08,
        min_samples: int = 3,
    ):
        super().__init__(
            modules,
            rng,
            w_improvement=w_improvement,
            w_diversity=w_diversity,
            w_learning=w_learning,
            w_ucb=w_ucb,
            n_min=n_min,
            ema_lambda=ema_lambda,
        )
        self.risk_quantile = float(risk_quantile)
        self.risk_margin = float(risk_margin)
        self.latency_weight = float(latency_weight)
        self.min_samples = int(min_samples)
        self.duration_samples: Dict[str, List[float]] = {m: [] for m in self.modules}

    def update_timing(self, module: str, charged_ms: float, cpu_ms: float) -> None:
        samples = self.duration_samples.setdefault(module, [])
        samples.append(float(max(0.0, charged_ms)))
        if len(samples) > 128:
            del samples[:-128]

    def required_budget(self, module: str, delta_min_ms: float, delta_max_ms: float) -> float:
        samples = np.asarray(self.duration_samples.get(module, []), dtype=np.float64)
        if samples.size < self.min_samples:
            return float(delta_max_ms)
        q = float(np.quantile(samples, self.risk_quantile))
        std = float(np.std(samples, ddof=1)) if samples.size > 1 else 0.0
        required = q + self.risk_margin * std
        return float(np.clip(required, delta_min_ms, delta_max_ms))

    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
        feasible = list(self.modules)
        if remaining_ms is not None:
            feasible = [
                m for m in self.modules
                if self.required_budget(m, 1.0, float("inf")) <= remaining_ms
            ]
            if not feasible:
                return self.modules[0]
        if self.n_min > 0:
            missing = [m for m in feasible if interval_counts.get(m, 0) < self.n_min]
            if missing:
                return sorted(missing)[0]
        idx = self.index_values()
        return max(feasible, key=lambda m: (idx[m], -self.modules.index(m)))

    def index_values(self) -> Dict[str, float]:
        base = super().index_values()
        out = {}
        for m, val in base.items():
            samples = self.duration_samples.get(m, [])
            if samples:
                mean_duration = float(np.mean(samples))
                out[m] = float(val / max(mean_duration, 1e-9) - self.latency_weight * mean_duration)
            else:
                out[m] = float(val)
        return out


class RacingScheduler(DLGPRScheduler):
    """Probe each module, then commit the interval to the best recent utility."""

    def __init__(self, modules: Sequence[str], rng: np.random.Generator,
                 commit_weight: float = 1.35, n_min: int = 1, ema_lambda: float = 0.75):
        super().__init__(
            modules,
            rng,
            w_improvement=commit_weight,
            w_diversity=0.15,
            w_learning=0.15,
            w_ucb=0.02,
            n_min=n_min,
            ema_lambda=ema_lambda,
        )

    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
        if self.n_min > 0:
            missing = [m for m in self.modules if interval_counts.get(m, 0) < self.n_min]
            if missing:
                return sorted(missing)[0]
        idx = self.index_values()
        return max(self.modules, key=lambda m: (idx[m], -self.modules.index(m)))


class ThompsonScheduler(DLGPRScheduler):
    """Discounted Thompson-style portfolio scheduler for nonstationary modules."""

    def __init__(self, modules: Sequence[str], rng: np.random.Generator,
                 n_min: int = 1, ema_lambda: float = 0.75, discount: float = 0.97):
        super().__init__(
            modules,
            rng,
            w_improvement=1.0,
            w_diversity=0.20,
            w_learning=0.20,
            w_ucb=0.0,
            n_min=n_min,
            ema_lambda=ema_lambda,
        )
        self.discount = float(discount)
        self.alpha = {m: 1.0 for m in self.modules}
        self.beta = {m: 1.0 for m in self.modules}

    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
        if self.n_min > 0:
            missing = [m for m in self.modules if interval_counts.get(m, 0) < self.n_min]
            if missing:
                return sorted(missing)[0]
        samples = {}
        idx = super().index_values()
        for m in self.modules:
            draw = float(self.rng.beta(self.alpha[m], self.beta[m]))
            samples[m] = draw * (1.0 + max(0.0, idx[m]))
        return max(self.modules, key=lambda m: (samples[m], -self.modules.index(m)))

    def update(self, module: str, improvement_rate: float, diversity: float, learning_progress: float) -> None:
        super().update(module, improvement_rate, diversity, learning_progress)
        for m in self.modules:
            self.alpha[m] *= self.discount
            self.beta[m] *= self.discount
        if improvement_rate > 1e-12:
            self.alpha[module] += 1.0 + min(4.0, float(improvement_rate))
        else:
            self.beta[module] += 1.0


class RiskAwareRacingScheduler(RiskAwareDLGPRScheduler):
    """Risk-aware thresholds with probe-then-commit interval allocation."""

    def __init__(self, modules: Sequence[str], rng: np.random.Generator,
                 n_min: int = 1, ema_lambda: float = 0.75):
        super().__init__(
            modules,
            rng,
            w_improvement=1.35,
            w_diversity=0.15,
            w_learning=0.15,
            w_ucb=0.02,
            n_min=n_min,
            ema_lambda=ema_lambda,
            risk_quantile=0.75,
            risk_margin=0.10,
            latency_weight=0.04,
        )


class WindowedDLGPRScheduler(DLGPRScheduler):
    """DLGPR with global windowed non-starvation instead of per-interval probes."""

    def __init__(
        self,
        modules: Sequence[str],
        rng: np.random.Generator,
        w_improvement: float = 1.0,
        w_diversity: float = 0.15,
        w_learning: float = 0.15,
        w_ucb: float = 0.08,
        n_min: int = 0,
        ema_lambda: float = 0.75,
        max_gap: int = 12,
    ):
        super().__init__(
            modules,
            rng,
            w_improvement=w_improvement,
            w_diversity=w_diversity,
            w_learning=w_learning,
            w_ucb=w_ucb,
            n_min=n_min,
            ema_lambda=ema_lambda,
        )
        self.max_gap = int(max_gap)
        self.gaps = {m: self.max_gap for m in self.modules}

    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
        never_selected = [m for m in self.modules if self.state.selection_counts.get(m, 0) == 0]
        if never_selected:
            return sorted(never_selected)[0]
        overdue = [m for m in self.modules if self.gaps.get(m, 0) >= self.max_gap]
        if overdue:
            return max(overdue, key=lambda m: (self.gaps.get(m, 0), -self.modules.index(m)))
        idx = self.index_values()
        return max(self.modules, key=lambda m: (idx[m], -self.modules.index(m)))

    def update(self, module: str, improvement_rate: float, diversity: float, learning_progress: float) -> None:
        super().update(module, improvement_rate, diversity, learning_progress)
        for m in self.modules:
            if m == module:
                self.gaps[m] = 0
            else:
                self.gaps[m] = self.gaps.get(m, 0) + 1


class SAGEDLGPRScheduler(DLGPRScheduler):
    """Selective Adaptive Gated Exploration for the GA-PSO-RL portfolio.

    SAGE replaces per-interval mandatory probing with event-triggered probing:
    every module is cold-started once, exploitation then follows the DLGPR
    utility index, and additional probes are triggered only after improvement
    plateaus or long starvation gaps. This keeps the strict delta_max contract
    while avoiding the systematic budget tax of probing all modules at every
    planning interval.
    """

    def __init__(
        self,
        modules: Sequence[str],
        rng: np.random.Generator,
        w_improvement: float = 1.15,
        w_diversity: float = 0.10,
        w_learning: float = 0.10,
        w_ucb: float = 0.0,
        n_min: int = 0,
        ema_lambda: float = 0.75,
        plateau_probe_gap: int = 12,
        starvation_gap: int = 12,
    ):
        super().__init__(
            modules,
            rng,
            w_improvement=w_improvement,
            w_diversity=w_diversity,
            w_learning=w_learning,
            w_ucb=w_ucb,
            n_min=n_min,
            ema_lambda=ema_lambda,
        )
        self.plateau_probe_gap = int(plateau_probe_gap)
        self.starvation_gap = int(starvation_gap)
        self.gaps = {m: self.starvation_gap for m in self.modules}
        self.plateau_steps = 0

    def select(self, interval_counts: Dict[str, int], remaining_ms: float | None = None) -> str:
        never_selected = [m for m in self.modules if self.state.selection_counts.get(m, 0) == 0]
        if never_selected:
            return sorted(never_selected)[0]

        idx = self.index_values()
        best_exploit = max(self.modules, key=lambda m: (idx[m], -self.modules.index(m)))
        overdue = [m for m in self.modules if self.gaps.get(m, 0) >= self.starvation_gap]
        if overdue:
            return max(overdue, key=lambda m: (self.gaps.get(m, 0), idx[m], -self.modules.index(m)))
        if self.plateau_steps >= self.plateau_probe_gap:
            alternatives = [m for m in self.modules if m != best_exploit]
            if alternatives:
                return max(alternatives, key=lambda m: (self.gaps.get(m, 0), idx[m], -self.modules.index(m)))
        return best_exploit

    def update(self, module: str, improvement_rate: float, diversity: float, learning_progress: float) -> None:
        super().update(module, improvement_rate, diversity, learning_progress)
        if improvement_rate > 1e-12:
            self.plateau_steps = 0
        else:
            self.plateau_steps += 1
        for m in self.modules:
            if m == module:
                self.gaps[m] = 0
            else:
                self.gaps[m] = self.gaps.get(m, 0) + 1
