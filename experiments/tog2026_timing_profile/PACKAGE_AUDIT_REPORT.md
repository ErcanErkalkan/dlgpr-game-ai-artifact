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
Log directory: `experiments/tog2026_timing_profile/logs/timing_profile`
- [OK] experiments/tog2026_timing_profile/logs/timing_profile/interval_logs.csv
- [OK] experiments/tog2026_timing_profile/logs/timing_profile/atomic_step_logs.csv
- [OK] experiments/tog2026_timing_profile/logs/timing_profile/environment_metadata.json

## Detected profile: `timing`
Interval log rows: 1,500
Missing interval columns: none
Method count: 3
Missing methods: none
Unexpected methods: none
- [OK] expected interval rows = 1,500
Handshake events by method: {'DLGPR-full': 5150, 'relaxed-delta-min': 8075, 'strict-delta-max': 4887}
- [OK] DLGPR-full has positive handshake events
Strict-delta-max loop overruns: 0
- [OK] strict-delta-max has zero charged-time loop overruns

## Atomic-step log rows: 16,158
Missing atomic-step columns: none
- [OK] expected atomic rows = 16,158
Atomic modules observed: ['GA', 'PSO', 'RL']
- [OK] atomic modules are within GA/PSO/RL

## Environment metadata
Metadata task count: 5
- [OK] metadata contains at least 3 task(s)
Metadata missing for line-duel: none
Metadata missing for resource-defense: none
Metadata missing for gym-frozenlake-4x4: none
Metadata missing for gym-cliffwalking: none
Metadata missing for minigrid-empty-5x5: none

## Generated tables
Table directory: `experiments/tog2026_timing_profile/paper/revised/tables`
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_method_equivalence.csv
  Missing table columns: none
  Method-equivalence pair validation: OK
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_main_results.csv
  Missing table columns: none
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_statistical_tests.csv
  Missing table columns: none
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_timing_profile.csv
  Missing table columns: none
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_claim_limits.csv
  Missing table columns: none
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_environment_metadata.csv
  Missing table columns: none
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_metric_definitions.csv
  Missing table columns: none
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_compute_accounting.csv
  Missing table columns: none

Overall status: PASS
