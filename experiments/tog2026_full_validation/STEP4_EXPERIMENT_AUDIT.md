# Step 4 Experiment Audit

Manuscript: ToG-2026-0045

Status: PASS

## Experiment Directory

- Required directory: `experiments/tog2026_full_validation/`
- Log directory: `experiments/tog2026_full_validation/logs/full_validation/`
- Old pilot logs overwritten: no
- Full-validation interval rows: 16,800
- Full-validation atomic-step rows: 131,718
- Tasks: `line-duel`, `grid-treasure`, `resource-defense`
- Seeds: 10, `0` through `9`
- Planning intervals per run: 40

## Method Coverage

| Required method | Implemented log method | Status |
|---|---|---|
| DLGPR full | `DLGPR-full` | present |
| GA-only | `GA-only` | present |
| PSO-only | `PSO-only` | present |
| RL-only | `RL-only` | present |
| fixed split GA-PSO-RL | `fixed-split` | present |
| round-robin scheduler | `round-robin` | present |
| greedy improvement-per-ms scheduler | `greedy-improvement` | present |
| DLGPR without diversity term | `no-diversity` | present |
| DLGPR without learning-progress term | `no-learning-progress` | present |
| DLGPR without UCB/exploration bonus | `no-ucb` | present |
| DLGPR without non-starvation | `no-non-starvation` | present |
| strict do-not-start threshold using delta_max | `strict-delta-max` | present |
| relaxed do-not-start threshold using delta_min | `relaxed-delta-min` | present |

Extra implemented ablation:

| Extra method | Purpose | Status |
|---|---|---|
| `no-handshake` | disables cross-layer handoff between GA, PSO, and RL | present |

## Required Interval-Log Fields

All required fields are present in `interval_logs.csv`.

| Required field | Log column |
|---|---|
| seed | `seed` |
| environment name | `environment_name` |
| task name | `task_name` |
| method | `method` |
| interval index | `interval` |
| B_tau | `B_tau_ms` |
| allowed_ms | `allowed_ms` |
| loop_time_ms | `loop_time_ms` |
| e2e_time_ms | `e2e_time_ms` |
| selected module | `selected_module` |
| atomic step duration | `atomic_step_duration_ms` |
| score | `score` |
| return | `return` |
| win/loss | `win` |
| steps-to-threshold | `steps_to_threshold` |
| p95 latency | `p95_latency_ms` |
| p99 latency | `p99_latency_ms` |
| worst-case latency | `max_latency_ms` |
| diversity value | `diversity_value` |
| learning-progress value | `learning_progress_value` |
| improvement-rate value | `improvement_rate_value` |

## Required Atomic-Step Fields

The atomic-step log provides the per-step selected module and charged duration. These fields support scheduler-allocation and timing-contract checks.

| Required field | Log column |
|---|---|
| run id | `run_id` |
| seed | `seed` |
| method | `method` |
| task name | `task_name` |
| interval index | `interval` |
| atomic step index | `atomic_index` |
| selected module | `module` |
| atomic step duration | `charged_ms` |
| measured CPU time | `cpu_ms` |
| score | `score` |
| improvement-rate value | `improvement_rate` |
| diversity value | `diversity` |
| learning-progress value | `learning_progress` |
| remaining budget before step | `remaining_before_ms` |
| remaining budget after step | `remaining_after_ms` |
| threshold rule | `do_not_start_rule` |

## Audit Commands

Run from `code_package/`:

```bash
python scripts/run_full_validation.py --full --output ..\experiments\tog2026_full_validation\logs\full_validation
python scripts/analyze_results.py --log-dir ..\experiments\tog2026_full_validation\logs\full_validation --table-dir ..\experiments\tog2026_full_validation\paper\revised\tables --fig-dir ..\experiments\tog2026_full_validation\paper\revised\figures
python scripts/audit_package.py --log-dir ..\experiments\tog2026_full_validation\logs\full_validation
```

Current audit result from `scripts/audit_package.py`: PASS.

