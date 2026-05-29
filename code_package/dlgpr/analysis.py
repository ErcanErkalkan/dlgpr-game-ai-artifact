"""Result aggregation and figure generation."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .metrics import mean_std_ci, paired_sign_test_p_value, paired_wilcoxon_p_value, cliffs_delta, holm_bonferroni


def _last_per_run(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values("interval").groupby(["task_name", "method", "seed"], as_index=False).tail(1)


def summarize_main(df: pd.DataFrame) -> pd.DataFrame:
    final = _last_per_run(df)
    rows = []
    for (task, method), g in final.groupby(["task_name", "method"]):
        ret_mean, ret_std, ret_ci = mean_std_ci(g["return"])
        score_mean, score_std, score_ci = mean_std_ci(g["score"])
        st = np.where(g["steps_to_threshold"] < 0, np.nan, g["steps_to_threshold"])
        steps_to_t = float(np.nanmean(st)) if np.isfinite(st).any() else np.nan
        subset = df[(df.task_name == task) & (df.method == method)]
        is_raw_timing = bool("timing_mode" in subset and subset["timing_mode"].eq("actual_cpu_raw").all())
        rows.append({
            "task_name": task,
            "method": method,
            "return_mean_up": ret_mean,
            "return_std": ret_std,
            "return_median_up": float(np.median(g["return"])),
            "return_ci95": ret_ci,
            "score_mean_up": score_mean,
            "score_std": score_std,
            "score_median_up": float(np.median(g["score"])),
            "score_ci95": score_ci,
            "win_rate_up": float(np.mean(g["win"])),
            "steps_to_T_down": steps_to_t,
            "p95_latency_ms_down": float(np.percentile(subset["e2e_time_ms"], 95)),
            "p99_latency_ms_down": float(np.percentile(subset["e2e_time_ms"], 99)),
            "max_latency_ms_down": float(np.max(subset["e2e_time_ms"])),
            "loop_overrun_rate_down": float(np.mean(subset["loop_overrun"].astype(bool))),
            "e2e_overrun_rate_down": float(np.mean(subset["e2e_overrun"].astype(bool))),
            "actual_cpu_e2e_p95_ms_down": float(np.percentile(subset["actual_cpu_e2e_ms"], 95)) if is_raw_timing and "actual_cpu_e2e_ms" in subset else np.nan,
            "actual_cpu_e2e_p99_ms_down": float(np.percentile(subset["actual_cpu_e2e_ms"], 99)) if is_raw_timing and "actual_cpu_e2e_ms" in subset else np.nan,
            "actual_cpu_e2e_max_ms_down": float(np.max(subset["actual_cpu_e2e_ms"])) if is_raw_timing and "actual_cpu_e2e_ms" in subset else np.nan,
            "actual_cpu_e2e_overrun_rate_down": float(np.mean(subset["actual_cpu_e2e_overrun"].astype(bool))) if is_raw_timing and "actual_cpu_e2e_overrun" in subset else np.nan,
        })
    return pd.DataFrame(rows)


def summarize_strict_relaxed(df: pd.DataFrame) -> pd.DataFrame:
    subset = df[df["method"].isin(["strict-delta-max", "relaxed-delta-min"])]
    rows = []
    for (task, method, rule), g in subset.groupby(["task_name", "method", "do_not_start_rule"]):
        is_raw_timing = bool("timing_mode" in g and g["timing_mode"].eq("actual_cpu_raw").all())
        rows.append({
            "task_name": task,
            "method": method,
            "do_not_start_rule": rule,
            "loop_overrun_rate_down": float(np.mean(g["loop_overrun"].astype(bool))),
            "e2e_overrun_rate_down": float(np.mean(g["e2e_overrun"].astype(bool))),
            "p95_latency_ms_down": float(np.percentile(g["e2e_time_ms"], 95)),
            "p99_latency_ms_down": float(np.percentile(g["e2e_time_ms"], 99)),
            "max_overrun_ms_down": float(max(g["loop_overrun_ms"].max(), g["e2e_overrun_ms"].max())),
            "unused_budget_ms_context": float(np.mean(np.maximum(0.0, g["allowed_ms"] - g["loop_time_ms"]))),
            "actual_cpu_e2e_p99_ms_down": float(np.percentile(g["actual_cpu_e2e_ms"], 99)) if is_raw_timing and "actual_cpu_e2e_ms" in g else np.nan,
            "actual_cpu_e2e_overrun_rate_down": float(np.mean(g["actual_cpu_e2e_overrun"].astype(bool))) if is_raw_timing and "actual_cpu_e2e_overrun" in g else np.nan,
            "return_mean_up": float(g.groupby("seed")["return"].last().mean()),
        })
    return pd.DataFrame(rows)


def summarize_ablation(df: pd.DataFrame) -> pd.DataFrame:
    final = _last_per_run(df)
    variants = ["DLGPR-full", "no-diversity", "no-learning-progress", "no-ucb", "no-non-starvation", "no-handshake"]
    final = final[final["method"].isin(variants)]
    rows = []
    for task, gtask in final.groupby("task_name"):
        full = gtask[gtask.method == "DLGPR-full"].sort_values("seed")
        full_mean = float(full["return"].mean()) if len(full) else np.nan
        for method, g in gtask.groupby("method"):
            g = g.sort_values("seed")
            variant_mean = float(g["return"].mean())
            delta = float(variant_mean - full_mean) if np.isfinite(full_mean) else np.nan
            if method == "DLGPR-full":
                interpretation = "full model reference"
            elif delta > 0:
                interpretation = "variant mean return is higher than DLGPR-full in this local run"
            elif delta < 0:
                interpretation = "DLGPR-full mean return is higher than this variant in this local run"
            else:
                interpretation = "no observed mean-return difference from DLGPR-full in this local run"
            rows.append({
                "task_name": task,
                "variant": method,
                "return_mean_up": variant_mean,
                "return_std": float(g["return"].std(ddof=1)) if len(g) > 1 else 0.0,
                "return_median_up": float(g["return"].median()),
                "return_ci95": float(1.96 * g["return"].std(ddof=1) / np.sqrt(len(g))) if len(g) > 1 else 0.0,
                "delta_return_vs_full": delta,
                "win_rate_up": float(g["win"].mean()),
                "p99_latency_ms_down": float(np.percentile(df[(df.task_name == task) & (df.method == method)]["e2e_time_ms"], 99)),
                "interpretation": interpretation,
            })
    return pd.DataFrame(rows)


def statistical_tests(df: pd.DataFrame) -> pd.DataFrame:
    final = _last_per_run(df)
    rows = []
    for task, gtask in final.groupby("task_name"):
        full = gtask[gtask.method == "DLGPR-full"].sort_values("seed")
        if full.empty:
            continue
        for method, comp in gtask.groupby("method"):
            if method == "DLGPR-full":
                continue
            comp = comp.sort_values("seed")
            merged = pd.merge(full[["seed", "return"]], comp[["seed", "return"]], on="seed", suffixes=("_full", "_comp"))
            p_value, test_name = paired_wilcoxon_p_value(merged["return_full"], merged["return_comp"])
            comp_lat = df[(df.task_name == task) & (df.method == method)]
            rows.append({
                "task_name": task,
                "comparator": method,
                "metric": "return",
                "DLGPR_mean": float(merged["return_full"].mean()),
                "DLGPR_std": float(merged["return_full"].std(ddof=1)) if len(merged) > 1 else 0.0,
                "DLGPR_median": float(merged["return_full"].median()),
                "DLGPR_ci95": float(1.96 * merged["return_full"].std(ddof=1) / np.sqrt(len(merged))) if len(merged) > 1 else 0.0,
                "comparator_mean": float(merged["return_comp"].mean()),
                "comparator_std": float(merged["return_comp"].std(ddof=1)) if len(merged) > 1 else 0.0,
                "comparator_median": float(merged["return_comp"].median()),
                "comparator_ci95": float(1.96 * merged["return_comp"].std(ddof=1) / np.sqrt(len(merged))) if len(merged) > 1 else 0.0,
                "test": test_name,
                "p_value": p_value,
                "effect_size_cliffs_delta": cliffs_delta(merged["return_full"], merged["return_comp"]),
                "p95_latency_ms_down": float(np.percentile(comp_lat["e2e_time_ms"], 95)),
                "p99_latency_ms_down": float(np.percentile(comp_lat["e2e_time_ms"], 99)),
                "max_latency_ms_down": float(comp_lat["e2e_time_ms"].max()),
                "loop_overrun_rate_down": float(np.mean(comp_lat["loop_overrun"].astype(bool))),
                "e2e_overrun_rate_down": float(np.mean(comp_lat["e2e_overrun"].astype(bool))),
                "n_pairs": len(merged),
                "conclusion": "interpret with Holm-adjusted p-values and effect sizes; do not use raw p-values alone",
            })
    out = pd.DataFrame(rows)
    if not out.empty:
        out["p_value_holm"] = holm_bonferroni(out["p_value"])
        out["significant_holm_0_05"] = out["p_value_holm"] < 0.05
    return out


def summarize_timing_profile(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    group_cols = ["benchmark", "task_name", "method", "timing_mode", "do_not_start_rule"]
    for keys, g in df.groupby(group_cols):
        benchmark, task, method, timing_mode, rule = keys
        rows.append({
            "benchmark": benchmark,
            "task_name": task,
            "method": method,
            "timing_mode": timing_mode,
            "do_not_start_rule": rule,
            "charged_e2e_p95_ms_down": float(np.percentile(g["e2e_time_ms"], 95)),
            "charged_e2e_p99_ms_down": float(np.percentile(g["e2e_time_ms"], 99)),
            "charged_e2e_max_ms_down": float(g["e2e_time_ms"].max()),
            "charged_loop_overrun_rate_down": float(np.mean(g["loop_overrun"].astype(bool))),
            "charged_e2e_overrun_rate_down": float(np.mean(g["e2e_overrun"].astype(bool))),
            "actual_cpu_loop_p95_ms_down": float(np.percentile(g["actual_cpu_loop_wall_ms"], 95)) if "actual_cpu_loop_wall_ms" in g else np.nan,
            "actual_cpu_e2e_p95_ms_down": float(np.percentile(g["actual_cpu_e2e_ms"], 95)) if "actual_cpu_e2e_ms" in g else np.nan,
            "actual_cpu_e2e_p99_ms_down": float(np.percentile(g["actual_cpu_e2e_ms"], 99)) if "actual_cpu_e2e_ms" in g else np.nan,
            "actual_cpu_e2e_max_ms_down": float(g["actual_cpu_e2e_ms"].max()) if "actual_cpu_e2e_ms" in g else np.nan,
            "actual_cpu_loop_overrun_rate_down": float(np.mean(g["actual_cpu_loop_overrun"].astype(bool))) if "actual_cpu_loop_overrun" in g else np.nan,
            "actual_cpu_e2e_overrun_rate_down": float(np.mean(g["actual_cpu_e2e_overrun"].astype(bool))) if "actual_cpu_e2e_overrun" in g else np.nan,
            "mean_unused_charged_loop_budget_ms_context": float(np.mean(np.maximum(0.0, g["allowed_ms"] - g["loop_time_ms"]))),
            "intervals": int(len(g)),
        })
    return pd.DataFrame(rows)


def write_environment_table(metadata_path: Path, out_path: Path) -> pd.DataFrame:
    meta = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    rows = []
    for task, m in meta.get("tasks", {}).items():
        rows.append({
            "benchmark": m.get("benchmark_family"),
            "task_name": task,
            "environment_name": m.get("environment_name"),
            "version": m.get("environment_version"),
            "observation": m.get("observation_definition"),
            "preprocessing": m.get("observation_preprocessing"),
            "action": m.get("action_definition"),
            "action_space": f"{m.get('action_space_type')} / {m.get('action_space_size')}",
            "reward": m.get("reward_definition"),
            "termination": m.get("episode_termination"),
            "opponent": m.get("opponent_policy"),
            "stochasticity": m.get("stochasticity_sources"),
            "evaluation_cadence": m.get("evaluation_cadence"),
            "K": m.get("number_of_rollouts_K"),
            "H": m.get("rollout_horizon_H"),
            "threshold_T": m.get("performance_threshold_T"),
            "B_tau_ms": m.get("B_tau_ms"),
            "allowed_ms": m.get("allowed_ms"),
            "delta_min_ms": m.get("delta_min_ms"),
            "delta_max_ms": m.get("delta_max_ms"),
            "guard_margin_ms": m.get("guard_margin_ms"),
            "scheduler_ema_lambda": m.get("scheduler_ema_lambda"),
            "timing_mode": m.get("timing_mode"),
            "hardware_id": m.get("hardware_id"),
            "OS": m.get("operating_system"),
            "runtime": m.get("runtime") or f"Python {m.get('python_version')}",
            "library_versions": json.dumps(m.get("library_versions", {}), sort_keys=True),
        })
    table = pd.DataFrame(rows)
    table.to_csv(out_path, index=False)
    return table


def summarize_scheduler_baselines(df: pd.DataFrame) -> pd.DataFrame:
    """Compare the full scheduler against fixed/round-robin/greedy alternatives."""
    methods = ["robust-DLGPR", "robust-near-elite-DLGPR", "DLGPR-full", "fixed-split", "round-robin", "greedy-improvement"]
    final = _last_per_run(df[df["method"].isin(methods)])
    rows = []
    for (task, method), g in final.groupby(["task_name", "method"]):
        lat = df[(df.task_name == task) & (df.method == method)]
        rows.append({
            "task_name": task,
            "scheduler": method,
            "return_mean_up": float(g["return"].mean()),
            "return_std": float(g["return"].std(ddof=1)) if len(g) > 1 else 0.0,
            "return_median_up": float(g["return"].median()),
            "return_ci95": float(1.96 * g["return"].std(ddof=1) / np.sqrt(len(g))) if len(g) > 1 else 0.0,
            "win_rate_up": float(g["win"].mean()),
            "p99_latency_ms_down": float(np.percentile(lat["e2e_time_ms"], 99)),
            "loop_overrun_rate_down": float(np.mean(lat["loop_overrun"].astype(bool))),
            "mean_unused_loop_budget_ms_context": float(np.mean(np.maximum(0.0, lat["allowed_ms"] - lat["loop_time_ms"]))),
            "handshake_events_total": int(lat.get("handshake_events", pd.Series([0])).sum()),
        })
    return pd.DataFrame(rows)


def summarize_aggregate_vs_dlgpr(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate paired differences against DLGPR-full across tasks and seeds."""
    final = _last_per_run(df)
    rows = []
    for method in sorted(m for m in final["method"].unique() if m != "DLGPR-full"):
        diffs = []
        task_wins = 0
        task_losses = 0
        task_ties = 0
        for task, gtask in final.groupby("task_name"):
            base = gtask[gtask.method == "DLGPR-full"][["seed", "return"]].rename(columns={"return": "base_return"})
            comp = gtask[gtask.method == method][["seed", "return"]].rename(columns={"return": "comp_return"})
            merged = pd.merge(base, comp, on="seed")
            if merged.empty:
                continue
            diff = merged["comp_return"] - merged["base_return"]
            diffs.extend(diff.tolist())
            mean_diff = float(diff.mean())
            if mean_diff > 1e-12:
                task_wins += 1
            elif mean_diff < -1e-12:
                task_losses += 1
            else:
                task_ties += 1
        if not diffs:
            continue
        arr = np.asarray(diffs, dtype=np.float64)
        rows.append({
            "comparator": method,
            "paired_mean_return_delta_vs_DLGPR": float(np.mean(arr)),
            "paired_median_return_delta_vs_DLGPR": float(np.median(arr)),
            "paired_wins_up": int(np.sum(arr > 0)),
            "paired_losses_down": int(np.sum(arr < 0)),
            "paired_ties": int(np.sum(arr == 0)),
            "tasks_with_positive_mean_delta_up": task_wins,
            "tasks_with_negative_mean_delta_down": task_losses,
            "tasks_with_zero_mean_delta": task_ties,
            "n_pairs": int(arr.size),
            "interpretation": "Aggregate diagnostic; confirm per-task tables and Holm-adjusted paired tests before claiming superiority.",
        })
    return pd.DataFrame(rows)


def metric_definitions() -> pd.DataFrame:
    return pd.DataFrame([
        {"metric": "return", "direction": "higher is better", "definition": "Mean episode return under the disclosed evaluation seed schedule."},
        {"metric": "score", "direction": "higher is better", "definition": "Task score; in the self-contained harness it is equal to episode return."},
        {"metric": "win_rate", "direction": "higher is better", "definition": "Fraction of evaluation episodes ending in a task win."},
        {"metric": "steps_to_T", "direction": "lower is better", "definition": "First interval where mean score reaches threshold T, converted by the environment-step cap; -1/blank means not reached."},
        {"metric": "p95_latency_ms", "direction": "lower is better", "definition": "95th percentile of per-interval end-to-end charged time."},
        {"metric": "p99_latency_ms", "direction": "lower is better", "definition": "99th percentile of per-interval end-to-end charged time."},
        {"metric": "loop_overrun_rate", "direction": "lower is better", "definition": "Fraction of intervals where charged loop time exceeds the disclosed loop budget."},
        {"metric": "e2e_overrun_rate", "direction": "lower is better", "definition": "Fraction of intervals where charged loop time plus guard margin exceeds the gross interval budget."},
        {"metric": "handshake_events", "direction": "diagnostic", "definition": "Number of executed cross-layer injection/distillation operations."},
        {"metric": "actual_cpu_loop_wall_ms", "direction": "diagnostic; lower is better for deployment", "definition": "Measured wall-clock duration of the budget-critical atomic-step loop, excluding offline evaluation/logging."},
        {"metric": "actual_cpu_e2e_ms", "direction": "diagnostic; lower is better for deployment", "definition": "Measured budget-critical atomic loop plus the disclosed guard margin; separate from simulated charged-time accounting."},
        {"metric": "wall_clock_interval_ms", "direction": "diagnostic", "definition": "Measured script-level interval duration including offline evaluation and logging; not used as the real-time engine budget metric."},
        {"metric": "p_value_holm", "direction": "lower is stronger evidence", "definition": "Holm-Bonferroni adjusted paired-test p-value across the reported comparator family."},
        {"metric": "atomic_eval_rollouts", "direction": "context", "definition": "Number of evaluation seeds used inside each atomic candidate-scoring step; robust variants set this to K."},
    ])


def package_claim_limits(df: pd.DataFrame | None = None) -> pd.DataFrame:
    has_external = False
    if df is not None and "benchmark" in df.columns:
        has_external = bool(df["benchmark"].astype(str).str.contains("gymnasium|external|procgen|microrts|gvgai|open_spiel", case=False, regex=True).any())
    return pd.DataFrame([
        {"item": "Self-contained environments", "status": "included", "manuscript_use": "Use for reproducibility and sanity-check evidence; do not claim GVGAI/MicroRTS/Procgen generalization."},
        {"item": "Charged-time accounting", "status": "included", "manuscript_use": "Can support budget-accounting diagnostics when timing_mode is disclosed."},
        {"item": "Actual external benchmark evidence", "status": "included" if has_external else "not included", "manuscript_use": "Use only for the named external benchmarks that were actually logged; do not generalize to GVGAI/MicroRTS/Procgen unless those logs exist."},
        {"item": "Cross-layer handoff", "status": "implemented", "manuscript_use": "Compare DLGPR-full with no-handshake ablation."},
    ])


def make_figures(df: pd.DataFrame, fig_dir: Path) -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)
    # 1. Latency CDF per method for each task.
    for task, gt in df.groupby("task_name"):
        plt.figure(figsize=(8, 5))
        for method, gm in gt.groupby("method"):
            vals = np.sort(gm["e2e_time_ms"].to_numpy(dtype=float))
            y = np.linspace(0, 1, len(vals), endpoint=True)
            plt.plot(vals, y, label=method)
        plt.xlabel("Per-interval E2E time (ms)")
        plt.ylabel("Empirical CDF")
        plt.title(f"Latency CDF: {task}")
        plt.legend(fontsize=7)
        plt.tight_layout()
        plt.savefig(fig_dir / f"latency_cdf_{task}.png", dpi=160)
        plt.close()

        plt.figure(figsize=(8, 5))
        for method, gm in gt.groupby("method"):
            vals = np.sort(gm["loop_overrun_ms"].to_numpy(dtype=float))
            y = np.linspace(0, 1, len(vals), endpoint=True)
            plt.plot(vals, y, label=method)
        plt.xlabel("Loop-budget overrun magnitude (ms)")
        plt.ylabel("Empirical CDF")
        plt.title(f"Loop overrun CDF: {task}")
        plt.legend(fontsize=7)
        plt.tight_layout()
        plt.savefig(fig_dir / f"overrun_cdf_{task}.png", dpi=160)
        plt.close()

    # 2. Allocation traces for DLGPR-full.
    for task, gt in df[df.method == "DLGPR-full"].groupby("task_name"):
        alloc = gt.groupby("interval")[["num_ga_steps", "num_pso_steps", "num_rl_steps"]].mean()
        denom = alloc.sum(axis=1).replace(0, np.nan)
        share = alloc.divide(denom, axis=0).fillna(0)
        plt.figure(figsize=(8, 5))
        for col in share.columns:
            plt.plot(share.index, share[col], label=col.replace("num_", "").replace("_steps", "").upper())
        plt.xlabel("Planning interval")
        plt.ylabel("Mean allocation share")
        plt.title(f"DLGPR allocation share: {task}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(fig_dir / f"allocation_share_{task}.png", dpi=160)
        plt.close()

    # 3. Final return bar chart.
    final = _last_per_run(df)
    for task, gt in final.groupby("task_name"):
        means = gt.groupby("method")["return"].mean().sort_values(ascending=False)
        plt.figure(figsize=(9, 5))
        plt.bar(range(len(means)), means.values)
        plt.xticks(range(len(means)), means.index, rotation=45, ha="right")
        plt.ylabel("Final mean return (higher is better)")
        plt.title(f"Final return by method: {task}")
        plt.tight_layout()
        plt.savefig(fig_dir / f"final_return_{task}.png", dpi=160)
        plt.close()


def analyze(log_dir: Path, table_dir: Path, fig_dir: Path) -> Dict[str, Path]:
    table_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(log_dir / "interval_logs.csv")
    outputs = {}
    env_table = write_environment_table(log_dir / "environment_metadata.json", table_dir / "table_environment_metadata.csv")
    outputs["environment"] = table_dir / "table_environment_metadata.csv"
    main = summarize_main(df)
    main.to_csv(table_dir / "table_main_results.csv", index=False)
    outputs["main"] = table_dir / "table_main_results.csv"
    strict = summarize_strict_relaxed(df)
    strict.to_csv(table_dir / "table_strict_vs_relaxed.csv", index=False)
    outputs["strict_relaxed"] = table_dir / "table_strict_vs_relaxed.csv"
    ablation = summarize_ablation(df)
    ablation.to_csv(table_dir / "table_ablation.csv", index=False)
    outputs["ablation"] = table_dir / "table_ablation.csv"
    sched = summarize_scheduler_baselines(df)
    sched.to_csv(table_dir / "table_scheduler_baselines.csv", index=False)
    outputs["scheduler_baselines"] = table_dir / "table_scheduler_baselines.csv"
    aggregate = summarize_aggregate_vs_dlgpr(df)
    aggregate.to_csv(table_dir / "table_aggregate_vs_dlgpr.csv", index=False)
    outputs["aggregate_vs_dlgpr"] = table_dir / "table_aggregate_vs_dlgpr.csv"
    metrics = metric_definitions()
    metrics.to_csv(table_dir / "table_metric_definitions.csv", index=False)
    outputs["metric_definitions"] = table_dir / "table_metric_definitions.csv"
    limits = package_claim_limits(df)
    limits.to_csv(table_dir / "table_claim_limits.csv", index=False)
    outputs["claim_limits"] = table_dir / "table_claim_limits.csv"
    stats = statistical_tests(df)
    stats.to_csv(table_dir / "table_statistical_tests.csv", index=False)
    outputs["stats"] = table_dir / "table_statistical_tests.csv"
    timing = summarize_timing_profile(df)
    timing.to_csv(table_dir / "table_timing_profile.csv", index=False)
    outputs["timing_profile"] = table_dir / "table_timing_profile.csv"
    make_figures(df, fig_dir)
    return outputs
