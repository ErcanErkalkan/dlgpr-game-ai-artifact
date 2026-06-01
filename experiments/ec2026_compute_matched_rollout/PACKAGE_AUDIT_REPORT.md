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
Log directory: `experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout`
- [OK] experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout/interval_logs.csv
- [OK] experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout/atomic_step_logs.csv
- [OK] experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout/environment_metadata.json

## Detected profile: `compute-matched`
Interval log rows: 9,600
Missing interval columns: none
Method count: 8
Missing methods: none
Unexpected methods: none
- [OK] expected interval rows = 9,600
Handshake events by method: {'DLGPR-full': 19540, 'GA-only': 0, 'PSO-only': 0, 'RL-only': 0, 'fixed-split': 18000, 'greedy-improvement': 24000, 'robust-DLGPR': 7200, 'robust-near-elite-DLGPR': 3746}
- [OK] DLGPR-full has positive handshake events

## Atomic-step log rows: 134,027
Missing atomic-step columns: none
- [OK] expected atomic rows = 134,027
Atomic modules observed: ['GA', 'PSO', 'RL']
- [OK] atomic modules are within GA/PSO/RL

## Environment metadata
Metadata task count: 3
- [OK] metadata contains at least 3 task(s)
Metadata missing for line-duel: none
Metadata missing for grid-treasure: none
Metadata missing for resource-defense: none

## Generated tables
Table directory: `experiments/ec2026_compute_matched_rollout/paper/revised/tables`
- [OK] experiments/ec2026_compute_matched_rollout/paper/revised/tables/table_method_equivalence.csv
  Missing table columns: none
  Method-equivalence pair validation: OK
- [OK] experiments/ec2026_compute_matched_rollout/paper/revised/tables/table_main_results.csv
  Missing table columns: none
- [OK] experiments/ec2026_compute_matched_rollout/paper/revised/tables/table_statistical_tests.csv
  Missing table columns: none
- [OK] experiments/ec2026_compute_matched_rollout/paper/revised/tables/table_timing_profile.csv
  Missing table columns: none
- [OK] experiments/ec2026_compute_matched_rollout/paper/revised/tables/table_claim_limits.csv
  Missing table columns: none
- [OK] experiments/ec2026_compute_matched_rollout/paper/revised/tables/table_environment_metadata.csv
  Missing table columns: none
- [OK] experiments/ec2026_compute_matched_rollout/paper/revised/tables/table_metric_definitions.csv
  Missing table columns: none
- [OK] experiments/ec2026_compute_matched_rollout/paper/revised/tables/table_compute_accounting.csv
  Missing table columns: none

Overall status: PASS
