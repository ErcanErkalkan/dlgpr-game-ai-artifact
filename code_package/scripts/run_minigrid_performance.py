#!/usr/bin/env python3
"""Run rollout-equivalent MiniGrid Empty-5x5 performance validation."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
ARTIFACT_ROOT = SCRIPT_PATH.parents[2]
sys.path.insert(0, str(CODE_ROOT))

from dlgpr.experiment import ExperimentConfig, run_suite


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
    parser.add_argument("--quick", action="store_true", help="Run a small MiniGrid performance smoke validation.")
    parser.add_argument("--full", action="store_true", help="Run the manuscript-scale MiniGrid performance validation.")
    parser.add_argument(
        "--output",
        default="experiments/ec2026_minigrid_performance/logs/minigrid_performance",
        help="Output directory relative to the artifact root.",
    )
    args = parser.parse_args()

    cfg = ExperimentConfig(
        tasks=["minigrid-empty-5x5-fullyobs"],
        seeds=list(range(10)) if args.full else [0, 1],
        intervals=12 if args.full else 4,
        horizon=32,
        eval_rollouts_K=5 if args.full else 3,
        B_tau_ms=40.0,
        guard_margin_ms=0.0,
        delta_min_ms=1.0,
        delta_max_ms=16.0,
        timing_mode="rollout_normalized",
        rollout_charge_ms=1.0,
    )
    output = Path(args.output)
    out = (output if output.is_absolute() else ARTIFACT_ROOT / output).resolve()
    result = run_suite(cfg, METHODS, out)
    print("MiniGrid performance validation complete")
    print(f"Methods: {len(METHODS)}")
    print(f"Interval rows: {result['interval_rows']}")
    print(f"Atomic rows: {result['atomic_rows']}")
    print(f"Output: {out}")


if __name__ == "__main__":
    main()
