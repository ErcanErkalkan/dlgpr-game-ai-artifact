#!/usr/bin/env python3
"""Run the full matched-budget validation harness."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dlgpr.experiment import ExperimentConfig, METHODS, run_suite


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Run a fast smoke validation with all methods.")
    parser.add_argument("--full", action="store_true", help="Run a larger local validation.")
    parser.add_argument("--output", default="logs/full_validation", help="Output directory.")
    args = parser.parse_args()

    if args.full:
        cfg = ExperimentConfig(tasks=["line-duel", "grid-treasure", "resource-defense"], seeds=list(range(10)), intervals=40, eval_rollouts_K=5)
    else:
        cfg = ExperimentConfig(tasks=["line-duel", "grid-treasure", "resource-defense"], seeds=[0, 1], intervals=4, horizon=18, eval_rollouts_K=2)

    out = ROOT / args.output
    result = run_suite(cfg, METHODS, out)
    print("Validation run complete")
    print(f"Interval rows: {result['interval_rows']}")
    print(f"Atomic rows: {result['atomic_rows']}")
    print(f"Output: {out}")


if __name__ == "__main__":
    main()
