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

Log directory: experiments/tog2026_external_gymnasium/logs/external_validation
- [OK] experiments/tog2026_external_gymnasium/logs/external_validation/interval_logs.csv
- [OK] experiments/tog2026_external_gymnasium/logs/external_validation/atomic_step_logs.csv
- [OK] experiments/tog2026_external_gymnasium/logs/external_validation/environment_metadata.json

## Interval log rows: 6720
Missing interval columns: none
Missing methods: none
Handshake events by method: {'DLGPR-full': 4870, 'GA-only': 0, 'PSO-only': 0, 'RL-only': 0, 'fixed-split': 4934, 'greedy-improvement': 3739, 'no-diversity': 5452, 'no-handshake': 0, 'no-learning-progress': 4306, 'no-non-starvation': 4158, 'no-ucb': 4829, 'relaxed-delta-min': 5567, 'round-robin': 4934, 'strict-delta-max': 4870}
Strict-delta-max loop overruns: 0

## Atomic-step log rows: 52687
Missing atomic-step columns: none
Atomic modules observed: ['GA', 'PSO', 'RL']

Metadata task count: 4
Metadata missing for gym-frozenlake-4x4: none
Metadata missing for gym-frozenlake-4x4-deterministic: none
Metadata missing for gym-cliffwalking: none
Metadata missing for gym-blackjack: none

Table directory: experiments/tog2026_external_gymnasium/paper/revised/tables
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_main_results.csv
  Missing table columns: none
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_strict_vs_relaxed.csv
  Missing table columns: none
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_statistical_tests.csv
  Missing table columns: none
- [OK] experiments/tog2026_external_gymnasium/paper/revised/tables/table_timing_profile.csv
  Missing table columns: none

Overall status: PASS
