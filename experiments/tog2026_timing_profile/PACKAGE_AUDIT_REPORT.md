# Package Audit Report

- [OK] README.md
- [OK] requirements.txt
- [OK] pyproject.toml
- [OK] LICENSE
- [OK] CITATION.cff
- [OK] docs/ENVIRONMENT_DISCLOSURE.md
- [OK] docs/METRIC_DEFINITIONS.md
- [OK] docs/EXTERNAL_BENCHMARK_ADAPTERS.md
- [OK] docs/REPRODUCIBILITY.md
- [OK] docs/MANUSCRIPT_INTEGRATION.md
- [OK] Dockerfile
- [OK] Makefile

Log directory: experiments/tog2026_timing_profile/logs/timing_profile
- [OK] experiments/tog2026_timing_profile/logs/timing_profile/interval_logs.csv
- [OK] experiments/tog2026_timing_profile/logs/timing_profile/atomic_step_logs.csv
- [OK] experiments/tog2026_timing_profile/logs/timing_profile/environment_metadata.json

## Interval log rows: 1500
Missing interval columns: none
Missing methods: none
Handshake events by method: {'DLGPR-full': 5150, 'relaxed-delta-min': 8075, 'strict-delta-max': 4887}
Strict-delta-max loop overruns: 0

## Atomic-step log rows: 16158
Missing atomic-step columns: none
Atomic modules observed: ['GA', 'PSO', 'RL']

Metadata task count: 5
Metadata missing for line-duel: none
Metadata missing for resource-defense: none
Metadata missing for gym-frozenlake-4x4: none
Metadata missing for gym-cliffwalking: none
Metadata missing for minigrid-empty-5x5: none

Table directory: experiments/tog2026_timing_profile/paper/revised/tables
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_main_results.csv
  Missing table columns: none
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_strict_vs_relaxed.csv
  Missing table columns: none
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_statistical_tests.csv
  Missing table columns: none
- [OK] experiments/tog2026_timing_profile/paper/revised/tables/table_timing_profile.csv
  Missing table columns: none

Overall status: PASS
