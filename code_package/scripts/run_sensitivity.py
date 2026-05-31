#!/usr/bin/env python3
"""Run a compact budget-sensitivity suite."""
from __future__ import annotations

from pathlib import Path
import sys
import pandas as pd

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
ARTIFACT_ROOT = SCRIPT_PATH.parents[2]
sys.path.insert(0, str(CODE_ROOT))

from dlgpr.experiment import ExperimentConfig, run_suite


def main() -> None:
    budgets = [18.0, 24.0, 30.0]
    smoothing = [0.50, 0.75, 0.90]
    methods = ["DLGPR-full", "fixed-split", "round-robin", "greedy-improvement"]
    all_frames = []
    out_root = ARTIFACT_ROOT / "code_package" / "logs" / "sensitivity"
    out_root.mkdir(parents=True, exist_ok=True)
    for b in budgets:
        for lam in smoothing:
            cfg = ExperimentConfig(
                tasks=["line-duel", "grid-treasure", "resource-defense"],
                seeds=[0, 1, 2],
                intervals=6,
                horizon=18,
                B_tau_ms=b,
                guard_margin_ms=2.0,
                eval_rollouts_K=2,
                scheduler_ema_lambda=lam,
            )
            out = out_root / f"B{int(b)}_ema{int(lam * 100)}"
            run_suite(cfg, methods, out)
            df = pd.read_csv(out / "interval_logs.csv")
            all_frames.append(df)
    merged = pd.concat(all_frames, ignore_index=True)
    merged.to_csv(out_root / "sensitivity_interval_logs.csv", index=False)
    print(out_root / "sensitivity_interval_logs.csv")


if __name__ == "__main__":
    main()
