# Experiment source of truth

This package preserves the 16-method charged-time robust validation as the
official contract-diagnostic source of truth and adds rollout-equivalent
performance layers for compute-matched interpretation.

Official cardinalities:

- Full validation: 19,200 interval rows / 150,297 atomic rows / 16 logged scheduler labels, including two behaviorally equivalent diagnostic pairs.
- External robust validation: 3,840 interval rows / 29,698 atomic rows / 8 methods.
- Rollout-equivalent local comparison: 9,600 interval rows / 134,027 atomic rows / 8 methods.
- MiniGrid Empty-5x5 fully observable comparison: 960 interval rows / 13,543 atomic rows / 8 methods.


Official full-validation logs:

- `experiments/tog2026_full_validation/logs/full_validation/interval_logs.csv`
- `experiments/tog2026_full_validation/logs/full_validation/atomic_step_logs.csv`
- `experiments/tog2026_full_validation/logs/full_validation/environment_metadata.json`

Official external-validation logs:

- `experiments/tog2026_external_gymnasium/logs/external_validation/interval_logs.csv`
- `experiments/tog2026_external_gymnasium/logs/external_validation/atomic_step_logs.csv`
- `experiments/tog2026_external_gymnasium/logs/external_validation/environment_metadata.json`

Official rollout-equivalent performance logs:

- `experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout/`
- `experiments/ec2026_minigrid_performance/logs/minigrid_performance/`

Use the rollout-equivalent local logs for robust-versus-standard performance
interpretation. Use the MiniGrid logs as bounded Empty-5x5 benchmark evidence.
Use the historical charged-time logs for stopping-contract diagnostics.

The previous non-robust 14-method experiment logs were removed from the official experiment directories.


## Method-equivalence note

These pairs are behaviorally equivalent under the reported configuration: `DLGPR-full` / `strict-delta-max`, and `fixed-split` / `round-robin`. The logs preserve scheduler labels for traceability; they should not be counted as independent algorithmic baselines.
