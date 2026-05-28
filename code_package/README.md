# DLGPR: Compute-Budgeted GA-PSO-RL Scheduler for Real-Time Game AI

This repository is a from-scratch, reproducible code package for manuscript ToG-2026-0045 revision work.
It implements a matched-budget experimental framework for a Dynamic Layered GA-PSO-RL (DLGPR) scheduler under per-interval compute budgets.

The package is intentionally self-contained: it includes lightweight game-like environments, GA/PSO/RL modules, strict and relaxed budget enforcement, scheduler baselines, ablations, metadata templates, interval logs, result tables, figures, and tests.

## Why this package exists

The reviewer decision highlighted several critical issues:

- missing environment/task metadata,
- pilot results that could not be interpreted without environment information,
- unclear strict-vs-relaxed timing behavior,
- insufficient scheduler baselines and ablations,
- unclear metric definitions,
- weak reproducibility artifacts.

This package addresses those issues by forcing every experiment to emit environment disclosure metadata and matched-budget logs.

## Quick start

```bash
python -m tests.run_tests
python scripts/run_full_validation.py --quick
python scripts/analyze_results.py
```

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

## Core design

Each planning interval has a gross budget `B_tau_ms` and a loop budget `allowed_ms = B_tau_ms - guard_margin_ms`.
Atomic steps are charged using a measured/simulated duration and logged. The strict variant stops when `remaining_budget < delta_max_ms`; the relaxed variant stops when `remaining_budget < delta_min_ms`.

Implemented methods:

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

## Citation of generated evidence in a manuscript

Use generated results only after checking:

1. every environment metadata field is complete,
2. all baselines use the same budget and seed schedules,
3. metrics are defined in the metadata file,
4. strict and relaxed timing are reported separately,
5. performance claims are supported by statistical summaries.

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
