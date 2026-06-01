# DLGPR Game AI Artifact

**Release version:** `v0.6.0`

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20447918.svg)](https://doi.org/10.5281/zenodo.20447918)
[![Repository](https://img.shields.io/badge/GitHub-dlgpr--game--ai--artifact-blue?logo=github)](https://github.com/ErcanErkalkan/dlgpr-game-ai-artifact/tree/v0.6.0)

This repository contains the code, reproducibility scripts, metadata-complete logs, statistical tables, and generated figures for the DLGPR Game AI validation artifact.

The manuscript source and manuscript PDF are intentionally excluded. The public artifact is meant to accompany the manuscript, not to publish the journal submission files.

The `experiments/tog2026_*` directory names are retained as stable historical
paths so that the generated tables, audit scripts, and archived logs remain
addressable. They do not identify the current target journal.

## Contents

- `code_package/`: official source-layout directory containing the importable `dlgpr` package, tests, analysis scripts, package documentation, configs, generated code-package logs, and generated code-package figures/tables. The root `pyproject.toml` uses `package-dir = {"" = "code_package"}` and `where = ["code_package"]`.
- `experiments/tog2026_full_validation/`: the full local validation used by the manuscript, including 19,200 interval-log rows, 150,297 atomic-step rows, 16 logged scheduler labels, task metadata, generated tables, and generated figures. Two logged label pairs are behaviorally equivalent diagnostics rather than independent methods.
- `experiments/tog2026_external_gymnasium/`: a matched-budget robust external benchmark extension on Gymnasium tasks, including 3,840 interval-log rows, 29,698 atomic-step rows, and 8 logged scheduler labels. The `fixed-split` / `round-robin` pair is an equivalent static-allocation diagnostic in the reported configuration.
- `experiments/tog2026_timing_profile/`: raw-CPU timing diagnostics for strict and relaxed do-not-start rules, including 1,500 interval-log rows and 16,158 atomic-step rows.
- `experiments/ec2026_compute_matched_rollout/`: rollout-equivalent compute-matched local performance comparison, including 9,600 interval-log rows and 134,027 atomic-step rows. Evaluation, RL-training, and RL-to-population injection rollouts are charged to the online scheduler account.
- `experiments/ec2026_minigrid_performance/`: rollout-equivalent performance validation on the recognized MiniGrid `Empty-5x5` task, including 960 interval-log rows and 13,543 atomic-step rows. This is a bounded fully observable adapter experiment, not a broad MiniGrid-suite claim.

Generated directories named `paper/revised` contain artifact tables, figures, and manuscript-insert snippets. They are not the manuscript source and do not contain the excluded `Paper/` submission directory.

## Official package layout

This release intentionally uses **Seçenek B / `code_package` layout** rather than moving source files to the repository root. The root contains project metadata and runner files, while importable source code remains under `code_package/dlgpr`.

```text
dlgpr-game-ai-artifact/
  README.md
  pyproject.toml
  requirements.txt
  Dockerfile
  Makefile
  code_package/
    dlgpr/
    tests/
    scripts/
    docs/
    configs/
```

The root `pyproject.toml` therefore declares:

```toml
[tool.setuptools]
package-dir = {"" = "code_package"}

[tool.setuptools.packages.find]
where = ["code_package"]
include = ["dlgpr*"]
```

Root-relative commands are the official interface. Do not call `scripts/...` or `tests/...` as if those directories existed at the repository root; use `code_package/scripts/...` and `code_package/tests/...`.

## Validation

From the root directory, install the package in editable mode and then run the official audit entry point:

```bash
python -m pip install -e .
python code_package/scripts/audit_package.py
```

To regenerate all release audit reports from the current files, run:

```bash
python -m pip install -e .
python code_package/tests/run_tests.py
python code_package/scripts/audit_package.py --profile full --out experiments/tog2026_full_validation/PACKAGE_AUDIT_REPORT.md
python code_package/scripts/audit_package.py --profile external --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --out experiments/tog2026_external_gymnasium/PACKAGE_AUDIT_REPORT.md
python code_package/scripts/audit_package.py --profile timing --log-dir experiments/tog2026_timing_profile/logs/timing_profile --table-dir experiments/tog2026_timing_profile/paper/revised/tables --out experiments/tog2026_timing_profile/PACKAGE_AUDIT_REPORT.md
python code_package/scripts/audit_package.py --profile compute-matched --log-dir experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout --table-dir experiments/ec2026_compute_matched_rollout/paper/revised/tables --out experiments/ec2026_compute_matched_rollout/PACKAGE_AUDIT_REPORT.md
python code_package/scripts/audit_package.py --profile minigrid-performance --log-dir experiments/ec2026_minigrid_performance/logs/minigrid_performance --table-dir experiments/ec2026_minigrid_performance/paper/revised/tables --out experiments/ec2026_minigrid_performance/PACKAGE_AUDIT_REPORT.md
```

Equivalently:

```bash
make install
make audit
```

Expected status:

- 17 tests pass.
- The official experiment directories now contain the robust source-of-truth logs; see `experiments/LOG_REPLACEMENT_AUDIT.md`.
- Strict `delta_max` timing has zero charged-time loop overruns in the full validation logs. This is a charged-time compliance statement, not a raw CPU wall-clock guarantee.


## Timing-claim boundary

This artifact deliberately separates two timing notions:

1. **Charged-time simulated budget compliance.** The main 24 ms result is a declared charged-time accounting result. In this mode, each atomic optimizer step is charged according to the disclosed timing model, and overrun rates are evaluated against the declared per-interval charged-time budget.
2. **Raw CPU wall-clock timing.** The `tog2026_timing_profile` experiment measures Python CPU timing under a separate calibrated 100 ms budget. It is a diagnostic profile for implementation behavior, not a 24 ms game-engine real-time guarantee.

Therefore, the manuscript-consistent claim is **zero strict-rule charged-time overruns under the disclosed 24 ms charged-time budget**, plus a separate raw-CPU diagnostic. Do not cite the 24 ms charged-time result as raw wall-clock performance in a deployed engine.

The release also contains a separate `rollout_normalized` performance layer. In that mode, each online evaluation rollout, RL training rollout, and RL-to-GA/PSO injection evaluation consumes one rollout-equivalent budget unit. This layer is the compute-matched basis for robust-versus-standard performance comparisons; it is not a millisecond or engine-latency claim.

## Manuscript Consistency

The manuscript reports the full local validation in `experiments/tog2026_full_validation`, not the smoke-test outputs generated by quick runs. The full validation contains:

- 3 tasks: `line-duel`, `grid-treasure`, and `resource-defense`.
- 16 logged scheduler labels, including core baselines, scheduler baselines, ablations, strict timing, relaxed timing, and the robust-DLGPR / robust-near-elite-DLGPR variants. These labels include two behaviorally equivalent diagnostic pairs: `DLGPR-full` / `strict-delta-max` and `fixed-split` / `round-robin`.
- 10 seeds and 40 planning intervals per run.
- Method-specific evaluation rollouts per interval: 2 for standard methods and 5 for the robust-DLGPR variants, as recorded in `atomic_eval_rollouts`.
- Strict `delta_max` loop and end-to-end overrun rate of 0.0 on all three tasks.
- Relaxed `delta_min` overrun rates of 0.5825 to 0.6275, matching the manuscript's 58.25--62.75% range.
- A separate Gymnasium extension reports named external benchmarks only; it uses the frozen 8-method robust external set and is not presented as GVGAI/MicroRTS/Procgen evidence.
- A separate raw-CPU timing profile uses a calibrated 100 ms interval budget and reports measured Python CPU behavior across the profiled tasks. It is diagnostic only and is not the 24 ms charged-time compliance claim.
- A separate rollout-equivalent local comparison charges online rollout work directly and reports method-specific rollout consumption. It is the appropriate comparison when robust methods use 5 evaluation rollouts and standard methods use 2.
- A separate MiniGrid `Empty-5x5` performance run uses `FullyObsWrapper`, disclosed goal-relative features, and the task-relevant `left/right/forward` action subset. It demonstrates bounded benchmark integration, not broad benchmark dominance.

The official row counts are fixed as follows:

- Full validation: 19,200 interval rows / 150,297 atomic rows / 16 logged scheduler labels. Conservative behavioral count: 14 behaviorally distinct configurations because `DLGPR-full` / `strict-delta-max` and `fixed-split` / `round-robin` are equivalent under the reported setup.
- External robust validation: 3,840 interval rows / 29,698 atomic rows / 8 methods.

## Method-equivalence disclosure

The artifact preserves 16 local scheduler labels for traceability, but it does not present all labels as independent algorithms. These pairs are behaviorally equivalent under the reported configuration:

- `DLGPR-full` and `strict-delta-max`.
- `fixed-split` and `round-robin`.

Therefore, manuscript and artifact text should use **16 logged scheduler labels with two behaviorally equivalent diagnostic pairs** or **14 behaviorally distinct local configurations**, rather than implying 16 independent algorithmic baselines.


The source-of-truth replacement is summarized in `experiments/SOURCE_OF_TRUTH.md` and `experiments/LOG_REPLACEMENT_AUDIT.md`. Method-equivalence disclosure is provided in `code_package/docs/METHOD_EQUIVALENCE.md`, `experiments/METHOD_EQUIVALENCE_AUDIT.md`, and `table_method_equivalence.csv`.

## License and Citation

The software is released under the MIT License. Citation metadata is provided in `CITATION.cff` and `.zenodo.json`.

---

# DLGPR: Charged-Time Budgeted GA-PSO-RL Scheduler for Game AI (Code Package Details)

This repository is a from-scratch, reproducible code package for the Entertainment Computing submission.
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

This package addresses those issues by forcing every experiment to emit environment disclosure metadata and matched-budget logs. Version 0.6.0 adds rollout-equivalent compute matching, paired small-sample statistics, and a bounded MiniGrid `Empty-5x5` performance integration for the Entertainment Computing submission.

## Quick start

```bash
python -m pip install -e .
python code_package/tests/run_tests.py
python code_package/scripts/run_full_validation.py --quick
python code_package/scripts/analyze_results.py --log-dir code_package/logs/full_validation --table-dir code_package/paper/revised/tables --fig-dir code_package/paper/revised/figures
```

The default package-generation commands write smoke/full local outputs under `code_package/logs/full_validation` and generated local analysis outputs under `code_package/paper/revised`.

In the release repository, the manuscript-consistent full validation logs are stored at `experiments/tog2026_full_validation/logs/full_validation`, with generated tables at `experiments/tog2026_full_validation/paper/revised/tables`.

External and raw-CPU timing artifacts are stored at:

- `experiments/tog2026_external_gymnasium/logs/external_validation`
- `experiments/tog2026_timing_profile/logs/timing_profile`
- `experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout`
- `experiments/ec2026_minigrid_performance/logs/minigrid_performance`

## Full run

```bash
python code_package/scripts/run_full_validation.py --full
python code_package/scripts/analyze_results.py --log-dir code_package/logs/full_validation --table-dir code_package/paper/revised/tables --fig-dir code_package/paper/revised/figures
```

The full run uses more seeds and planning intervals. It is still a compact local validation harness, not a substitute for GVGAI/MicroRTS/Procgen experiments. To use external benchmarks, implement an environment factory with the same API as `dlgpr.envs`.

## External benchmark and timing runs

```bash
python code_package/scripts/run_external_validation.py --full
python code_package/scripts/analyze_results.py --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir experiments/tog2026_external_gymnasium/paper/revised/figures
python code_package/scripts/run_timing_profile.py --full
python code_package/scripts/analyze_results.py --log-dir experiments/tog2026_timing_profile/logs/timing_profile --table-dir experiments/tog2026_timing_profile/paper/revised/tables --fig-dir experiments/tog2026_timing_profile/paper/revised/figures
python code_package/scripts/run_compute_matched_validation.py --full --basis rollout
python code_package/scripts/analyze_results.py --log-dir experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout --table-dir experiments/ec2026_compute_matched_rollout/paper/revised/tables --fig-dir experiments/ec2026_compute_matched_rollout/paper/revised/figures
python code_package/scripts/run_minigrid_performance.py --full
python code_package/scripts/analyze_results.py --log-dir experiments/ec2026_minigrid_performance/logs/minigrid_performance --table-dir experiments/ec2026_minigrid_performance/paper/revised/tables --fig-dir experiments/ec2026_minigrid_performance/paper/revised/figures
```

The manuscript-consistent external run covers Gymnasium FrozenLake, deterministic FrozenLake, CliffWalking, and Blackjack with the frozen 8-method robust external set: `robust-DLGPR`, `robust-near-elite-DLGPR`, `DLGPR-full`, `fixed-split`, `round-robin`, `greedy-improvement`, `no-non-starvation`, and `no-handshake`. The full default external run is therefore `4 tasks x 10 seeds x 12 intervals x 8 methods = 3,840 interval rows`; its precomputed atomic-step log has 29,698 rows. The optional MiniGrid adapter is available via `--include-minigrid`; adding MiniGrid changes the row count and is not the manuscript-consistent external performance run.

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

The robust variants use `atomic_eval_rollouts = K` for candidate scoring. The standard DLGPR and baseline methods keep the lighter two-rollout atomic proxy. Simulated charged-time tables must disclose that mismatch. Robust-versus-standard performance claims should use the separate `rollout_normalized` experiment, where consumed rollout work is charged explicitly.

## Important claim boundary

The local tasks (`line-duel`, `grid-treasure`, `resource-defense`) are self-contained validation environments. They solve the metadata and reproducibility problem, but they do not replace recognized Game AI benchmarks such as GVGAI, MicroRTS, or Procgen. Use the local results as implementation and scheduler-diagnostic evidence unless external benchmark adapters are added and run.


## Algorithm-code alignment scope

The released implementation optimizes continuous policy/controller parameter vectors. It does not claim implemented PCG, difficulty-vector, level-artifact, or environment-configuration optimization. Non-starvation is implemented as an explicit `n_min` minimum-selection safeguard, not as an additive starvation-age term in the scheduler index. The UCB-style term uses cumulative scheduler-state selection counts. Candidate exchange is implemented through module-local memories, the run-level incumbent, and explicit handoff operations rather than a single materialized global candidate pool. See `code_package/docs/ALGORITHM_CODE_ALIGNMENT.md`.
