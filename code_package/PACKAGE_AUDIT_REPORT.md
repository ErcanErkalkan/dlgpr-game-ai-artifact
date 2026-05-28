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

Log directory: experiments/tog2026_full_validation/logs/full_validation
- [OK] experiments/tog2026_full_validation/logs/full_validation/interval_logs.csv
- [OK] experiments/tog2026_full_validation/logs/full_validation/atomic_step_logs.csv
- [OK] experiments/tog2026_full_validation/logs/full_validation/environment_metadata.json

## Interval log rows: 16800
Missing interval columns: none
Missing methods: none
Handshake events by method: {'DLGPR-full': 11891, 'GA-only': 0, 'PSO-only': 0, 'RL-only': 0, 'fixed-split': 12463, 'greedy-improvement': 9312, 'no-diversity': 13405, 'no-handshake': 0, 'no-learning-progress': 10715, 'no-non-starvation': 9897, 'no-ucb': 11121, 'relaxed-delta-min': 13922, 'round-robin': 12463, 'strict-delta-max': 11891}
Strict-delta-max loop overruns: 0

## Atomic-step log rows: 131718
Missing atomic-step columns: none
Atomic modules observed: ['GA', 'PSO', 'RL']

Metadata task count: 3
Metadata missing for line-duel: none
Metadata missing for grid-treasure: none
Metadata missing for resource-defense: none

Table directory: experiments/tog2026_full_validation/paper/revised/tables
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_main_results.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_strict_vs_relaxed.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_statistical_tests.csv
  Missing table columns: none
- [OK] experiments/tog2026_full_validation/paper/revised/tables/table_timing_profile.csv
  Missing table columns: none

Overall status: PASS
