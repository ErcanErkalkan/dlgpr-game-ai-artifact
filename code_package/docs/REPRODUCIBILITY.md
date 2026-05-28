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

## Determinism

All local runs use NumPy seeded RNG schedules. External adapters must disclose environment-level sources of nondeterminism.
