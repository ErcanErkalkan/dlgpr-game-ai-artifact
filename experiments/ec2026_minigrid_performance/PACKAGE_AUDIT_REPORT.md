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
Log directory: `experiments/ec2026_minigrid_performance/logs/minigrid_performance`
- [OK] experiments/ec2026_minigrid_performance/logs/minigrid_performance/interval_logs.csv
- [OK] experiments/ec2026_minigrid_performance/logs/minigrid_performance/atomic_step_logs.csv
- [OK] experiments/ec2026_minigrid_performance/logs/minigrid_performance/environment_metadata.json

## Detected profile: `minigrid-performance`
Interval log rows: 960
Missing interval columns: none
Method count: 8
Missing methods: none
Unexpected methods: none
- [OK] expected interval rows = 960
Handshake events by method: {'DLGPR-full': 2124, 'GA-only': 0, 'PSO-only': 0, 'RL-only': 0, 'fixed-split': 1800, 'greedy-improvement': 2400, 'robust-DLGPR': 720, 'robust-near-elite-DLGPR': 655}
- [OK] DLGPR-full has positive handshake events

## Atomic-step log rows: 13,543
Missing atomic-step columns: none
- [OK] expected atomic rows = 13,543
Atomic modules observed: ['GA', 'PSO', 'RL']
- [OK] atomic modules are within GA/PSO/RL

## Environment metadata
Metadata task count: 1
- [OK] metadata contains at least 1 task(s)
Metadata missing for minigrid-empty-5x5-fullyobs: none

## Generated tables
Table directory: `experiments/ec2026_minigrid_performance/paper/revised/tables`
- [OK] experiments/ec2026_minigrid_performance/paper/revised/tables/table_method_equivalence.csv
  Missing table columns: none
  Method-equivalence pair validation: OK
- [OK] experiments/ec2026_minigrid_performance/paper/revised/tables/table_main_results.csv
  Missing table columns: none
- [OK] experiments/ec2026_minigrid_performance/paper/revised/tables/table_statistical_tests.csv
  Missing table columns: none
- [OK] experiments/ec2026_minigrid_performance/paper/revised/tables/table_timing_profile.csv
  Missing table columns: none
- [OK] experiments/ec2026_minigrid_performance/paper/revised/tables/table_claim_limits.csv
  Missing table columns: none
- [OK] experiments/ec2026_minigrid_performance/paper/revised/tables/table_environment_metadata.csv
  Missing table columns: none
- [OK] experiments/ec2026_minigrid_performance/paper/revised/tables/table_metric_definitions.csv
  Missing table columns: none
- [OK] experiments/ec2026_minigrid_performance/paper/revised/tables/table_compute_accounting.csv
  Missing table columns: none

Overall status: PASS
