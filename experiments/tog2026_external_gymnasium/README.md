# Entertainment Computing External Gymnasium Validation

This directory stores the official matched-budget robust external benchmark extension used by the revised manuscript.

## Source-of-truth status

The previous non-robust 14-method external logs in this directory were removed. This directory now contains the robust external-validation logs copied from `code_package/logs/robust_external_validation/`.

## Generation commands

Run from the artifact root:

```bash
python code_package/scripts/run_external_validation.py --full
python code_package/scripts/analyze_results.py --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir experiments/tog2026_external_gymnasium/paper/revised/figures
python code_package/scripts/make_manuscript_assets.py --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir experiments/tog2026_external_gymnasium/paper/revised/figures --out-dir experiments/tog2026_external_gymnasium/paper/revised/manuscript_assets
python code_package/scripts/audit_package.py --profile external --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --out experiments/tog2026_external_gymnasium/PACKAGE_AUDIT_REPORT.md
```

## Run summary

- Interval log rows: 3,840
- Atomic-step log rows: 29,698
- Interval-log columns: 66
- Atomic-step columns: 20
- Tasks: `gym-blackjack`, `gym-cliffwalking`, `gym-frozenlake-4x4`, `gym-frozenlake-4x4-deterministic`
- Methods: 8, including robust-DLGPR and robust-near-elite-DLGPR
- Method list: `DLGPR-full`, `fixed-split`, `greedy-improvement`, `no-handshake`, `no-non-starvation`, `robust-DLGPR`, `robust-near-elite-DLGPR`, `round-robin`
- Seeds: 10
- Planning intervals per run: 12
- Robust variants present: yes
- Source-of-truth audit: `../LOG_REPLACEMENT_AUDIT.md`

## Claim boundary

These logs support named-task external adapter evidence and strict charged-time timing checks. They do not establish broad performance generalization to GVGAI, MicroRTS, Procgen, OpenSpiel, or MiniGrid.


## Method-equivalence note

These pairs are behaviorally equivalent under the reported configuration: `DLGPR-full` / `strict-delta-max`, and `fixed-split` / `round-robin`. The logs preserve scheduler labels for traceability; they should not be counted as independent algorithmic baselines.
