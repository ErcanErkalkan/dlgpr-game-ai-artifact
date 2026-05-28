# Artifact Manifest

| Path | Purpose |
|---|---|
| `dlgpr/envs.py` | Self-contained game-like environments with metadata. |
| `dlgpr/modules.py` | GA, PSO, RL atomic update modules and cross-layer handoff operations. |
| `dlgpr/scheduler.py` | DLGPR, fixed-split, round-robin, and greedy schedulers. |
| `dlgpr/experiment.py` | Matched-budget experiment runner and logging schema. |
| `dlgpr/analysis.py` | Table and figure generation. |
| `dlgpr/external_adapters.py` | Optional adapter interface for external benchmarks. |
| `scripts/run_full_validation.py` | Quick/full experiment execution. |
| `scripts/run_sensitivity.py` | Compact budget-sensitivity execution. |
| `scripts/analyze_results.py` | Generates result tables and figures. |
| `scripts/audit_package.py` | Checks reviewer-critical package completeness. |
| `tests/` | Unit and smoke tests. |
| `logs/full_validation/` | Latest generated local validation logs. |
| `paper/revised/tables/` | Manuscript-ready CSV tables. |
| `paper/revised/figures/` | Manuscript-ready PNG figures. |
