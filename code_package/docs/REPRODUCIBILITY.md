# Reproducibility Instructions

All commands below are run from the artifact root.  This release uses the official `code_package` source layout: project metadata lives at the root, while importable source code lives under `code_package/dlgpr`.

## Install

```bash
python -m pip install -e .
```

## Tests

```bash
python code_package/tests/run_tests.py
```

## Quick validation

```bash
python code_package/scripts/run_full_validation.py --quick
python code_package/scripts/analyze_results.py --log-dir code_package/logs/full_validation --table-dir code_package/paper/revised/tables --fig-dir code_package/paper/revised/figures
python code_package/scripts/audit_package.py
```

## Full local validation

```bash
python code_package/scripts/run_full_validation.py --full --output experiments/tog2026_full_validation/logs/full_validation
python code_package/scripts/analyze_results.py --log-dir experiments/tog2026_full_validation/logs/full_validation --table-dir experiments/tog2026_full_validation/paper/revised/tables --fig-dir experiments/tog2026_full_validation/paper/revised/figures
python code_package/scripts/audit_package.py --profile full --out experiments/tog2026_full_validation/PACKAGE_AUDIT_REPORT.md
```

## External Gymnasium validation

```bash
python code_package/scripts/run_external_validation.py --full
python code_package/scripts/analyze_results.py --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir experiments/tog2026_external_gymnasium/paper/revised/figures
python code_package/scripts/audit_package.py --profile external --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --out experiments/tog2026_external_gymnasium/PACKAGE_AUDIT_REPORT.md
```

## Raw-CPU timing profile

```bash
python code_package/scripts/run_timing_profile.py --full
python code_package/scripts/analyze_results.py --log-dir experiments/tog2026_timing_profile/logs/timing_profile --table-dir experiments/tog2026_timing_profile/paper/revised/tables --fig-dir experiments/tog2026_timing_profile/paper/revised/figures
python code_package/scripts/audit_package.py --profile timing --log-dir experiments/tog2026_timing_profile/logs/timing_profile --table-dir experiments/tog2026_timing_profile/paper/revised/tables --out experiments/tog2026_timing_profile/PACKAGE_AUDIT_REPORT.md
```

## Rollout-equivalent compute-matched local validation

```bash
python code_package/scripts/run_compute_matched_validation.py --full --basis rollout
python code_package/scripts/analyze_results.py --log-dir experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout --table-dir experiments/ec2026_compute_matched_rollout/paper/revised/tables --fig-dir experiments/ec2026_compute_matched_rollout/paper/revised/figures
python code_package/scripts/audit_package.py --profile compute-matched --log-dir experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout --table-dir experiments/ec2026_compute_matched_rollout/paper/revised/tables --out experiments/ec2026_compute_matched_rollout/PACKAGE_AUDIT_REPORT.md
```

## MiniGrid Empty-5x5 performance validation

```bash
python code_package/scripts/run_minigrid_performance.py --full
python code_package/scripts/analyze_results.py --log-dir experiments/ec2026_minigrid_performance/logs/minigrid_performance --table-dir experiments/ec2026_minigrid_performance/paper/revised/tables --fig-dir experiments/ec2026_minigrid_performance/paper/revised/figures
python code_package/scripts/audit_package.py --profile minigrid-performance --log-dir experiments/ec2026_minigrid_performance/logs/minigrid_performance --table-dir experiments/ec2026_minigrid_performance/paper/revised/tables --out experiments/ec2026_minigrid_performance/PACKAGE_AUDIT_REPORT.md
```

## Sensitivity run

```bash
python code_package/scripts/run_sensitivity.py
python code_package/scripts/analyze_sensitivity.py
```

## Main outputs

For quick/package-generation commands:

- `code_package/logs/full_validation/interval_logs.csv`
- `code_package/logs/full_validation/atomic_step_logs.csv`
- `code_package/logs/full_validation/environment_metadata.json`
- `code_package/paper/revised/tables/*.csv`
- `code_package/paper/revised/figures/*.png`

For manuscript-consistent completed release outputs:

- `experiments/tog2026_full_validation/`
- `experiments/tog2026_external_gymnasium/`
- `experiments/tog2026_timing_profile/`
- `experiments/ec2026_compute_matched_rollout/`
- `experiments/ec2026_minigrid_performance/`

## Determinism

All local runs use NumPy seeded RNG schedules. External adapters must disclose environment-level sources of nondeterminism.


## Method-equivalence disclosure

See `METHOD_EQUIVALENCE.md`. These pairs are behaviorally equivalent under the reported configuration: `DLGPR-full` / `strict-delta-max`, and `fixed-split` / `round-robin`. They are retained as diagnostic labels, not independent baselines.
