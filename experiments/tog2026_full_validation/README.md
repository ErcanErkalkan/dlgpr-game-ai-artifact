# Entertainment Computing Full Local Validation

This directory stores the official full matched-budget local validation run used by the revised manuscript.

## Source-of-truth status

The previous non-robust 14-method logs in this directory were removed. This directory now contains the 16-method robust validation logs copied from `code_package/logs/full_validation/`.

## Generation commands

Run from the artifact root:

```bash
python code_package/scripts/run_full_validation.py --full --output experiments/tog2026_full_validation/logs/full_validation
python code_package/scripts/analyze_results.py --log-dir experiments/tog2026_full_validation/logs/full_validation --table-dir experiments/tog2026_full_validation/paper/revised/tables --fig-dir experiments/tog2026_full_validation/paper/revised/figures
python code_package/scripts/make_manuscript_assets.py --log-dir experiments/tog2026_full_validation/logs/full_validation --table-dir experiments/tog2026_full_validation/paper/revised/tables --fig-dir experiments/tog2026_full_validation/paper/revised/figures --out-dir experiments/tog2026_full_validation/paper/revised/manuscript_assets
python code_package/scripts/audit_package.py --profile full --out experiments/tog2026_full_validation/PACKAGE_AUDIT_REPORT.md
```

## Run summary

- Interval log rows: 19,200
- Atomic-step log rows: 150,297
- Interval-log columns: 67
- Atomic-step columns: 20
- Tasks: `grid-treasure`, `line-duel`, `resource-defense`
- Methods: 16, including robust-DLGPR and robust-near-elite-DLGPR
- Method list: `DLGPR-full`, `GA-only`, `PSO-only`, `RL-only`, `fixed-split`, `greedy-improvement`, `no-diversity`, `no-handshake`, `no-learning-progress`, `no-non-starvation`, `no-ucb`, `relaxed-delta-min`, `robust-DLGPR`, `robust-near-elite-DLGPR`, `round-robin`, `strict-delta-max`
- Seeds: 10
- Planning intervals per run: 40
- Robust variants present: yes
- Source-of-truth audit: `../LOG_REPLACEMENT_AUDIT.md`

## Claim boundary

These logs support implementation-level claims about matched-budget accounting, metadata completeness, scheduler behavior, robust DLGPR variants, ablation plumbing, and strict-versus-relaxed timing. They do not establish broad performance generalization to GVGAI, MicroRTS, Procgen, OpenSpiel, or other external Game AI benchmarks.


## Method-equivalence note

These pairs are behaviorally equivalent under the reported configuration: `DLGPR-full` / `strict-delta-max`, and `fixed-split` / `round-robin`. The logs preserve scheduler labels for traceability; they should not be counted as independent algorithmic baselines.
