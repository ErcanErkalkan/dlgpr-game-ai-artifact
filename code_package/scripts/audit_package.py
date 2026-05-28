#!/usr/bin/env python3
"""Audit the revision package for reviewer-critical missing artifacts."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import argparse
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "LICENSE",
    "CITATION.cff",
    "docs/ENVIRONMENT_DISCLOSURE.md",
    "docs/METRIC_DEFINITIONS.md",
    "docs/EXTERNAL_BENCHMARK_ADAPTERS.md",
    "docs/REPRODUCIBILITY.md",
    "docs/MANUSCRIPT_INTEGRATION.md",
    "Dockerfile",
    "Makefile",
]

REQUIRED_INTERVAL_COLUMNS = [
    "run_id", "seed", "method", "benchmark", "environment_name", "environment_version",
    "task_name", "interval", "B_tau_ms", "allowed_ms", "delta_min_ms", "delta_max_ms",
    "do_not_start_rule", "scheduler_ema_lambda", "loop_time_ms", "e2e_time_ms", "actual_cpu_loop_wall_ms",
    "actual_cpu_e2e_ms", "wall_clock_interval_ms", "total_atomic_cpu_ms", "actual_cpu_loop_overrun", "actual_cpu_e2e_overrun",
    "timing_mode", "selected_module", "atomic_step_duration_ms",
    "score", "return", "win", "threshold_T", "steps_to_threshold",
    "p95_latency_ms", "p99_latency_ms", "max_latency_ms", "loop_overrun", "e2e_overrun",
    "diversity_value", "learning_progress_value", "improvement_rate_value",
    "handshake_enabled", "handshake_events", "rng_train_seed", "rng_eval_seed", "hardware_id",
]

REQUIRED_ATOMIC_COLUMNS = [
    "run_id", "seed", "method", "task_name", "interval", "atomic_index", "module",
    "charged_ms", "cpu_ms", "score", "improvement_rate", "diversity",
    "learning_progress", "remaining_before_ms", "remaining_after_ms", "do_not_start_rule",
]

REQUIRED_METHODS = {
    "DLGPR-full", "GA-only", "PSO-only", "RL-only", "fixed-split", "round-robin",
    "greedy-improvement", "no-diversity", "no-learning-progress", "no-ucb",
    "no-non-starvation", "no-handshake", "strict-delta-max", "relaxed-delta-min",
}

TIMING_METHODS = {"DLGPR-full", "strict-delta-max", "relaxed-delta-min"}


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.parent.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def audit(log_dir: Path | None = None, table_dir: Path | None = None) -> tuple[bool, str]:
    log_dir = log_dir or (ROOT / "logs/full_validation")
    table_dir = table_dir or (ROOT / "paper/revised/tables")
    lines: list[str] = ["# Package Audit Report", ""]
    ok = True
    for rel in REQUIRED_FILES:
        exists = (ROOT / rel).exists()
        lines.append(f"- [{'OK' if exists else 'MISSING'}] {rel}")
        ok = ok and exists
    lines.append("")

    lines.append(f"Log directory: {display_path(log_dir)}")
    for rel in ["interval_logs.csv", "atomic_step_logs.csv", "environment_metadata.json"]:
        exists = (log_dir / rel).exists()
        lines.append(f"- [{'OK' if exists else 'MISSING'}] {display_path(log_dir / rel)}")
        ok = ok and exists
    lines.append("")

    log_path = log_dir / "interval_logs.csv"
    if log_path.exists():
        df = pd.read_csv(log_path)
        missing_cols = [c for c in REQUIRED_INTERVAL_COLUMNS if c not in df.columns]
        lines.append(f"## Interval log rows: {len(df)}")
        lines.append(f"Missing interval columns: {missing_cols if missing_cols else 'none'}")
        ok = ok and not missing_cols
        methods = set(df["method"].unique()) if "method" in df.columns else set()
        is_timing_profile = "timing_mode" in df.columns and set(df["timing_mode"].dropna().unique()) == {"actual_cpu_raw"} and methods.issubset(TIMING_METHODS)
        expected_methods = TIMING_METHODS if is_timing_profile else REQUIRED_METHODS
        missing_methods = sorted(expected_methods - methods)
        lines.append(f"Missing methods: {missing_methods if missing_methods else 'none'}")
        ok = ok and not missing_methods
        if "method" in df.columns and "handshake_events" in df.columns:
            hs = df.groupby("method")["handshake_events"].sum().to_dict()
            lines.append(f"Handshake events by method: {hs}")
            ok = ok and hs.get("DLGPR-full", 0) > 0
            if "no-handshake" in methods:
                ok = ok and hs.get("no-handshake", 1) == 0
        strict = df[df.get("method", "") == "strict-delta-max"]
        if not strict.empty and "loop_overrun" in strict.columns:
            strict_overruns = int(strict["loop_overrun"].astype(bool).sum())
            lines.append(f"Strict-delta-max loop overruns: {strict_overruns}")
            ok = ok and strict_overruns == 0
    lines.append("")

    atomic_path = log_dir / "atomic_step_logs.csv"
    if atomic_path.exists():
        atomic_df = pd.read_csv(atomic_path)
        missing_atomic_cols = [c for c in REQUIRED_ATOMIC_COLUMNS if c not in atomic_df.columns]
        lines.append(f"## Atomic-step log rows: {len(atomic_df)}")
        lines.append(f"Missing atomic-step columns: {missing_atomic_cols if missing_atomic_cols else 'none'}")
        ok = ok and not missing_atomic_cols
        if "module" in atomic_df.columns:
            modules = sorted(atomic_df["module"].dropna().unique().tolist())
            lines.append(f"Atomic modules observed: {modules}")
            ok = ok and set(modules).issubset({"GA", "PSO", "RL"}) and bool(modules)
    lines.append("")

    meta_path = log_dir / "environment_metadata.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8-sig"))
        required_meta = [
            "environment_name", "environment_version", "benchmark_family", "task_name",
            "observation_definition", "action_definition", "reward_definition",
            "episode_termination", "opponent_policy", "stochasticity_sources",
            "training_seed_schedule", "evaluation_seed_schedule", "rollout_horizon_H",
            "number_of_rollouts_K", "B_tau_ms", "delta_min_ms", "delta_max_ms", "guard_margin_ms",
            "evaluation_cadence", "timing_mode", "scheduler_ema_lambda", "operating_system", "runtime", "library_versions",
        ]
        task_count = len(meta.get("tasks", {}))
        lines.append(f"Metadata task count: {task_count}")
        ok = ok and task_count >= 3
        for task, item in meta.get("tasks", {}).items():
            missing = [k for k in required_meta if k not in item or item[k] in (None, "")]
            lines.append(f"Metadata missing for {task}: {missing if missing else 'none'}")
            ok = ok and not missing
    lines.append("")

    table_checks = {
        "table_main_results.csv": ["return_mean_up", "return_std", "return_median_up", "return_ci95", "p95_latency_ms_down", "p99_latency_ms_down", "max_latency_ms_down", "loop_overrun_rate_down", "e2e_overrun_rate_down"],
        "table_strict_vs_relaxed.csv": ["loop_overrun_rate_down", "e2e_overrun_rate_down", "p95_latency_ms_down", "p99_latency_ms_down", "max_overrun_ms_down", "unused_budget_ms_context"],
        "table_statistical_tests.csv": ["DLGPR_mean", "DLGPR_std", "DLGPR_median", "DLGPR_ci95", "comparator_mean", "comparator_std", "comparator_median", "comparator_ci95", "p_value", "p_value_holm", "effect_size_cliffs_delta"],
        "table_timing_profile.csv": ["charged_e2e_p99_ms_down", "actual_cpu_e2e_p99_ms_down", "actual_cpu_e2e_overrun_rate_down"],
    }
    lines.append(f"Table directory: {display_path(table_dir)}")
    for filename, cols in table_checks.items():
        path = table_dir / filename
        exists = path.exists()
        lines.append(f"- [{'OK' if exists else 'MISSING'}] {display_path(path)}")
        ok = ok and exists
        if exists:
            table = pd.read_csv(path, nrows=1)
            missing = [c for c in cols if c not in table.columns]
            lines.append(f"  Missing table columns: {missing if missing else 'none'}")
            ok = ok and not missing
    lines.append("")
    lines.append(f"Overall status: {'PASS' if ok else 'FAIL'}")
    return ok, "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-dir", default="logs/full_validation")
    parser.add_argument("--table-dir", default="paper/revised/tables")
    parser.add_argument("--out", default="PACKAGE_AUDIT_REPORT.md")
    args = parser.parse_args()
    log_dir = ROOT / args.log_dir
    table_dir = ROOT / args.table_dir
    ok, report = audit(log_dir, table_dir)
    out = ROOT / args.out
    out.write_text(report, encoding="utf-8")
    print(report)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
