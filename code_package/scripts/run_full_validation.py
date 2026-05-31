#!/usr/bin/env python3
"""Run the full matched-budget validation harness.

Relative output paths are interpreted from the artifact root.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
ARTIFACT_ROOT = SCRIPT_PATH.parents[2]
sys.path.insert(0, str(CODE_ROOT))

from dlgpr.experiment import ExperimentConfig, METHODS, run_suite


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return ARTIFACT_ROOT / path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Run a fast smoke validation with all methods.")
    parser.add_argument("--full", action="store_true", help="Run a larger local validation.")
    parser.add_argument("--output", default="code_package/logs/full_validation", help="Output directory relative to the artifact root.")
    args = parser.parse_args()

    if args.full:
        cfg = ExperimentConfig(tasks=["line-duel", "grid-treasure", "resource-defense"], seeds=list(range(10)), intervals=40, eval_rollouts_K=5)
    else:
        cfg = ExperimentConfig(tasks=["line-duel", "grid-treasure", "resource-defense"], seeds=[0, 1], intervals=4, horizon=18, eval_rollouts_K=2)

    out = resolve_path(args.output)
    result = run_suite(cfg, METHODS, out)
    print("Validation run complete")
    print(f"Interval rows: {result['interval_rows']}")
    print(f"Atomic rows: {result['atomic_rows']}")
    print(f"Output: {out}")


if __name__ == "__main__":
    main()
