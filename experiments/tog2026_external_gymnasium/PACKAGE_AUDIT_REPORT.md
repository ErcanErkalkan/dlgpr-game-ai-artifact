# Package Audit Report

Artifact root: `.`
Official command: `python code_package/scripts/audit_package.py`

## Root and code-layout files
- [OK] README.md
- [OK] requirements.txt
- [OK] pyproject.toml
- [OK] LICENSE
- [OK] CITATION.cff
- [OK] .zenodo.json
- [OK] Dockerfile
- [OK] Makefile
- [OK] code_package/docs/ENVIRONMENT_DISCLOSURE.md
- [OK] code_package/docs/METRIC_DEFINITIONS.md
- [OK] code_package/docs/EXTERNAL_BENCHMARK_ADAPTERS.md
- [OK] code_package/docs/REPRODUCIBILITY.md
- [OK] code_package/docs/MANUSCRIPT_INTEGRATION.md
- [OK] code_package/docs/METHOD_EQUIVALENCE.md
- [OK] code_package/docs/DUPLICATE_METHOD_VALIDATION.md
- [OK] code_package/dlgpr/experiment.py
- [OK] code_package/dlgpr/scheduler.py
- [OK] code_package/tests/run_tests.py

## Log files
Log directory: `experiments/tog2026_external_gymnasium/logs/external_validation`
- [OK] experiments/tog2026_external_gymnasium/logs/external_validation/interval_logs.csv
- [OK] experiments/tog2026_external_gymnasium/logs/external_validation/atomic_step_logs.csv
- [OK] experiments/tog2026_external_gymnasium/logs/external_validation/environment_metadata.json

## Detected profile: `external`
Interval log rows: 3,840
Missing interval columns: none
Method count: 8
Missing methods: none
Unexpected methods: none
- [OK] expected interval rows = 3,840
Handshake events by method: {'DLGPR-full': 4870, 'fixed-split': 4934, 'greedy-improvement': 3739, 'no-handshake': 0, 'no-non-starvation': 4158, 'robust-DLGPR': 4863, 'robust-near-elite-DLGPR': 2798, 'round-robin': 4934}
- [OK] DLGPR-full has positive handshake events
- [OK] no-handshake has zero handshake events

## Atomic-step log rows: 29,698
Missing atomic-step columns: none
- [OK] expected atomic rows = 29,698
Atomic modules observed: ['GA', 'PSO', 'RL']
- [OK] atomic modules are within GA/PSO/RL

## Environment metadata
Metadata task count: 4
- [OK] metadata contains at least three tasks
Metadata missing for gym-frozenlake-4x4: none
Metadata missing for gym-frozenlake-4x4-deterministic: none
Metadata missing for gym-cliffwalking: none
Metadata missing for gym-blackjack: none

## Generated tables
Table directory: `experiments/tog2026_external_gymnasium/paper/revised/tables`
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_method_equivalence.csv
  Missing table columns: none
  Method-equivalence pair validation: OK
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_main_results.csv
  Missing table columns: none
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_statistical_tests.csv
  Missing table columns: none
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_timing_profile.csv
  Missing table columns: none
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_claim_limits.csv
  Missing table columns: none
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_environment_metadata.csv
  Missing table columns: none
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_metric_definitions.csv
  Missing table columns: none

Overall status: PASS
