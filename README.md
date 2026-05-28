# DLGPR Game AI Artifact

This release repository contains the code, reproducibility scripts, metadata, logs, tables, and figures for the DLGPR Game AI validation artifact.

The manuscript source and manuscript PDF are intentionally excluded. The artifact is meant for GitHub and Zenodo publication as code/data accompanying the paper, not as the paper submission package itself.

## Contents

- `code_package/`: implementation, tests, analysis scripts, documentation, Dockerfile, and generated compact outputs.
- `experiments/tog2026_full_validation/`: metadata-complete full validation logs, generated tables, generated figures, and experiment audit notes.

## Validation

From `code_package/`:

```bash
python -m tests.run_tests
python scripts/audit_package.py --log-dir ../experiments/tog2026_full_validation/logs/full_validation
```

Expected status:

- 10 tests pass.
- Package audit reports `Overall status: PASS`.
- Strict `delta_max` timing has zero loop overruns in the full validation logs.

## Paper Exclusion

The `Paper/` directory from the working folder is not included here. This avoids publishing the manuscript source, manuscript PDF, Elsevier template files, and journal-submission material in the public artifact repository.

## License

The software package is released under the MIT License in `code_package/LICENSE`.

