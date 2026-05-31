#!/usr/bin/env python3
"""Run matched-budget validation on optional Gymnasium benchmark tasks."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
ARTIFACT_ROOT = SCRIPT_PATH.parents[2]
sys.path.insert(0, str(CODE_ROOT))

from dlgpr.experiment import ExperimentConfig, run_suite


EXTERNAL_TASKS = [
    "gym-frozenlake-4x4",
    "gym-frozenlake-4x4-deterministic",
    "gym-cliffwalking",
    "gym-blackjack",
]
MINIGRID_TASKS = ["minigrid-empty-5x5"]

# Manuscript-consistent robust external validation method set.
# Do not replace this with dlgpr.experiment.METHODS unless the README,
# precomputed logs, tables, and manuscript external-validation counts are
# intentionally regenerated and updated. The official full external run is:
# 4 Gymnasium tasks x 10 seeds x 12 intervals x 8 methods = 3,840 interval rows.
EXTERNAL_ROBUST_METHODS = [
    "robust-DLGPR",
    "robust-near-elite-DLGPR",
    "DLGPR-full",
    "fixed-split",
    "round-robin",
    "greedy-improvement",
    "no-non-starvation",
    "no-handshake",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Run a small external smoke validation.")
    parser.add_argument("--full", action="store_true", help="Run the manuscript-scale external validation.")
    parser.add_argument("--include-minigrid", action="store_true", help="Also run the slower MiniGrid adapter smoke task.")
    parser.add_argument(
        "--output",
        default="experiments/tog2026_external_gymnasium/logs/external_validation",
        help="Output directory relative to the artifact root.",
    )
    args = parser.parse_args()

    tasks = EXTERNAL_TASKS + (MINIGRID_TASKS if args.include_minigrid else [])

    if args.full:
        cfg = ExperimentConfig(tasks=tasks, seeds=list(range(10)), intervals=12, horizon=80, eval_rollouts_K=5)
    else:
        cfg = ExperimentConfig(tasks=tasks, seeds=[0, 1], intervals=4, horizon=32, eval_rollouts_K=2)

    out = (Path(args.output) if Path(args.output).is_absolute() else ARTIFACT_ROOT / args.output).resolve()
    result = run_suite(cfg, EXTERNAL_ROBUST_METHODS, out)
    print("External Gymnasium validation complete")
    print(f"Methods: {len(EXTERNAL_ROBUST_METHODS)}")
    print(f"Method list: {', '.join(EXTERNAL_ROBUST_METHODS)}")
    print(f"Interval rows: {result['interval_rows']}")
    print(f"Atomic rows: {result['atomic_rows']}")
    print(f"Output: {out}")


if __name__ == "__main__":
    main()
