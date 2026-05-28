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
- **rollout_horizon_H:** 24
- **number_of_rollouts_K:** 5
- **B_tau_ms:** 24.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 4.0
- **guard_margin_ms:** 2.0
- **timing_mode:** simulated_charged
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1'}

### grid-treasure
- **environment_name:** GridTreasureEnv
- **environment_version:** 1.0-local
- **benchmark_family:** self-contained-game-ai
- **observation_definition:** [agent_xy, treasure_xy, chaser_xy, normalized_step, manhattan_treasure, manhattan_chaser, bias]
- **action_definition:** 0=stay, 1=up, 2=down, 3=left, 4=right
- **reward_definition:** +1.0 for treasure, -1.0 when caught, -0.01 per step, shaping toward treasure, random hazard penalty.
- **episode_termination:** Treasure reached, chaser catches agent, or max_steps reached.
- **opponent_policy:** Chaser greedily reduces Manhattan distance every other step with seeded randomness.
- **stochasticity_sources:** Initial positions, hazard penalty, and chaser tie-breaking controlled by seeded NumPy RNG.
- **rollout_horizon_H:** 24
- **number_of_rollouts_K:** 5
- **B_tau_ms:** 24.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 4.0
- **guard_margin_ms:** 2.0
- **timing_mode:** simulated_charged
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1'}

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
- **rollout_horizon_H:** 24
- **number_of_rollouts_K:** 5
- **B_tau_ms:** 24.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 4.0
- **guard_margin_ms:** 2.0
- **timing_mode:** simulated_charged
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1'}


## Manuscript-ready Results Narrative



Throughout the local validation tables, higher values are better for return, score, and win rate. Lower values are better for steps-to-threshold, p95/p99 latency, maximum latency, and overrun rates. Handshake counts are diagnostic and are not interpreted as a performance metric.



For `grid-treasure`, the self-contained validation harness reports the best mean return for `no-handshake` (-0.052). The DLGPR-full configuration reports mean return -0.145, win rate 0.440, p99 latency 23.587 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.

For `line-duel`, the self-contained validation harness reports the best mean return for `relaxed-delta-min` (-0.116). The DLGPR-full configuration reports mean return -0.118, win rate 0.440, p99 latency 23.720 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.

For `resource-defense`, the self-contained validation harness reports the best mean return for `no-non-starvation` (1.512). The DLGPR-full configuration reports mean return 1.504, win rate 0.000, p99 latency 23.614 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.


## Strict versus relaxed timing interpretation



For `grid-treasure`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.6275, E2E overrun rate 0.6275, and p99 latency 26.504 ms.

For `grid-treasure`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 23.587 ms.

For `line-duel`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.5825, E2E overrun rate 0.5825, and p99 latency 26.671 ms.

For `line-duel`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 23.720 ms.

For `resource-defense`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.6100, E2E overrun rate 0.6100, and p99 latency 26.593 ms.

For `resource-defense`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 23.614 ms.

This paragraph should be used to explicitly separate the theorem-backed strict rule from the relaxed diagnostic variant.


## Figure interpretation scaffold

- `allocation_share_grid-treasure.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_line-duel.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_resource-defense.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `final_return_grid-treasure.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_line-duel.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_resource-defense.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `latency_cdf_grid-treasure.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_line-duel.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_resource-defense.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `overrun_cdf_grid-treasure.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_line-duel.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_resource-defense.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
