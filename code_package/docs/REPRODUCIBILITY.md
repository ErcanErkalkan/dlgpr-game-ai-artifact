# Reproducibility Instructions

## Install

```bash
python -m pip install -r requirements.txt
```

## Tests

```bash
python -m tests.run_tests
```

## Quick validation

```bash
python scripts/run_full_validation.py --quick
python scripts/analyze_results.py
python scripts/audit_package.py
```

## Full local validation

```bash
python scripts/run_full_validation.py --full
python scripts/analyze_results.py
python scripts/audit_package.py
```

## External Gymnasium validation

```bash
python scripts/run_external_validation.py --full
python scripts/analyze_results.py --log-dir ../experiments/tog2026_external_gymnasium/logs/external_validation --table-dir ../experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir ../experiments/tog2026_external_gymnasium/paper/revised/figures
python scripts/audit_package.py --log-dir ../experiments/tog2026_external_gymnasium/logs/external_validation --table-dir ../experiments/tog2026_external_gymnasium/paper/revised/tables
```

## Raw-CPU timing profile

```bash
python scripts/run_timing_profile.py --full
python scripts/analyze_results.py --log-dir ../experiments/tog2026_timing_profile/logs/timing_profile --table-dir ../experiments/tog2026_timing_profile/paper/revised/tables --fig-dir ../experiments/tog2026_timing_profile/paper/revised/figures
python scripts/audit_package.py --log-dir ../experiments/tog2026_timing_profile/logs/timing_profile --table-dir ../experiments/tog2026_timing_profile/paper/revised/tables
```

## Sensitivity run

```bash
python scripts/run_sensitivity.py
```

## Main outputs

- `logs/full_validation/interval_logs.csv`
- `logs/full_validation/atomic_step_logs.csv`
- `logs/full_validation/environment_metadata.json`
- `paper/revised/tables/*.csv`
- `paper/revised/figures/*.png`
- `PACKAGE_AUDIT_REPORT.md`

Release-level completed outputs are stored under `../experiments/` rather than `code_package/logs/`.

## Determinism

All local runs use NumPy seeded RNG schedules. External adapters must disclose environment-level sources of nondeterminism.
