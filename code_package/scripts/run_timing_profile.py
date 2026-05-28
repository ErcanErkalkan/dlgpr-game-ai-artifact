#!/usr/bin/env python3
"""Run raw-CPU timing diagnostics for the strict and relaxed budget variants."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dlgpr.experiment import ExperimentConfig, run_suite


TIMING_TASKS = ["line-duel", "resource-defense", "gym-frozenlake-4x4", "gym-cliffwalking", "minigrid-empty-5x5"]
TIMING_METHODS = ["DLGPR-full", "strict-delta-max", "relaxed-delta-min"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Run a small timing smoke test.")
    parser.add_argument("--full", action="store_true", help="Run the manuscript-scale raw-CPU timing profile.")
    parser.add_argument(
        "--output",
        default="../experiments/tog2026_timing_profile/logs/timing_profile",
        help="Output directory relative to code_package.",
    )
    args = parser.parse_args()

    if args.full:
        cfg = ExperimentConfig(
            tasks=TIMING_TASKS,
            seeds=list(range(5)),
            intervals=20,
            horizon=4,
            eval_rollouts_K=1,
            B_tau_ms=100.0,
            guard_margin_ms=10.0,
            delta_min_ms=1.0,
            delta_max_ms=40.0,
            timing_mode="actual_cpu_raw",
        )
    else:
        cfg = ExperimentConfig(
            tasks=TIMING_TASKS,
            seeds=[0],
            intervals=3,
            horizon=4,
            eval_rollouts_K=1,
            B_tau_ms=100.0,
            guard_margin_ms=10.0,
            delta_min_ms=1.0,
            delta_max_ms=40.0,
            timing_mode="actual_cpu_raw",
        )

    out = (ROOT / args.output).resolve()
    result = run_suite(cfg, TIMING_METHODS, out)
    print("Raw-CPU timing profile complete")
    print(f"Interval rows: {result['interval_rows']}")
    print(f"Atomic rows: {result['atomic_rows']}")
    print(f"Output: {out}")


if __name__ == "__main__":
    main()
