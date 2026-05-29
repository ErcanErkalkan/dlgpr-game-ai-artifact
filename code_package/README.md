# DLGPR: Compute-Budgeted GA-PSO-RL Scheduler for Real-Time Game AI

This repository is a from-scratch, reproducible code package for manuscript ToG-2026-0045 revision work.
It implements a matched-budget experimental framework for a Dynamic Layered GA-PSO-RL (DLGPR) scheduler under per-interval compute budgets. The current release adds robust DLGPR variants that score atomic candidates on the disclosed evaluation-rollout set rather than on a smaller two-seed proxy.

The package is intentionally self-contained: it includes lightweight game-like environments, GA/PSO/RL modules, strict and relaxed budget enforcement, scheduler baselines, ablations, metadata templates, interval logs, result tables, figures, and tests.

## Why this package exists

The reviewer decision highlighted several critical issues:

- missing environment/task metadata,
- pilot results that could not be interpreted without environment information,
- unclear strict-vs-relaxed timing behavior,
- insufficient scheduler baselines and ablations,
- unclear metric definitions,
- weak reproducibility artifacts.

This package addresses those issues by forcing every experiment to emit environment disclosure metadata and matched-budget logs. Version 0.5.0 adds robust candidate acceptance (`robust-DLGPR`) and a near-elite transfer-gated robustness ablation (`robust-near-elite-DLGPR`).

## Quick start

```bash
python -m tests.run_tests
python scripts/run_full_validation.py --quick
python scripts/analyze_results.py
```

In the release repository, the manuscript-consistent full validation logs are stored at `logs/full_validation`, with generated tables at `paper/revised/tables`.

External and raw-CPU timing artifacts are stored at:

- `../experiments/tog2026_external_gymnasium/logs/external_validation`
- `../experiments/tog2026_timing_profile/logs/timing_profile`

Generated outputs:

- `logs/full_validation/interval_logs.csv`
- `logs/full_validation/atomic_step_logs.csv`
- `logs/full_validation/environment_metadata.json`
- `paper/revised/tables/*.csv`
- `paper/revised/figures/*.png`

## Full run

```bash
python scripts/run_full_validation.py --full
python scripts/analyze_results.py
```

The full run uses more seeds and planning intervals. It is still a compact local validation harness, not a substitute for GVGAI/MicroRTS/Procgen experiments. To use external benchmarks, implement an environment factory with the same API as `dlgpr.envs`.

## External benchmark and timing runs

```bash
python scripts/run_external_validation.py --full
python scripts/analyze_results.py --log-dir ../experiments/tog2026_external_gymnasium/logs/external_validation --table-dir ../experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir ../experiments/tog2026_external_gymnasium/paper/revised/figures
python scripts/run_timing_profile.py --full
python scripts/analyze_results.py --log-dir ../experiments/tog2026_timing_profile/logs/timing_profile --table-dir ../experiments/tog2026_timing_profile/paper/revised/tables --fig-dir ../experiments/tog2026_timing_profile/paper/revised/figures
```

The external run covers Gymnasium FrozenLake, deterministic FrozenLake, CliffWalking, and Blackjack. The optional MiniGrid adapter is available via `--include-minigrid`; it is included in the raw-CPU timing profile but not in the default external performance run because the simple linear policy is not a strong MiniGrid controller.

To audit the manuscript-consistent release artifacts from this directory:

```bash
python scripts/audit_package.py --log-dir logs/full_validation --table-dir paper/revised/tables
```

## Core design

Each planning interval has a gross budget `B_tau_ms` and a loop budget `allowed_ms = B_tau_ms - guard_margin_ms`.
Atomic steps are charged using a measured/simulated duration and logged. The strict variant stops when `remaining_budget < delta_max_ms`; the relaxed variant stops when `remaining_budget < delta_min_ms`.

Implemented methods:

- robust-DLGPR
- robust-near-elite-DLGPR
- DLGPR full
- GA-only
- PSO-only
- RL-only
- fixed split GA-PSO-RL
- round-robin scheduler
- greedy improvement-per-ms scheduler
- no-diversity ablation
- no-learning-progress ablation
- no-UCB ablation
- no-non-starvation ablation
- no-handshake ablation
- strict do-not-start variant
- relaxed do-not-start variant

The robust variants use `atomic_eval_rollouts = K` for candidate scoring. The standard DLGPR and baseline methods keep the lighter two-rollout atomic proxy, so tables must disclose `atomic_eval_rollouts` whenever robust and non-robust methods are compared.

## What was added in version 0.5.0

- Added `robust-DLGPR`, which evaluates atomic GA/PSO/RL candidates on the disclosed rollout count `K` before scheduler updates.
- Added `robust-near-elite-DLGPR`, a sensitivity variant that combines robust candidate scoring with near-elite transfer gating.
- Added `atomic_eval_rollouts` to interval logs and metric definitions.
- Added `table_aggregate_vs_dlgpr.csv` for paired aggregate diagnostics across tasks and seeds.

## Citation of generated evidence in a manuscript

Use generated results only after checking:

1. every environment metadata field is complete,
2. all baselines use the same budget and seed schedules,
3. metrics are defined in the metadata file,
4. strict and relaxed timing are reported separately,
5. performance claims are supported by statistical summaries.

## What was added in version 0.4.0

- Added Gymnasium external benchmark tasks: FrozenLake slippery, FrozenLake deterministic, CliffWalking, and Blackjack.
- Added a MiniGrid Empty-5x5 adapter for compatibility and raw-CPU timing diagnostics.
- Added `actual_cpu_raw` timing mode and raw-CPU timing-profile script.
- Added Holm-Bonferroni adjusted p-values to the statistical table.
- Added `table_timing_profile.csv` and clearer separation between charged-time validation and measured CPU profiling.

## What was added in version 0.3.0

- Added a third self-contained RTS-inspired micro-domain: `resource-defense`.
- Updated quick/full validation to run three diverse local tasks.
- Added manuscript-asset generation via `python scripts/make_manuscript_assets.py`.
- Added `Makefile` and `Dockerfile` for reproducible local execution.
- Added manuscript-ready limitation language and figure/table interpretation scaffold.

## What was added in version 0.2.0

- Real executable cross-layer handoff: RL candidates can be injected into GA/PSO memories, and GA/PSO candidates can distill the RL parameter vector.
- `no-handshake` is now a true ablation rather than a placeholder.
- Interval logs now separate charged-time accounting from actual Python CPU runtime.
- The package now includes a reviewer-facing audit script: `python scripts/audit_package.py`.
- Additional manuscript tables are generated: scheduler baselines, metric definitions, and claim-boundary tables.
- Optional external benchmark adapter scaffolding is provided in `dlgpr/external_adapters.py`.

## Important claim boundary

The local tasks (`line-duel`, `grid-treasure`, `resource-defense`) are self-contained validation environments. They solve the metadata and reproducibility problem, but they do not replace recognized Game AI benchmarks such as GVGAI, MicroRTS, or Procgen. Use the local results as implementation and scheduler-diagnostic evidence unless external benchmark adapters are added and run.
