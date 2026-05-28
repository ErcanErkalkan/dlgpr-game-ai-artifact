# Manuscript Assets Generated from Local Validation Logs


## Claim-boundary paragraph for manuscript

The local experiments are self-contained validation tasks designed to verify scheduler implementation, metadata completeness, matched-budget accounting, strict-versus-relaxed timing behavior, and ablation plumbing. They should not be presented as evidence of general performance across established Game AI benchmarks. Broad empirical claims require the same harness to be connected to recognized benchmarks such as GVGAI, MicroRTS, Procgen, or OpenSpiel, with the same environment-disclosure and matched-budget logging fields used here.


## Environment-disclosure appendix draft

### line-duel
- **environment_name:** LineDuelEnv
- **environment_version:** 1.0-local
- **benchmark_family:** self-contained-game-ai
- **observation_definition:** [agent_pos, target_pos, opponent_pos, normalized_step, dist_target, dist_opponent, bias, slip_prob]
- **action_definition:** 0=left, 1=stay, 2=right
- **reward_definition:** +1.0 for reaching target, -1.0 if caught, -0.01 per step, small shaping toward target.
- **episode_termination:** Target reached, opponent catches agent, or max_steps reached.
- **opponent_policy:** Greedy one-step move toward agent with stochastic slip/no-move probability.
- **stochasticity_sources:** Initial positions and action slip controlled by seeded NumPy RNG.
- **rollout_horizon_H:** 4
- **number_of_rollouts_K:** 1
- **B_tau_ms:** 100.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 40.0
- **guard_margin_ms:** 10.0
- **scheduler_ema_lambda:** 0.75
- **timing_mode:** actual_cpu_raw
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1', 'gymnasium': '1.3.0', 'minigrid': '3.1.0'}

### resource-defense
- **environment_name:** ResourceDefenseEnv
- **environment_version:** 1.0-local
- **benchmark_family:** self-contained-rts-micro
- **observation_definition:** [resources, workers, soldiers, base_health, enemy_pressure, normalized_step, last_wave, cooldown, stockpile_ratio, defense_ratio, bias]
- **action_definition:** 0=gather, 1=train_worker, 2=train_soldier, 3=attack_pressure, 4=repair_base
- **reward_definition:** Incremental reward for survival, soldiers, and pressure reduction; penalties for base damage and defeat; terminal win bonus if base survives.
- **episode_termination:** Base destroyed or max_steps reached.
- **opponent_policy:** Seeded enemy pressure process with stochastic waves; pressure damages base unless countered by soldiers/attack actions.
- **stochasticity_sources:** Initial stockpile, enemy wave arrivals, and wave magnitudes controlled by seeded NumPy RNG.
- **rollout_horizon_H:** 4
- **number_of_rollouts_K:** 1
- **B_tau_ms:** 100.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 40.0
- **guard_margin_ms:** 10.0
- **scheduler_ema_lambda:** 0.75
- **timing_mode:** actual_cpu_raw
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1', 'gymnasium': '1.3.0', 'minigrid': '3.1.0'}

### gym-frozenlake-4x4
- **environment_name:** Gymnasium/FrozenLake-v1
- **environment_version:** 1.3.0
- **benchmark_family:** gymnasium-toy-text
- **observation_definition:** Discrete grid state encoded as a 16-dimensional one-hot vector.
- **action_definition:** Discrete, 4 actions: left, down, right, up.
- **reward_definition:** +1.0 for reaching the goal, 0 otherwise; slippery transition dynamics enabled.
- **episode_termination:** Goal reached, hole reached, or Gymnasium time-limit truncation.
- **opponent_policy:** No opponent; environment transition model is stochastic because the slippery map changes intended motion.
- **stochasticity_sources:** Gymnasium reset seed and slippery transition dynamics.
- **rollout_horizon_H:** 4
- **number_of_rollouts_K:** 1
- **B_tau_ms:** 100.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 40.0
- **guard_margin_ms:** 10.0
- **scheduler_ema_lambda:** 0.75
- **timing_mode:** actual_cpu_raw
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1', 'gymnasium': '1.3.0', 'minigrid': '3.1.0'}

### gym-cliffwalking
- **environment_name:** Gymnasium/CliffWalking-v1
- **environment_version:** 1.3.0
- **benchmark_family:** gymnasium-toy-text
- **observation_definition:** Discrete grid state encoded as a 48-dimensional one-hot vector.
- **action_definition:** Discrete, 4 actions: up, right, down, left.
- **reward_definition:** -1 per step and -100 for stepping into the cliff; episode ends at the goal.
- **episode_termination:** Goal reached or Gymnasium time-limit truncation.
- **opponent_policy:** No opponent; deterministic grid transition dynamics.
- **stochasticity_sources:** Gymnasium reset seed; transition dynamics are deterministic.
- **rollout_horizon_H:** 4
- **number_of_rollouts_K:** 1
- **B_tau_ms:** 100.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 40.0
- **guard_margin_ms:** 10.0
- **scheduler_ema_lambda:** 0.75
- **timing_mode:** actual_cpu_raw
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1', 'gymnasium': '1.3.0', 'minigrid': '3.1.0'}

### minigrid-empty-5x5
- **environment_name:** MiniGrid/MiniGrid-Empty-5x5-v0
- **environment_version:** 3.1.0
- **benchmark_family:** minigrid
- **observation_definition:** Partial-observation MiniGrid dictionary with 7x7x3 symbolic image and agent direction.
- **action_definition:** Discrete, 7 MiniGrid actions: left, right, forward, pickup, drop, toggle, done.
- **reward_definition:** MiniGrid sparse goal reward with built-in time penalty; zero for non-goal transitions.
- **episode_termination:** Goal reached or MiniGrid time-limit truncation.
- **opponent_policy:** No opponent; partial observability and randomized start/goal placement define task variation.
- **stochasticity_sources:** MiniGrid reset seed controls layout/start orientation and any environment randomization.
- **rollout_horizon_H:** 4
- **number_of_rollouts_K:** 1
- **B_tau_ms:** 100.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 40.0
- **guard_margin_ms:** 10.0
- **scheduler_ema_lambda:** 0.75
- **timing_mode:** actual_cpu_raw
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1', 'gymnasium': '1.3.0', 'minigrid': '3.1.0'}


## Manuscript-ready Results Narrative



Throughout the local validation tables, higher values are better for return, score, and win rate. Lower values are better for steps-to-threshold, p95/p99 latency, maximum latency, and overrun rates. Handshake counts are diagnostic and are not interpreted as a performance metric.



For `gym-cliffwalking`, the self-contained validation harness reports the best mean return for `DLGPR-full` (-4.000). The DLGPR-full configuration reports mean return -4.000, win rate 0.000, p99 latency 77.046 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.

For `gym-frozenlake-4x4`, the self-contained validation harness reports the best mean return for `DLGPR-full` (0.000). The DLGPR-full configuration reports mean return 0.000, win rate 0.000, p99 latency 67.076 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.

For `line-duel`, the self-contained validation harness reports the best mean return for `strict-delta-max` (0.358). The DLGPR-full configuration reports mean return 0.354, win rate 0.400, p99 latency 63.610 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.

For `minigrid-empty-5x5`, the self-contained validation harness reports the best mean return for `DLGPR-full` (0.000). The DLGPR-full configuration reports mean return 0.000, win rate 0.000, p99 latency 65.795 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.

For `resource-defense`, the self-contained validation harness reports the best mean return for `DLGPR-full` (0.151). The DLGPR-full configuration reports mean return 0.151, win rate 0.000, p99 latency 64.150 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.


## Strict versus relaxed timing interpretation



For `gym-cliffwalking`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.9900, E2E overrun rate 0.9900, and p99 latency 120.405 ms.

For `gym-cliffwalking`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 76.650 ms.

For `gym-frozenlake-4x4`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.9800, E2E overrun rate 0.9800, and p99 latency 105.428 ms.

For `gym-frozenlake-4x4`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 67.313 ms.

For `line-duel`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.7000, E2E overrun rate 0.7000, and p99 latency 102.406 ms.

For `line-duel`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 63.587 ms.

For `minigrid-empty-5x5`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 1.0000, E2E overrun rate 1.0000, and p99 latency 134.907 ms.

For `minigrid-empty-5x5`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 79.660 ms.

For `resource-defense`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.5800, E2E overrun rate 0.5800, and p99 latency 103.078 ms.

For `resource-defense`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 64.269 ms.

This paragraph should be used to explicitly separate the theorem-backed strict rule from the relaxed diagnostic variant.


## Figure interpretation scaffold

- `allocation_share_gym-cliffwalking.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_gym-frozenlake-4x4.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_line-duel.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_minigrid-empty-5x5.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_resource-defense.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `final_return_gym-cliffwalking.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_gym-frozenlake-4x4.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_line-duel.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_minigrid-empty-5x5.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_resource-defense.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `latency_cdf_gym-cliffwalking.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_gym-frozenlake-4x4.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_line-duel.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_minigrid-empty-5x5.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_resource-defense.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `overrun_cdf_gym-cliffwalking.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_gym-frozenlake-4x4.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_line-duel.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_minigrid-empty-5x5.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_resource-defense.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
