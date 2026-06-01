#!/usr/bin/env python3
"""Run compute-matched validation with rollout-equivalent or raw-CPU charges."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
ARTIFACT_ROOT = SCRIPT_PATH.parents[2]
sys.path.insert(0, str(CODE_ROOT))

from dlgpr.experiment import ExperimentConfig, run_suite


TASKS = ["line-duel", "grid-treasure", "resource-defense"]
METHODS = [
    "robust-DLGPR",
    "robust-near-elite-DLGPR",
    "DLGPR-full",
    "GA-only",
    "PSO-only",
    "RL-only",
    "fixed-split",
    "greedy-improvement",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Run a small compute-matched smoke validation.")
    parser.add_argument("--full", action="store_true", help="Run the manuscript-scale compute-matched validation.")
    parser.add_argument(
        "--basis",
        choices=["rollout", "actual-cpu"],
        default="rollout",
        help="Charge online optimization by rollout-equivalent work or raw measured CPU time.",
    )
    parser.add_argument("--output", help="Output directory relative to the artifact root.")
    args = parser.parse_args()

    if args.basis == "rollout":
        cfg = ExperimentConfig(
            tasks=TASKS,
            seeds=list(range(10)) if args.full else [0, 1],
            intervals=40 if args.full else 4,
            horizon=24 if args.full else 18,
            eval_rollouts_K=5 if args.full else 3,
            B_tau_ms=40.0,
            guard_margin_ms=0.0,
            delta_min_ms=1.0,
            delta_max_ms=16.0,
            timing_mode="rollout_normalized",
            rollout_charge_ms=1.0,
        )
        default_output = "experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout"
    else:
        cfg = ExperimentConfig(
            tasks=TASKS,
            seeds=list(range(10)) if args.full else [0, 1],
            intervals=20 if args.full else 4,
            horizon=24 if args.full else 18,
            eval_rollouts_K=5 if args.full else 3,
            B_tau_ms=250.0,
            guard_margin_ms=25.0,
            delta_min_ms=1.0,
            delta_max_ms=100.0,
            timing_mode="actual_cpu_raw",
        )
        default_output = "experiments/ec2026_compute_matched_actual_cpu/logs/compute_matched_actual_cpu"

    output = Path(args.output or default_output)
    out = (output if output.is_absolute() else ARTIFACT_ROOT / output).resolve()
    result = run_suite(cfg, METHODS, out)
    print("Compute-matched validation complete")
    print(f"Basis: {args.basis}")
    print(f"Methods: {len(METHODS)}")
    print(f"Interval rows: {result['interval_rows']}")
    print(f"Atomic rows: {result['atomic_rows']}")
    print(f"Output: {out}")


if __name__ == "__main__":
    main()
