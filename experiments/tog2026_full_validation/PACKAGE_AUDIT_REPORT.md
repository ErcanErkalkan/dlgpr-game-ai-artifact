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
Log directory: `experiments/tog2026_full_validation/logs/full_validation`
- [OK] experiments/tog2026_full_validation/logs/full_validation/interval_logs.csv
- [OK] experiments/tog2026_full_validation/logs/full_validation/atomic_step_logs.csv
- [OK] experiments/tog2026_full_validation/logs/full_validation/environment_metadata.json

## Detected profile: `full`
Interval log rows: 19,200
Missing interval columns: none
Method count: 16
Missing methods: none
Unexpected methods: none
- [OK] expected interval rows = 19,200
Handshake events by method: {'DLGPR-full': 11891, 'GA-only': 0, 'PSO-only': 0, 'RL-only': 0, 'fixed-split': 12463, 'greedy-improvement': 9312, 'no-diversity': 13405, 'no-handshake': 0, 'no-learning-progress': 10715, 'no-non-starvation': 9897, 'no-ucb': 11121, 'relaxed-delta-min': 13922, 'robust-DLGPR': 12206, 'robust-near-elite-DLGPR': 3632, 'round-robin': 12463, 'strict-delta-max': 11891}
- [OK] DLGPR-full has positive handshake events
- [OK] no-handshake has zero handshake events
Strict-delta-max loop overruns: 0
- [OK] strict-delta-max has zero charged-time loop overruns

## Atomic-step log rows: 150,297
Missing atomic-step columns: none
- [OK] expected atomic rows = 150,297
Atomic modules observed: ['GA', 'PSO', 'RL']
- [OK] atomic modules are within GA/PSO/RL

## Environment metadata
Metadata task count: 3
- [OK] metadata contains at least 3 task(s)
Metadata missing for line-duel: none
Metadata missing for grid-treasure: none
Metadata missing for resource-defense: none

## Generated tables
Table directory: `experiments/tog2026_full_validation/paper/revised/tables`
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_method_equivalence.csv
  Missing table columns: none
  Method-equivalence pair validation: OK
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_main_results.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_statistical_tests.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_timing_profile.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_claim_limits.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_environment_metadata.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_metric_definitions.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_compute_accounting.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_strict_vs_relaxed.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_aggregate_vs_dlgpr.csv
  Missing table columns: none

Overall status: PASS
