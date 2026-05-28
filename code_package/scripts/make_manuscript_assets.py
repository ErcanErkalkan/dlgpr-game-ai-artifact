#!/usr/bin/env python3
"""Generate manuscript-ready text snippets from completed local logs.

The generated text is intentionally conservative: it labels the local tasks as
self-contained validation tasks and prevents overclaiming broad Game AI
benchmark generalization.
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import json
import argparse

ROOT = Path(__file__).resolve().parents[1]


def load_csv(table_dir: Path, name: str) -> pd.DataFrame:
    path = table_dir / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def metric_direction_note() -> str:
    return (
        "Throughout the local validation tables, higher values are better for return, score, and win rate. "
        "Lower values are better for steps-to-threshold, p95/p99 latency, maximum latency, and overrun rates. "
        "Handshake counts are diagnostic and are not interpreted as a performance metric."
    )


def main_results_text(main: pd.DataFrame) -> str:
    if main.empty:
        return "Main-result table not found. Run scripts/analyze_results.py first."
    lines = ["## Manuscript-ready Results Narrative", "", metric_direction_note(), ""]
    for task in sorted(main["task_name"].unique()):
        gt = main[main.task_name == task].copy()
        if "return_mean_up" in gt.columns:
            gt = gt.sort_values("return_mean_up", ascending=False)
            best = gt.iloc[0]
            full = gt[gt.method == "DLGPR-full"]
            full_txt = "not available"
            if not full.empty:
                row = full.iloc[0]
                full_txt = f"mean return {row['return_mean_up']:.3f}, win rate {row['win_rate_up']:.3f}, p99 latency {row['p99_latency_ms_down']:.3f} ms"
            lines.append(
                f"For `{task}`, the self-contained validation harness reports the best mean return for `{best['method']}` "
                f"({best['return_mean_up']:.3f}). The DLGPR-full configuration reports {full_txt}. "
                "These values support implementation-level comparison under matched local budgets, not broad benchmark generalization."
            )
    return "\n\n".join(lines) + "\n"


def strict_relaxed_text(strict: pd.DataFrame) -> str:
    if strict.empty:
        return "Strict/relaxed timing table not found."
    lines = ["## Strict versus relaxed timing interpretation", ""]
    for task in sorted(strict["task_name"].unique()):
        gt = strict[strict.task_name == task]
        for _, row in gt.iterrows():
            lines.append(
                f"For `{task}`, `{row['method']}` uses `{row['do_not_start_rule']}` and reports loop overrun rate "
                f"{row['loop_overrun_rate_down']:.4f}, E2E overrun rate {row['e2e_overrun_rate_down']:.4f}, "
                f"and p99 latency {row['p99_latency_ms_down']:.3f} ms."
            )
    lines.append("This paragraph should be used to explicitly separate the theorem-backed strict rule from the relaxed diagnostic variant.")
    return "\n\n".join(lines) + "\n"


def figure_caption_scaffold(fig_dir: Path) -> str:
    figs = sorted(fig_dir.glob("*.png"))
    lines = ["## Figure interpretation scaffold", ""]
    for fig in figs:
        name = fig.stem
        if name.startswith("latency_cdf"):
            interp = "This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets."
        elif name.startswith("overrun_cdf"):
            interp = "This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance."
        elif name.startswith("allocation_share"):
            interp = "This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute."
        elif name.startswith("final_return"):
            interp = "This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks."
        else:
            interp = "Add a task-specific interpretation before manuscript submission."
        lines.append(f"- `{fig.name}`: {interp}")
    return "\n".join(lines) + "\n"


def claim_boundary_text() -> str:
    return """## Claim-boundary paragraph for manuscript

The local experiments are self-contained validation tasks designed to verify scheduler implementation, metadata completeness, matched-budget accounting, strict-versus-relaxed timing behavior, and ablation plumbing. They should not be presented as evidence of general performance across established Game AI benchmarks. Broad empirical claims require the same harness to be connected to recognized benchmarks such as GVGAI, MicroRTS, Procgen, or OpenSpiel, with the same environment-disclosure and matched-budget logging fields used here.
"""


def environment_appendix(meta_path: Path) -> str:
    if not meta_path.exists():
        return "Environment metadata file not found."
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    lines = ["## Environment-disclosure appendix draft", ""]
    for task, item in meta.get("tasks", {}).items():
        lines.append(f"### {task}")
        for key in ["environment_name", "environment_version", "benchmark_family", "observation_definition", "action_definition", "reward_definition", "episode_termination", "opponent_policy", "stochasticity_sources", "rollout_horizon_H", "number_of_rollouts_K", "B_tau_ms", "delta_min_ms", "delta_max_ms", "guard_margin_ms", "scheduler_ema_lambda", "timing_mode", "operating_system", "runtime", "library_versions"]:
            lines.append(f"- **{key}:** {item.get(key)}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--table-dir", default="paper/revised/tables")
    parser.add_argument("--fig-dir", default="paper/revised/figures")
    parser.add_argument("--log-dir", default="logs/full_validation")
    parser.add_argument("--out-dir", default="paper/revised/manuscript_assets")
    args = parser.parse_args()
    table_dir = ROOT / args.table_dir
    fig_dir = ROOT / args.fig_dir
    log_dir = ROOT / args.log_dir
    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    main_df = load_csv(table_dir, "table_main_results.csv")
    strict_df = load_csv(table_dir, "table_strict_vs_relaxed.csv")
    parts = [
        "# Manuscript Assets Generated from Local Validation Logs\n",
        claim_boundary_text(),
        environment_appendix(log_dir / "environment_metadata.json"),
        main_results_text(main_df),
        strict_relaxed_text(strict_df),
        figure_caption_scaffold(fig_dir),
    ]
    out = out_dir / "MANUSCRIPT_INSERTS.md"
    out.write_text("\n\n".join(parts), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
