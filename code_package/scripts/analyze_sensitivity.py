#!/usr/bin/env python3
"""Analyze compact budget-sensitivity logs."""
from __future__ import annotations

from pathlib import Path
import sys
import pandas as pd
import numpy as np

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
ARTIFACT_ROOT = SCRIPT_PATH.parents[2]


def main() -> None:
    in_path = ARTIFACT_ROOT / "code_package" / "logs" / "sensitivity" / "sensitivity_interval_logs.csv"
    out_dir = ARTIFACT_ROOT / "code_package" / "paper" / "revised" / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)
    if not in_path.exists():
        raise SystemExit(f"Missing sensitivity log: {in_path}. Run code_package/scripts/run_sensitivity.py first.")
    df = pd.read_csv(in_path)
    if "scheduler_ema_lambda" not in df.columns:
        df["scheduler_ema_lambda"] = 0.75
    final = df.sort_values("interval").groupby(["task_name", "method", "seed", "B_tau_ms", "scheduler_ema_lambda"], as_index=False).tail(1)
    rows = []
    for (task, method, budget, lam), g in final.groupby(["task_name", "method", "B_tau_ms", "scheduler_ema_lambda"]):
        lat = df[(df.task_name == task) & (df.method == method) & (df.B_tau_ms == budget) & (df.scheduler_ema_lambda == lam)]
        rows.append({
            "task_name": task,
            "method": method,
            "B_tau_ms": budget,
            "scheduler_ema_lambda": lam,
            "return_mean_up": float(g["return"].mean()),
            "return_std": float(g["return"].std(ddof=1)) if len(g) > 1 else 0.0,
            "return_median_up": float(g["return"].median()),
            "win_rate_up": float(g["win"].mean()),
            "p99_latency_ms_down": float(np.percentile(lat["e2e_time_ms"], 99)),
            "loop_overrun_rate_down": float(lat["loop_overrun"].astype(bool).mean()),
            "mean_unused_loop_budget_ms_context": float(np.maximum(0.0, lat["allowed_ms"] - lat["loop_time_ms"]).mean()),
        })
    table = pd.DataFrame(rows).sort_values(["task_name", "method", "B_tau_ms", "scheduler_ema_lambda"])
    out = out_dir / "table_budget_sensitivity.csv"
    table.to_csv(out, index=False)
    print(out)


if __name__ == "__main__":
    main()
