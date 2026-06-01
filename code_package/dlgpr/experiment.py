"""Matched-budget experiment runner."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Callable, Tuple, Any
import csv
import json
import time
import platform
import os
import subprocess
from importlib import metadata as importlib_metadata

import numpy as np

from .envs import make_env, BaseGameEnv
from .policies import LinearSoftmaxPolicy
from .evaluation import evaluate_theta, estimate_steps_to_threshold
from .modules import GAModule, CEMGAModule, PSOModule, RLModule, AtomicResult
from .scheduler import (
    DLGPRScheduler,
    RoundRobinScheduler,
    FixedSplitScheduler,
    GreedyImprovementScheduler,
    RiskAwareDLGPRScheduler,
    RacingScheduler,
    ThompsonScheduler,
    RiskAwareRacingScheduler,
    WindowedDLGPRScheduler,
    SAGEDLGPRScheduler,
    BaseScheduler,
)


@dataclass
class ExperimentConfig:
    tasks: List[str]
    seeds: List[int]
    intervals: int = 20
    B_tau_ms: float = 24.0
    guard_margin_ms: float = 2.0
    delta_min_ms: float = 1.0
    delta_max_ms: float = 4.0
    horizon: int = 24
    eval_rollouts_K: int = 3
    train_seed_offset: int = 10000
    eval_seed_offset: int = 20000
    step_cap_per_interval: int = 32
    threshold_T: float = 0.50
    deterministic_eval: bool = True
    timing_mode: str = "simulated_charged"  # simulated_charged, rollout_normalized, actual_cpu_clipped, or actual_cpu_raw
    rollout_charge_ms: float = 1.0
    scheduler_ema_lambda: float = 0.75

    @property
    def allowed_ms(self) -> float:
        return self.B_tau_ms - self.guard_margin_ms


METHODS = [
    "robust-DLGPR",
    "robust-near-elite-DLGPR",
    "DLGPR-full",
    "GA-only",
    "PSO-only",
    "RL-only",
    "fixed-split",
    "round-robin",
    "greedy-improvement",
    "no-diversity",
    "no-learning-progress",
    "no-ucb",
    "no-non-starvation",
    "no-handshake",
    "strict-delta-max",
    "relaxed-delta-min",
]


INTERVAL_FIELDS = [
    "run_id", "git_commit", "timestamp", "seed", "method", "benchmark", "environment_name", "environment_version", "task_name", "interval",
    "B_tau_ms", "allowed_ms", "guard_margin_ms", "delta_min_ms", "delta_max_ms", "do_not_start_rule", "scheduler_ema_lambda",
    "loop_time_ms", "e2e_time_ms", "actual_cpu_loop_wall_ms", "actual_cpu_e2e_ms", "wall_clock_interval_ms",
    "total_atomic_cpu_ms", "actual_cpu_loop_overrun", "actual_cpu_e2e_overrun", "actual_cpu_e2e_overrun_ms",
    "timing_mode", "budget_unit", "rollout_charge_ms", "selected_module", "atomic_step_duration_ms",
    "total_rollout_equivalents", "last_step_rollout_equivalents",
    "num_ga_steps", "num_pso_steps", "num_rl_steps", "candidate_count", "evaluated_candidate_count",
    "score", "return", "win", "threshold_T", "steps_to_threshold", "evaluation_cadence",
    "atomic_eval_rollouts",
    "p95_latency_ms", "p99_latency_ms", "max_latency_ms", "loop_overrun", "e2e_overrun", "loop_overrun_ms", "e2e_overrun_ms",
    "diversity_value", "diversity_descriptor_valid", "learning_progress_value", "improvement_rate_value", "handshake_enabled", "handshake_events",
    "scheduler_index_ga", "scheduler_index_pso", "scheduler_index_rl", "rng_train_seed", "rng_eval_seed", "hardware_id", "notes",
    "required_budget_ga_ms", "required_budget_pso_ms", "required_budget_rl_ms", "selected_required_budget_ms", "budget_utilization", "meta_mode",
]

ATOMIC_FIELDS = [
    "run_id", "seed", "method", "task_name", "interval", "atomic_index", "module", "charged_ms", "cpu_ms", "value", "score", "win_rate",
    "improvement_rate", "diversity", "learning_progress", "evaluation_rollouts", "training_rollouts",
    "handoff_evaluation_rollouts", "rollout_equivalents", "remaining_before_ms", "remaining_after_ms",
    "do_not_start_rule", "handshake_events", "note",
]


def git_commit() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=Path.cwd(), stderr=subprocess.DEVNULL, text=True).strip()
        return out
    except Exception:
        return "no-git"


def hardware_id() -> str:
    return f"{platform.system()}-{platform.machine()}-py{platform.python_version()}"


def library_versions() -> Dict[str, str]:
    versions: Dict[str, str] = {}
    for package in ["numpy", "pandas", "matplotlib", "scipy", "gymnasium", "minigrid"]:
        try:
            versions[package] = importlib_metadata.version(package)
        except importlib_metadata.PackageNotFoundError:
            versions[package] = "not-installed"
    return versions


def make_factory(task: str) -> Callable[[int], BaseGameEnv]:
    return lambda seed: make_env(task, seed=seed)


def method_components(method: str) -> Tuple[List[str], str, Dict[str, float], int]:
    """Return active modules, scheduler kind, weights, n_min."""
    if method == "GA-only":
        return ["GA"], "round-robin", {}, 0
    if method == "PSO-only":
        return ["PSO"], "round-robin", {}, 0
    if method == "RL-only":
        return ["RL"], "round-robin", {}, 0
    if method == "fixed-split":
        return ["GA", "PSO", "RL"], "fixed-split", {}, 0
    if method == "round-robin":
        return ["GA", "PSO", "RL"], "round-robin", {}, 0
    if method == "greedy-improvement":
        return ["GA", "PSO", "RL"], "greedy", {}, 0
    if method == "RAPID-DLGPR":
        return ["GA", "PSO", "RL"], "risk-aware", {}, 1
    if method == "racing-DLGPR":
        return ["GA", "PSO", "RL"], "racing", {}, 1
    if method == "thompson-DLGPR":
        return ["GA", "PSO", "RL"], "thompson", {}, 1
    if method == "RAPID-racing-DLGPR":
        return ["GA", "PSO", "RL"], "risk-racing", {}, 1
    if method == "windowed-DLGPR":
        return ["GA", "PSO", "RL"], "windowed", {}, 0
    if method == "SAGE-DLGPR":
        return ["GA", "PSO", "RL"], "sage", {}, 0
    if method == "SAGE-fastprobe-DLGPR":
        return ["GA", "PSO", "RL"], "sage", {"plateau_probe_gap": 8, "starvation_gap": 8}, 0
    if method == "gated-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 0
    if method == "lean-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.1, "w_diversity": 0.0, "w_learning": 0.10, "w_ucb": 0.08}, 0
    if method == "adaptive-gated-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 0
    if method == "transfer-adaptive-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 0
    if method == "near-elite-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 0
    if method == "CEM-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.20, "w_learning": 0.20, "w_ucb": 0.12}, 1
    if method == "near-elite-CEM-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.20, "w_learning": 0.20, "w_ucb": 0.12}, 0
    if method == "meta-gated-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 1
    if method == "robust-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 1
    if method == "robust-near-elite-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 0
    if method == "robust-no-non-starvation":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 0
    if method == "robust-no-handshake":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 1
    if method == "robust-near-full-DLGPR":
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 1
    if method in ("near-elite-tight-DLGPR", "near-elite-wide-DLGPR"):
        return ["GA", "PSO", "RL"], "dlgpr", {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}, 0
    weights = {"w_improvement": 1.0, "w_diversity": 0.25, "w_learning": 0.25, "w_ucb": 0.15}
    n_min = 1
    if method == "no-diversity":
        weights["w_diversity"] = 0.0
    if method == "no-learning-progress":
        weights["w_learning"] = 0.0
    if method == "no-ucb":
        weights["w_ucb"] = 0.0
    if method == "no-non-starvation":
        n_min = 0
    return ["GA", "PSO", "RL"], "dlgpr", weights, n_min


def build_scheduler(kind: str, modules: List[str], rng: np.random.Generator, weights: Dict[str, float], n_min: int, ema_lambda: float) -> BaseScheduler:
    if kind == "fixed-split":
        return FixedSplitScheduler(modules, rng, ema_lambda=ema_lambda)
    if kind == "round-robin":
        return RoundRobinScheduler(modules, rng, ema_lambda=ema_lambda)
    if kind == "greedy":
        return GreedyImprovementScheduler(modules, rng, ema_lambda=ema_lambda)
    if kind == "risk-aware":
        return RiskAwareDLGPRScheduler(modules, rng, n_min=n_min, ema_lambda=ema_lambda, **weights)
    if kind == "racing":
        return RacingScheduler(modules, rng, n_min=n_min, ema_lambda=ema_lambda)
    if kind == "thompson":
        return ThompsonScheduler(modules, rng, n_min=n_min, ema_lambda=ema_lambda)
    if kind == "risk-racing":
        return RiskAwareRacingScheduler(modules, rng, n_min=n_min, ema_lambda=ema_lambda)
    if kind == "windowed":
        return WindowedDLGPRScheduler(modules, rng, n_min=n_min, ema_lambda=ema_lambda)
    if kind == "sage":
        return SAGEDLGPRScheduler(modules, rng, n_min=n_min, ema_lambda=ema_lambda, **weights)
    return DLGPRScheduler(modules, rng, n_min=n_min, ema_lambda=ema_lambda, **weights)


def build_modules(active_modules: List[str], policy: LinearSoftmaxPolicy, env_factory: Callable[[int], BaseGameEnv], rng: np.random.Generator,
                  train_seeds: List[int], eval_seeds: List[int], cfg: ExperimentConfig, ga_variant: str = "ga",
                  atomic_eval_rollouts: int = 2) -> Dict[str, Any]:
    mods: Dict[str, Any] = {}
    if "GA" in active_modules:
        ga_cls = CEMGAModule if ga_variant == "cem" else GAModule
        mods["GA"] = ga_cls(policy, env_factory, rng, eval_seeds, cfg.horizon, cfg.delta_min_ms, cfg.delta_max_ms,
                            atomic_eval_rollouts=atomic_eval_rollouts)
    if "PSO" in active_modules:
        mods["PSO"] = PSOModule(policy, env_factory, rng, eval_seeds, cfg.horizon, cfg.delta_min_ms, cfg.delta_max_ms,
                                atomic_eval_rollouts=atomic_eval_rollouts)
    if "RL" in active_modules:
        mods["RL"] = RLModule(policy, env_factory, rng, train_seeds, eval_seeds, cfg.horizon, cfg.delta_min_ms, cfg.delta_max_ms,
                              atomic_eval_rollouts=atomic_eval_rollouts)
    return mods


def run_one(cfg: ExperimentConfig, method: str, task: str, seed: int, output_dir: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    rng = np.random.default_rng(seed + 12345)
    env_factory = make_factory(task)
    env0 = env_factory(seed)
    policy = LinearSoftmaxPolicy(env0.obs_dim, env0.action_dim)
    active_modules, sched_kind, weights, n_min = method_components(method)
    scheduler = build_scheduler(sched_kind, active_modules, rng, weights, n_min, cfg.scheduler_ema_lambda)
    train_seeds = [cfg.train_seed_offset + seed * 1000 + i for i in range(max(10, cfg.intervals * 2))]
    eval_seeds = [cfg.eval_seed_offset + seed * 1000 + i for i in range(max(cfg.eval_rollouts_K, 3))]
    ga_variant = "cem" if method in ("CEM-DLGPR", "near-elite-CEM-DLGPR") else "ga"
    atomic_eval_rollouts = cfg.eval_rollouts_K if method in ("robust-DLGPR", "robust-near-elite-DLGPR", "robust-no-non-starvation", "robust-no-handshake", "robust-near-full-DLGPR") else 2
    mods = build_modules(active_modules, policy, env_factory, rng, train_seeds, eval_seeds, cfg,
                         ga_variant=ga_variant, atomic_eval_rollouts=atomic_eval_rollouts)
    handshake_enabled = bool(set(["GA", "PSO", "RL"]).issubset(set(active_modules)) and method not in ("no-handshake", "robust-no-handshake"))
    selective_handoff = method in ("RAPID-DLGPR", "racing-DLGPR", "thompson-DLGPR", "RAPID-racing-DLGPR", "windowed-DLGPR", "SAGE-DLGPR", "SAGE-fastprobe-DLGPR", "gated-DLGPR", "lean-DLGPR", "adaptive-gated-DLGPR", "transfer-adaptive-DLGPR", "near-elite-DLGPR", "near-elite-tight-DLGPR", "near-elite-wide-DLGPR", "near-elite-CEM-DLGPR", "meta-gated-DLGPR", "robust-near-elite-DLGPR", "robust-near-full-DLGPR")
    adaptive_handoff = method == "adaptive-gated-DLGPR"
    transfer_adaptive_handoff = method == "transfer-adaptive-DLGPR"
    near_elite_margin = 0.05
    if method == "near-elite-tight-DLGPR":
        near_elite_margin = 0.02
    if method == "near-elite-wide-DLGPR":
        near_elite_margin = 0.10
    near_elite_handoff = method in ("near-elite-DLGPR", "near-elite-tight-DLGPR", "near-elite-wide-DLGPR", "near-elite-CEM-DLGPR", "robust-near-elite-DLGPR", "robust-near-full-DLGPR")

    adaptive_threshold = method in ("RAPID-DLGPR", "RAPID-racing-DLGPR")
    if cfg.timing_mode == "rollout_normalized":
        rule = "strict_rollout_equivalent_max"
        threshold = cfg.delta_max_ms
    elif adaptive_threshold:
        rule = "risk_adaptive_module_threshold"
        threshold = cfg.delta_max_ms
    elif method in ("strict-delta-max", "DLGPR-full", "no-diversity", "no-learning-progress", "no-ucb", "no-non-starvation", "no-handshake", "racing-DLGPR", "thompson-DLGPR", "windowed-DLGPR", "SAGE-DLGPR", "SAGE-fastprobe-DLGPR", "gated-DLGPR", "lean-DLGPR", "adaptive-gated-DLGPR", "transfer-adaptive-DLGPR", "near-elite-DLGPR", "near-elite-tight-DLGPR", "near-elite-wide-DLGPR", "CEM-DLGPR", "near-elite-CEM-DLGPR", "meta-gated-DLGPR", "robust-DLGPR", "robust-near-elite-DLGPR", "robust-no-non-starvation", "robust-no-handshake", "robust-near-full-DLGPR"):
        rule = "strict_delta_max"
        threshold = cfg.delta_max_ms
    elif method == "relaxed-delta-min":
        rule = "relaxed_delta_min"
        threshold = cfg.delta_min_ms
    else:
        rule = "strict_delta_max"
        threshold = cfg.delta_max_ms

    run_id = f"{task}_{method}_seed{seed}"
    best_theta = list(mods.values())[0].best_theta()
    best_eval = evaluate_theta(env_factory, policy, best_theta, eval_seeds[:cfg.eval_rollouts_K], cfg.horizon, cfg.deterministic_eval)
    best_value = best_eval["return"]
    score_history: List[float] = []
    interval_logs: List[Dict[str, Any]] = []
    atomic_logs: List[Dict[str, Any]] = []
    e2e_history: List[float] = []
    handoff_success_ema = 0.0
    meta_modes = ["full", "gated", "no_handshake", "no_non_starvation"]
    meta_scores: Dict[str, List[float]] = {m: [] for m in meta_modes}
    meta_committed_mode: str | None = None
    meta_warmup_intervals = 12
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    commit = git_commit()
    hw = hardware_id()

    for interval in range(cfg.intervals):
        if method == "meta-gated-DLGPR":
            if meta_committed_mode is None:
                current_meta_mode = meta_modes[interval % len(meta_modes)]
            else:
                current_meta_mode = meta_committed_mode
            scheduler.n_min = 1 if current_meta_mode == "full" else 0
        else:
            current_meta_mode = "fixed"
        interval_wall_start = time.perf_counter()
        remaining = cfg.allowed_ms
        loop_time = 0.0
        interval_counts = {"GA": 0, "PSO": 0, "RL": 0}
        candidates = []
        selected_module = "none"
        last_atomic_ms = 0.0
        last_div = 0.0
        last_lp = 0.0
        last_imp = 0.0
        atomic_idx = 0
        interval_handshake_events = 0
        total_rollout_equivalents = 0
        last_step_rollout_equivalents = 0
        total_atomic_cpu_ms = 0.0
        actual_loop_wall_start = time.perf_counter()
        selected_required_budget_ms = 0.0

        def module_rollout_equivalent_max(module_name: str) -> int:
            module = mods[module_name]
            cost = int(getattr(module, "atomic_eval_rollouts", 0))
            if module_name == "RL":
                cost += 1
                if handshake_enabled:
                    for target in ("GA", "PSO"):
                        if target in mods:
                            cost += int(getattr(mods[target], "atomic_eval_rollouts", 0))
            return cost

        def module_required_budget(module_name: str) -> float:
            if cfg.timing_mode == "rollout_normalized":
                return float(module_rollout_equivalent_max(module_name) * cfg.rollout_charge_ms)
            if adaptive_threshold:
                return scheduler.required_budget(module_name, cfg.delta_min_ms, cfg.delta_max_ms)
            return float(threshold)

        def feasible_modules() -> List[str]:
            return [m for m in active_modules if module_required_budget(m) <= remaining]

        while feasible_modules() and atomic_idx < cfg.step_cap_per_interval:
            selected_module = scheduler.select(interval_counts, remaining)
            if selected_module not in mods:
                break
            if module_required_budget(selected_module) > remaining:
                idx_now = scheduler.index_values()
                feasible = feasible_modules()
                if not feasible:
                    break
                selected_module = max(feasible, key=lambda m: (idx_now.get(m, 0.0), -active_modules.index(m)))
            selected_required_budget_ms = module_required_budget(selected_module)
            before = remaining
            atomic_wall_start = time.perf_counter()
            result: AtomicResult = mods[selected_module].atomic_step(best_value)

            step_handshake_events = 0
            step_handoff_evaluation_rollouts = 0
            effective_handshake_enabled = handshake_enabled
            effective_selective_handoff = selective_handoff
            effective_near_elite_handoff = near_elite_handoff
            if method == "meta-gated-DLGPR":
                effective_handshake_enabled = handshake_enabled and current_meta_mode != "no_handshake"
                effective_selective_handoff = current_meta_mode == "gated"
                effective_near_elite_handoff = current_meta_mode == "gated"

            positive_module_signal = scheduler.state.ema_improvement.get(selected_module, 0.0) > 1e-9
            positive_transfer_signal = handoff_success_ema >= 0.35
            allow_handoff = (
                (not effective_selective_handoff)
                or result.value > best_value
                or (adaptive_handoff and positive_module_signal)
                or (transfer_adaptive_handoff and positive_transfer_signal)
                or (effective_near_elite_handoff and result.value >= best_value - near_elite_margin)
            )
            if effective_handshake_enabled and allow_handoff:
                handoff_success = 0.0
                handoff_attempts = 0
                if selected_module == "RL":
                    if "GA" in mods and hasattr(mods["GA"], "inject_candidate"):
                        info = mods["GA"].inject_candidate(result.theta)
                        handoff_success += float(info.get("replaced", 0.0))
                        step_handoff_evaluation_rollouts += int(info.get("evaluation_rollouts", 0.0))
                        handoff_attempts += 1
                        step_handshake_events += 1
                    if "PSO" in mods and hasattr(mods["PSO"], "inject_candidate"):
                        info = mods["PSO"].inject_candidate(result.theta)
                        handoff_success += float(info.get("replaced", 0.0))
                        step_handoff_evaluation_rollouts += int(info.get("evaluation_rollouts", 0.0))
                        handoff_attempts += 1
                        step_handshake_events += 1
                elif selected_module in ("GA", "PSO") and "RL" in mods and hasattr(mods["RL"], "distill_toward"):
                    lp_extra = mods["RL"].distill_toward(result.theta)
                    result.learning_progress += lp_extra / max(result.charged_ms, 1e-9)
                    handoff_success += float(lp_extra > 1e-12)
                    handoff_attempts += 1
                    step_handshake_events += 1
                if handoff_attempts:
                    observed_success = handoff_success / max(1, handoff_attempts)
                    handoff_success_ema = 0.80 * handoff_success_ema + 0.20 * observed_success
                if step_handshake_events:
                    result.note = "cross_layer_handoff_executed"
            elif transfer_adaptive_handoff:
                handoff_success_ema *= 0.98

            # Timing convention: by default the harness uses a disclosed simulated
            # charged duration to stress the budget scheduler deterministically.
            # The measured CPU duration is still logged separately. Profiling
            # runs can charge the full selected step, including cross-layer
            # handoff, either after clipping to the declared atomic-step contract
            # or directly as raw CPU duration. Rollout-normalized runs instead
            # charge every evaluation and training rollout as one declared
            # rollout-equivalent unit, including RL-to-population injection.
            full_step_cpu_ms = (time.perf_counter() - atomic_wall_start) * 1000.0
            result.cpu_ms = full_step_cpu_ms
            module_reported_charge_ms = result.charged_ms
            step_rollout_equivalents = int(result.evaluation_rollouts + result.training_rollouts + step_handoff_evaluation_rollouts)
            if cfg.timing_mode == "actual_cpu_clipped":
                result.charged_ms = float(np.clip(full_step_cpu_ms, cfg.delta_min_ms, cfg.delta_max_ms))
            elif cfg.timing_mode == "actual_cpu_raw":
                result.charged_ms = float(full_step_cpu_ms)
            elif cfg.timing_mode == "rollout_normalized":
                result.charged_ms = float(step_rollout_equivalents * cfg.rollout_charge_ms)
            result.learning_progress *= module_reported_charge_ms / max(result.charged_ms, 1e-9)
            result.improvement_rate = max(0.0, result.value - best_value) / max(result.charged_ms, 1e-9)

            after = remaining - result.charged_ms
            remaining = after
            loop_time += result.charged_ms
            total_atomic_cpu_ms += result.cpu_ms
            interval_counts[selected_module] = interval_counts.get(selected_module, 0) + 1
            interval_handshake_events += step_handshake_events
            total_rollout_equivalents += step_rollout_equivalents
            candidates.append(result)
            scheduler.update(selected_module, result.improvement_rate, result.diversity, result.learning_progress)
            scheduler.update_timing(selected_module, result.charged_ms, result.cpu_ms)
            if result.value > best_value:
                best_value = result.value
                best_theta = result.theta.copy()
            last_atomic_ms = result.charged_ms
            last_step_rollout_equivalents = step_rollout_equivalents
            last_div = result.diversity
            last_lp = result.learning_progress
            last_imp = result.improvement_rate
            atomic_logs.append({
                "run_id": run_id, "seed": seed, "method": method, "task_name": task, "interval": interval,
                "atomic_index": atomic_idx, "module": result.module, "charged_ms": result.charged_ms, "cpu_ms": result.cpu_ms,
                "value": result.value, "score": result.score, "win_rate": result.win_rate, "improvement_rate": result.improvement_rate,
                "diversity": result.diversity, "learning_progress": result.learning_progress,
                "evaluation_rollouts": result.evaluation_rollouts, "training_rollouts": result.training_rollouts,
                "handoff_evaluation_rollouts": step_handoff_evaluation_rollouts,
                "rollout_equivalents": step_rollout_equivalents,
                "remaining_before_ms": before, "remaining_after_ms": after, "do_not_start_rule": rule,
                "handshake_events": step_handshake_events, "note": result.note,
            })
            atomic_idx += 1
            # relaxed variant may overrun after a final too-large atomic step; stop once negative.
            if remaining < 0:
                break

        actual_cpu_loop_wall_ms = (time.perf_counter() - actual_loop_wall_start) * 1000.0
        eval_metrics = evaluate_theta(env_factory, policy, best_theta, eval_seeds[:cfg.eval_rollouts_K], cfg.horizon, cfg.deterministic_eval)
        if method == "meta-gated-DLGPR":
            meta_scores[current_meta_mode].append(float(eval_metrics["return"]))
            if meta_committed_mode is None and interval + 1 >= meta_warmup_intervals and all(meta_scores[m] for m in meta_modes):
                meta_committed_mode = max(meta_modes, key=lambda m: (float(np.mean(meta_scores[m])), -meta_modes.index(m)))
        score_history.append(eval_metrics["score"])
        steps_to_T = estimate_steps_to_threshold(score_history, cfg.threshold_T, cfg.step_cap_per_interval)
        _actual_cpu_e2e_ms = actual_cpu_loop_wall_ms + cfg.guard_margin_ms
        wall_clock_interval_ms = (time.perf_counter() - interval_wall_start) * 1000.0
        # The manuscript timing contract is evaluated on charged loop time plus
        # reserved guard margin. CPU time is still retained in atomic_step_logs.csv
        # for profiling, but the budget-compliance columns intentionally use the
        # disclosed charged-time convention.
        e2e_ms = loop_time + cfg.guard_margin_ms
        e2e_history.append(e2e_ms)
        idx = scheduler.index_values()
        if cfg.timing_mode == "rollout_normalized":
            required = {m: module_required_budget(m) for m in active_modules}
        else:
            required = scheduler.threshold_snapshot(cfg.delta_min_ms, cfg.delta_max_ms)
        budget_unit = "rollout-equivalent unit" if cfg.timing_mode == "rollout_normalized" else "ms"
        interval_logs.append({
            "run_id": run_id, "git_commit": commit, "timestamp": timestamp, "seed": seed, "method": method,
            "benchmark": env0.metadata.benchmark_family, "environment_name": env0.metadata.environment_name,
            "environment_version": env0.metadata.environment_version, "task_name": task, "interval": interval,
            "B_tau_ms": cfg.B_tau_ms, "allowed_ms": cfg.allowed_ms, "guard_margin_ms": cfg.guard_margin_ms,
            "delta_min_ms": cfg.delta_min_ms, "delta_max_ms": cfg.delta_max_ms, "do_not_start_rule": rule,
            "scheduler_ema_lambda": cfg.scheduler_ema_lambda,
            "loop_time_ms": loop_time, "e2e_time_ms": e2e_ms, "actual_cpu_loop_wall_ms": actual_cpu_loop_wall_ms,
            "actual_cpu_e2e_ms": _actual_cpu_e2e_ms, "wall_clock_interval_ms": wall_clock_interval_ms,
            "total_atomic_cpu_ms": total_atomic_cpu_ms,
            "actual_cpu_loop_overrun": bool(actual_cpu_loop_wall_ms > cfg.allowed_ms),
            "actual_cpu_e2e_overrun": bool(_actual_cpu_e2e_ms > cfg.B_tau_ms),
            "actual_cpu_e2e_overrun_ms": max(0.0, _actual_cpu_e2e_ms - cfg.B_tau_ms),
            "timing_mode": cfg.timing_mode, "budget_unit": budget_unit, "rollout_charge_ms": cfg.rollout_charge_ms,
            "selected_module": selected_module,
            "atomic_step_duration_ms": last_atomic_ms, "num_ga_steps": interval_counts.get("GA", 0),
            "total_rollout_equivalents": total_rollout_equivalents,
            "last_step_rollout_equivalents": last_step_rollout_equivalents,
            "num_pso_steps": interval_counts.get("PSO", 0), "num_rl_steps": interval_counts.get("RL", 0),
            "candidate_count": len(candidates), "evaluated_candidate_count": len(candidates), "score": eval_metrics["score"],
            "return": eval_metrics["return"], "win": eval_metrics["win_rate"], "threshold_T": cfg.threshold_T,
            "steps_to_threshold": steps_to_T, "evaluation_cadence": 1,
            "atomic_eval_rollouts": atomic_eval_rollouts,
            "p95_latency_ms": float(np.percentile(e2e_history, 95)), "p99_latency_ms": float(np.percentile(e2e_history, 99)),
            "max_latency_ms": float(np.max(e2e_history)), "loop_overrun": bool(loop_time > cfg.allowed_ms),
            "e2e_overrun": bool(e2e_ms > cfg.B_tau_ms), "loop_overrun_ms": max(0.0, loop_time - cfg.allowed_ms),
            "e2e_overrun_ms": max(0.0, e2e_ms - cfg.B_tau_ms), "diversity_value": last_div,
            "diversity_descriptor_valid": bool(np.isfinite(last_div) and last_div > 1e-12),
            "learning_progress_value": last_lp, "improvement_rate_value": last_imp,
            "scheduler_index_ga": idx.get("GA", 0.0), "scheduler_index_pso": idx.get("PSO", 0.0), "scheduler_index_rl": idx.get("RL", 0.0),
            "rng_train_seed": train_seeds[0], "rng_eval_seed": eval_seeds[0], "hardware_id": hw,
            "handshake_enabled": handshake_enabled, "handshake_events": interval_handshake_events,
            "required_budget_ga_ms": required.get("GA", 0.0), "required_budget_pso_ms": required.get("PSO", 0.0),
            "required_budget_rl_ms": required.get("RL", 0.0), "selected_required_budget_ms": selected_required_budget_ms,
            "budget_utilization": loop_time / max(cfg.allowed_ms, 1e-9), "meta_mode": current_meta_mode,
            "notes": "self-contained local validation harness; charged-time accounting is disclosed by timing_mode",
        })

    metadata = env0.metadata.to_dict()
    metadata.update({
        "training_seed_schedule": train_seeds,
        "evaluation_seed_schedule": eval_seeds,
        "rollout_horizon_H": cfg.horizon,
        "number_of_rollouts_K": cfg.eval_rollouts_K,
        "performance_threshold_T": cfg.threshold_T,
        "steps_to_T_definition": "First interval at which mean evaluation score >= T, converted to environment-step cap units.",
        "hardware_id": hw,
        "operating_system": platform.platform(),
        "python_version": platform.python_version(),
        "runtime": f"Python {platform.python_version()}",
        "library_versions": library_versions(),
        "B_tau_ms": cfg.B_tau_ms,
        "B_tau_budget_units": cfg.B_tau_ms,
        "allowed_ms": cfg.allowed_ms,
        "allowed_budget_units": cfg.allowed_ms,
        "delta_min_ms": cfg.delta_min_ms,
        "delta_max_ms": cfg.delta_max_ms,
        "guard_margin_ms": cfg.guard_margin_ms,
        "environment_step_cap_per_interval": cfg.step_cap_per_interval,
        "evaluation_cadence": 1,
        "atomic_eval_rollouts": atomic_eval_rollouts,
        "timing_mode": cfg.timing_mode,
        "budget_unit": "rollout-equivalent unit" if cfg.timing_mode == "rollout_normalized" else "ms",
        "rollout_charge_ms": cfg.rollout_charge_ms,
        "scheduler_ema_lambda": cfg.scheduler_ema_lambda,
        "risk_adaptive_scheduler": "RAPID-DLGPR and RAPID-racing-DLGPR learn module-specific do-not-start thresholds from charged-duration histories; these variants are bounded-risk diagnostics and are reported separately from strict_delta_max theorem validation.",
        "timing_mode_definition": "simulated_charged uses deterministic charged durations for scheduler stress tests; rollout_normalized charges each evaluation or training rollout, including RL-to-population injection evaluations, as rollout_charge_ms declared rollout-equivalent units; actual_cpu_clipped charges measured CPU time clipped to the declared atomic-step bounds; actual_cpu_raw charges measured CPU time without clipping for profiling diagnostics. actual_cpu_e2e_ms is the measured budget-critical atomic loop plus guard margin; wall_clock_interval_ms additionally includes offline evaluation/logging overhead.",
        "rollout_accounting_scope": "Atomic-step evaluation rollouts, RL training rollouts, and RL-to-GA/PSO injection evaluations are charged during rollout_normalized runs. One-rollout GA/PSO memory initialization and final per-interval incumbent evaluation are disclosed offline setup/evaluation work outside the online scheduler account.",
        "cross_layer_handoff": "When enabled, RL candidates are injected into GA/PSO elite memories and GA/PSO teachers distill RL parameters within the selected atomic-step charge.",
    })
    return interval_logs, atomic_logs, metadata


def write_csv(path: Path, rows: List[Dict[str, Any]], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def run_suite(cfg: ExperimentConfig, methods: List[str], output_dir: Path) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    all_intervals: List[Dict[str, Any]] = []
    all_atomic: List[Dict[str, Any]] = []
    metadata_bundle: Dict[str, Any] = {"config": asdict(cfg), "tasks": {}}
    for task in cfg.tasks:
        metadata_bundle["tasks"].setdefault(task, {})
        for method in methods:
            for seed in cfg.seeds:
                interval_rows, atomic_rows, metadata = run_one(cfg, method, task, seed, output_dir)
                all_intervals.extend(interval_rows)
                all_atomic.extend(atomic_rows)
                metadata_bundle["tasks"][task] = metadata
    write_csv(output_dir / "interval_logs.csv", all_intervals, INTERVAL_FIELDS)
    write_csv(output_dir / "atomic_step_logs.csv", all_atomic, ATOMIC_FIELDS)
    with (output_dir / "environment_metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata_bundle, f, indent=2)
    return {"interval_rows": len(all_intervals), "atomic_rows": len(all_atomic), "metadata": metadata_bundle}
