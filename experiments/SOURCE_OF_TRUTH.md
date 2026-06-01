# Experiment source of truth

This package uses the 16-method robust validation results as the official source of truth.

Official cardinalities:

- Full validation: 19,200 interval rows / 150,297 atomic rows / 16 logged scheduler labels, including two behaviorally equivalent diagnostic pairs.
- External robust validation: 3,840 interval rows / 29,698 atomic rows / 8 methods.


Official full-validation logs:

- `experiments/tog2026_full_validation/logs/full_validation/interval_logs.csv`
- `experiments/tog2026_full_validation/logs/full_validation/atomic_step_logs.csv`
- `experiments/tog2026_full_validation/logs/full_validation/environment_metadata.json`

Official external-validation logs:

- `experiments/tog2026_external_gymnasium/logs/external_validation/interval_logs.csv`
- `experiments/tog2026_external_gymnasium/logs/external_validation/atomic_step_logs.csv`
- `experiments/tog2026_external_gymnasium/logs/external_validation/environment_metadata.json`

The previous non-robust 14-method experiment logs were removed from the official experiment directories.


## Method-equivalence note

These pairs are behaviorally equivalent under the reported configuration: `DLGPR-full` / `strict-delta-max`, and `fixed-split` / `round-robin`. The logs preserve scheduler labels for traceability; they should not be counted as independent algorithmic baselines.
