#!/usr/bin/env python3
"""Audit the DLGPR artifact against the released root-directory layout.

Official invocation from the artifact root:

    python code_package/scripts/audit_package.py

Relative CLI paths are interpreted from the artifact root, not from
``code_package``.  This prevents stale PASS reports caused by checking the old
pre-release layout.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import pandas as pd
from pandas.errors import EmptyDataError

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
ARTIFACT_ROOT = SCRIPT_PATH.parents[2]

ROOT_REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "LICENSE",
    "CITATION.cff",
    ".zenodo.json",
    "Dockerfile",
    "Makefile",
]

CODE_REQUIRED_FILES = [
    "code_package/docs/ENVIRONMENT_DISCLOSURE.md",
    "code_package/docs/METRIC_DEFINITIONS.md",
    "code_package/docs/EXTERNAL_BENCHMARK_ADAPTERS.md",
    "code_package/docs/REPRODUCIBILITY.md",
    "code_package/docs/MANUSCRIPT_INTEGRATION.md",
    "code_package/docs/METHOD_EQUIVALENCE.md",
    "code_package/docs/DUPLICATE_METHOD_VALIDATION.md",
    "code_package/dlgpr/experiment.py",
    "code_package/dlgpr/scheduler.py",
    "code_package/tests/run_tests.py",
]

CORE_INTERVAL_COLUMNS = [
    "run_id", "seed", "method", "benchmark", "environment_name", "environment_version",
    "task_name", "interval", "B_tau_ms", "allowed_ms", "delta_min_ms", "delta_max_ms",
    "do_not_start_rule", "scheduler_ema_lambda", "loop_time_ms", "e2e_time_ms",
    "actual_cpu_loop_wall_ms", "actual_cpu_e2e_ms", "wall_clock_interval_ms",
    "total_atomic_cpu_ms", "actual_cpu_loop_overrun", "actual_cpu_e2e_overrun",
    "timing_mode", "selected_module", "atomic_step_duration_ms", "score", "return", "win",
    "threshold_T", "steps_to_threshold", "p95_latency_ms", "p99_latency_ms",
    "max_latency_ms", "loop_overrun", "e2e_overrun", "diversity_value",
    "learning_progress_value", "improvement_rate_value", "handshake_enabled",
    "handshake_events", "rng_train_seed", "rng_eval_seed", "hardware_id",
]

FULL_ONLY_INTERVAL_COLUMNS = ["atomic_eval_rollouts"]
ROLLOUT_NORMALIZED_INTERVAL_COLUMNS = [
    "budget_unit", "rollout_charge_ms", "total_rollout_equivalents",
    "last_step_rollout_equivalents",
]

REQUIRED_ATOMIC_COLUMNS = [
    "run_id", "seed", "method", "task_name", "interval", "atomic_index", "module",
    "charged_ms", "cpu_ms", "score", "improvement_rate", "diversity",
    "learning_progress", "remaining_before_ms", "remaining_after_ms", "do_not_start_rule",
]
ROLLOUT_NORMALIZED_ATOMIC_COLUMNS = [
    "evaluation_rollouts", "training_rollouts", "handoff_evaluation_rollouts",
    "rollout_equivalents",
]

FULL_METHODS = {
    "DLGPR-full", "GA-only", "PSO-only", "RL-only", "fixed-split", "round-robin",
    "robust-DLGPR", "robust-near-elite-DLGPR", "greedy-improvement", "no-diversity",
    "no-learning-progress", "no-ucb", "no-non-starvation", "no-handshake",
    "strict-delta-max", "relaxed-delta-min",
}

EXTERNAL_METHODS = {
    "robust-DLGPR", "robust-near-elite-DLGPR", "DLGPR-full", "fixed-split",
    "round-robin", "greedy-improvement", "no-non-starvation", "no-handshake",
}

TIMING_METHODS = {"DLGPR-full", "strict-delta-max", "relaxed-delta-min"}
COMPUTE_MATCHED_METHODS = {
    "robust-DLGPR", "robust-near-elite-DLGPR", "DLGPR-full", "GA-only",
    "PSO-only", "RL-only", "fixed-split", "greedy-improvement",
}

EXPECTED_COUNTS = {
    "full": {"interval_rows": 19200, "atomic_rows": 150297, "methods": FULL_METHODS},
    "external": {"interval_rows": 3840, "atomic_rows": 29698, "methods": EXTERNAL_METHODS},
    "timing": {"interval_rows": 1500, "atomic_rows": 16158, "methods": TIMING_METHODS},
    "compute-matched": {"interval_rows": 9600, "atomic_rows": 134027, "methods": COMPUTE_MATCHED_METHODS},
    "minigrid-performance": {"interval_rows": 960, "atomic_rows": 13543, "methods": COMPUTE_MATCHED_METHODS},
}

REQUIRED_META = [
    "environment_name", "environment_version", "benchmark_family", "task_name",
    "observation_definition", "action_definition", "reward_definition",
    "episode_termination", "opponent_policy", "stochasticity_sources",
    "training_seed_schedule", "evaluation_seed_schedule", "rollout_horizon_H",
    "number_of_rollouts_K", "B_tau_ms", "delta_min_ms", "delta_max_ms",
    "guard_margin_ms", "evaluation_cadence", "timing_mode", "scheduler_ema_lambda",
    "operating_system", "runtime", "library_versions",
]

TABLE_CHECKS_COMMON = {
    "table_method_equivalence.csv": [
        "equivalence_group", "method", "behaviorally_equivalent_to",
        "independent_baseline", "scope", "reason", "reporting_note",
    ],
    "table_main_results.csv": [
        "return_mean_up", "return_std", "return_median_up", "return_ci95",
        "p95_latency_ms_down", "p99_latency_ms_down", "max_latency_ms_down",
        "loop_overrun_rate_down", "e2e_overrun_rate_down",
    ],
    "table_statistical_tests.csv": [
        "DLGPR_mean", "DLGPR_std", "DLGPR_median", "DLGPR_ci95",
        "comparator_mean", "comparator_std", "comparator_median", "comparator_ci95",
        "p_value", "p_value_holm", "paired_mean_difference_DLGPR_minus_comparator",
        "paired_difference_bootstrap_ci95_low", "paired_difference_bootstrap_ci95_high",
        "effect_size_paired_rank_biserial", "effect_size_paired_cohens_dz",
    ],
    "table_timing_profile.csv": [
        "charged_e2e_p99_ms_down", "actual_cpu_e2e_p99_ms_down",
        "actual_cpu_e2e_overrun_rate_down",
    ],
    "table_claim_limits.csv": ["item", "status", "manuscript_use"],
    "table_environment_metadata.csv": ["task_name"],
    "table_metric_definitions.csv": ["metric", "direction", "definition"],
    "table_compute_accounting.csv": [
        "timing_mode", "budget_unit", "atomic_eval_rollouts",
        "mean_online_rollout_equivalents_per_interval", "mean_actual_cpu_loop_wall_ms",
    ],
}

TABLE_CHECKS_FULL_ONLY = {
    "table_strict_vs_relaxed.csv": [
        "loop_overrun_rate_down", "e2e_overrun_rate_down", "p95_latency_ms_down",
        "p99_latency_ms_down", "max_overrun_ms_down", "unused_budget_ms_context",
    ],
    "table_aggregate_vs_dlgpr.csv": [
        "paired_mean_return_delta_vs_DLGPR", "paired_wins_up", "paired_losses_down",
        "tasks_with_positive_mean_delta_up",
    ],
}


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return ARTIFACT_ROOT / path


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ARTIFACT_ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def detect_profile(df: pd.DataFrame, log_dir: Path, explicit: str | None = None) -> str:
    if explicit and explicit != "auto":
        return explicit
    methods = set(df["method"].dropna().unique()) if "method" in df.columns else set()
    log_text = str(log_dir).lower()
    if "timing_profile" in log_text or methods == TIMING_METHODS:
        return "timing"
    if "minigrid_performance" in log_text:
        return "minigrid-performance"
    if "compute_matched" in log_text:
        return "compute-matched"
    if "external" in log_text or methods == EXTERNAL_METHODS:
        return "external"
    return "full"


def add_check(lines: list[str], condition: bool, label: str) -> bool:
    lines.append(f"- [{'OK' if condition else 'FAIL'}] {label}")
    return condition


def read_csv_if_nonempty(path: Path) -> pd.DataFrame | None:
    try:
        return pd.read_csv(path)
    except EmptyDataError:
        return None


def audit(log_dir: Path, table_dir: Path, profile_arg: str | None = "auto") -> tuple[bool, str, str]:
    lines: list[str] = [
        "# Package Audit Report",
        "",
        f"Artifact root: `{display_path(ARTIFACT_ROOT) or '.'}`",
        f"Official command: `python code_package/scripts/audit_package.py`",
        "",
        "## Root and code-layout files",
    ]
    ok = True

    for rel in ROOT_REQUIRED_FILES + CODE_REQUIRED_FILES:
        exists = (ARTIFACT_ROOT / rel).exists()
        lines.append(f"- [{'OK' if exists else 'MISSING'}] {rel}")
        ok = ok and exists

    lines.append("")
    lines.append("## Log files")
    lines.append(f"Log directory: `{display_path(log_dir)}`")
    for rel in ["interval_logs.csv", "atomic_step_logs.csv", "environment_metadata.json"]:
        exists = (log_dir / rel).exists()
        lines.append(f"- [{'OK' if exists else 'MISSING'}] {display_path(log_dir / rel)}")
        ok = ok and exists

    profile = "unknown"
    interval_path = log_dir / "interval_logs.csv"
    atomic_path = log_dir / "atomic_step_logs.csv"

    if interval_path.exists():
        df = pd.read_csv(interval_path)
        profile = detect_profile(df, log_dir, profile_arg)
        expected = EXPECTED_COUNTS.get(profile)
        lines.append("")
        lines.append(f"## Detected profile: `{profile}`")
        lines.append(f"Interval log rows: {len(df):,}")

        required_cols = list(CORE_INTERVAL_COLUMNS)
        if profile == "full":
            required_cols += FULL_ONLY_INTERVAL_COLUMNS
        if profile in {"compute-matched", "minigrid-performance"}:
            required_cols += ROLLOUT_NORMALIZED_INTERVAL_COLUMNS
        missing_cols = [c for c in required_cols if c not in df.columns]
        lines.append(f"Missing interval columns: {missing_cols if missing_cols else 'none'}")
        ok = ok and not missing_cols

        methods = set(df["method"].dropna().unique()) if "method" in df.columns else set()
        if expected:
            missing_methods = sorted(expected["methods"] - methods)
            unexpected_methods = sorted(methods - expected["methods"])
            lines.append(f"Method count: {len(methods)}")
            lines.append(f"Missing methods: {missing_methods if missing_methods else 'none'}")
            lines.append(f"Unexpected methods: {unexpected_methods if unexpected_methods else 'none'}")
            ok = ok and not missing_methods and not unexpected_methods
            ok = add_check(lines, len(df) == expected["interval_rows"], f"expected interval rows = {expected['interval_rows']:,}") and ok

        if "handshake_events" in df.columns and "method" in df.columns:
            hs = df.groupby("method")["handshake_events"].sum().to_dict()
            lines.append(f"Handshake events by method: {hs}")
            if "DLGPR-full" in methods:
                ok = add_check(lines, hs.get("DLGPR-full", 0) > 0, "DLGPR-full has positive handshake events") and ok
            if "no-handshake" in methods:
                ok = add_check(lines, hs.get("no-handshake", 1) == 0, "no-handshake has zero handshake events") and ok

        if {"method", "loop_overrun"}.issubset(df.columns):
            strict = df[df["method"] == "strict-delta-max"]
            if not strict.empty:
                strict_overruns = int(strict["loop_overrun"].astype(bool).sum())
                lines.append(f"Strict-delta-max loop overruns: {strict_overruns}")
                ok = add_check(lines, strict_overruns == 0, "strict-delta-max has zero charged-time loop overruns") and ok

    if atomic_path.exists():
        atomic_df = pd.read_csv(atomic_path)
        lines.append("")
        lines.append(f"## Atomic-step log rows: {len(atomic_df):,}")
        missing_atomic_cols = [c for c in REQUIRED_ATOMIC_COLUMNS if c not in atomic_df.columns]
        if profile in {"compute-matched", "minigrid-performance"}:
            missing_atomic_cols += [c for c in ROLLOUT_NORMALIZED_ATOMIC_COLUMNS if c not in atomic_df.columns]
        lines.append(f"Missing atomic-step columns: {missing_atomic_cols if missing_atomic_cols else 'none'}")
        ok = ok and not missing_atomic_cols
        expected = EXPECTED_COUNTS.get(profile)
        if expected:
            ok = add_check(lines, len(atomic_df) == expected["atomic_rows"], f"expected atomic rows = {expected['atomic_rows']:,}") and ok
        if "module" in atomic_df.columns:
            modules = sorted(atomic_df["module"].dropna().unique().tolist())
            lines.append(f"Atomic modules observed: {modules}")
            ok = add_check(lines, bool(modules) and set(modules).issubset({"GA", "PSO", "RL"}), "atomic modules are within GA/PSO/RL") and ok

    meta_path = log_dir / "environment_metadata.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8-sig"))
        lines.append("")
        lines.append("## Environment metadata")
        tasks = meta.get("tasks", {})
        lines.append(f"Metadata task count: {len(tasks)}")
        min_task_count = 1 if profile == "minigrid-performance" else 3
        ok = add_check(lines, len(tasks) >= min_task_count, f"metadata contains at least {min_task_count} task(s)") and ok
        for task, item in tasks.items():
            missing = [k for k in REQUIRED_META if k not in item or item[k] in (None, "")]
            lines.append(f"Metadata missing for {task}: {missing if missing else 'none'}")
            ok = ok and not missing

    lines.append("")
    lines.append("## Generated tables")
    lines.append(f"Table directory: `{display_path(table_dir)}`")
    table_checks = dict(TABLE_CHECKS_COMMON)
    if profile == "full":
        table_checks.update(TABLE_CHECKS_FULL_ONLY)
    for filename, cols in table_checks.items():
        path = table_dir / filename
        exists = path.exists()
        lines.append(f"- [{'OK' if exists else 'MISSING'}] {display_path(path)}")
        ok = ok and exists
        if exists:
            table = read_csv_if_nonempty(path)
            if table is None:
                lines.append("  Empty table: acceptable only when no rows are applicable; not used for this required check.")
                ok = False
                continue
            missing = [c for c in cols if c not in table.columns]
            lines.append(f"  Missing table columns: {missing if missing else 'none'}")
            ok = ok and not missing
            if filename == "table_method_equivalence.csv" and table is not None and not missing:
                expected_pairs = {
                    ("DLGPR-full", "strict-delta-max"),
                    ("strict-delta-max", "DLGPR-full"),
                    ("fixed-split", "round-robin"),
                    ("round-robin", "fixed-split"),
                }
                observed_pairs = set(zip(table["method"], table["behaviorally_equivalent_to"]))
                lines.append("  Method-equivalence pair validation: " + ("OK" if expected_pairs.issubset(observed_pairs) else "FAIL"))
                ok = ok and expected_pairs.issubset(observed_pairs)

    lines.append("")
    lines.append(f"Overall status: {'PASS' if ok else 'FAIL'}")
    return ok, "\n".join(lines) + "\n", profile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-dir", default="experiments/tog2026_full_validation/logs/full_validation")
    parser.add_argument("--table-dir", default="experiments/tog2026_full_validation/paper/revised/tables")
    parser.add_argument("--profile", default="auto", choices=["auto", "full", "external", "timing", "compute-matched", "minigrid-performance"])
    parser.add_argument("--out", default="PACKAGE_AUDIT_REPORT.md")
    args = parser.parse_args()

    log_dir = resolve_path(args.log_dir)
    table_dir = resolve_path(args.table_dir)
    ok, report, _profile = audit(log_dir, table_dir, args.profile)
    out = resolve_path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(report)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
