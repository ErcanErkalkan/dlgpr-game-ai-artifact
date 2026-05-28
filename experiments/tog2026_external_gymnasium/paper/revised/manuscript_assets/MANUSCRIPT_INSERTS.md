# Manuscript Assets Generated from Local Validation Logs


## Claim-boundary paragraph for manuscript

The local experiments are self-contained validation tasks designed to verify scheduler implementation, metadata completeness, matched-budget accounting, strict-versus-relaxed timing behavior, and ablation plumbing. They should not be presented as evidence of general performance across established Game AI benchmarks. Broad empirical claims require the same harness to be connected to recognized benchmarks such as GVGAI, MicroRTS, Procgen, or OpenSpiel, with the same environment-disclosure and matched-budget logging fields used here.


## Environment-disclosure appendix draft

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
- **rollout_horizon_H:** 80
- **number_of_rollouts_K:** 5
- **B_tau_ms:** 24.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 4.0
- **guard_margin_ms:** 2.0
- **scheduler_ema_lambda:** 0.75
- **timing_mode:** simulated_charged
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1', 'gymnasium': '1.3.0', 'minigrid': '3.1.0'}

### gym-frozenlake-4x4-deterministic
- **environment_name:** Gymnasium/FrozenLake-v1
- **environment_version:** 1.3.0
- **benchmark_family:** gymnasium-toy-text
- **observation_definition:** Discrete grid state encoded as a 16-dimensional one-hot vector.
- **action_definition:** Discrete, 4 actions: left, down, right, up.
- **reward_definition:** +1.0 for reaching the goal, 0 otherwise; deterministic transition dynamics.
- **episode_termination:** Goal reached, hole reached, or Gymnasium time-limit truncation.
- **opponent_policy:** No opponent; deterministic grid transition dynamics.
- **stochasticity_sources:** Gymnasium reset seed controls initial RNG state; transition dynamics are deterministic.
- **rollout_horizon_H:** 80
- **number_of_rollouts_K:** 5
- **B_tau_ms:** 24.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 4.0
- **guard_margin_ms:** 2.0
- **scheduler_ema_lambda:** 0.75
- **timing_mode:** simulated_charged
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
- **rollout_horizon_H:** 80
- **number_of_rollouts_K:** 5
- **B_tau_ms:** 24.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 4.0
- **guard_margin_ms:** 2.0
- **scheduler_ema_lambda:** 0.75
- **timing_mode:** simulated_charged
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1', 'gymnasium': '1.3.0', 'minigrid': '3.1.0'}

### gym-blackjack
- **environment_name:** Gymnasium/Blackjack-v1
- **environment_version:** 1.3.0
- **benchmark_family:** gymnasium-toy-text-card
- **observation_definition:** Tuple observation [player_sum, dealer_showing_card, usable_ace] represented as a normalized numeric vector.
- **action_definition:** Discrete, 2 actions: stick or hit.
- **reward_definition:** +1 for win, 0 for draw, -1 for loss under the Gymnasium Blackjack rules.
- **episode_termination:** Player sticks or goes bust; dealer then resolves the hand according to the built-in policy.
- **opponent_policy:** Built-in dealer policy: draw until reaching 17, then stick.
- **stochasticity_sources:** Gymnasium reset seed controls card draws and initial hands.
- **rollout_horizon_H:** 80
- **number_of_rollouts_K:** 5
- **B_tau_ms:** 24.0
- **delta_min_ms:** 1.0
- **delta_max_ms:** 4.0
- **guard_margin_ms:** 2.0
- **scheduler_ema_lambda:** 0.75
- **timing_mode:** simulated_charged
- **operating_system:** Windows-11-10.0.26200-SP0
- **runtime:** Python 3.14.3
- **library_versions:** {'numpy': '2.4.3', 'pandas': '3.0.1', 'matplotlib': '3.10.8', 'scipy': '1.17.1', 'gymnasium': '1.3.0', 'minigrid': '3.1.0'}


## Manuscript-ready Results Narrative



Throughout the local validation tables, higher values are better for return, score, and win rate. Lower values are better for steps-to-threshold, p95/p99 latency, maximum latency, and overrun rates. Handshake counts are diagnostic and are not interpreted as a performance metric.



For `gym-blackjack`, the self-contained validation harness reports the best mean return for `GA-only` (0.000). The DLGPR-full configuration reports mean return -0.120, win rate 0.380, p99 latency 23.819 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.

For `gym-cliffwalking`, the self-contained validation harness reports the best mean return for `DLGPR-full` (-80.000). The DLGPR-full configuration reports mean return -80.000, win rate 0.000, p99 latency 23.852 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.

For `gym-frozenlake-4x4`, the self-contained validation harness reports the best mean return for `relaxed-delta-min` (0.440). The DLGPR-full configuration reports mean return 0.380, win rate 0.380, p99 latency 23.583 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.

For `gym-frozenlake-4x4-deterministic`, the self-contained validation harness reports the best mean return for `DLGPR-full` (0.100). The DLGPR-full configuration reports mean return 0.100, win rate 0.100, p99 latency 23.678 ms. These values support implementation-level comparison under matched local budgets, not broad benchmark generalization.


## Strict versus relaxed timing interpretation



For `gym-blackjack`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.6000, E2E overrun rate 0.6000, and p99 latency 26.384 ms.

For `gym-blackjack`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 23.819 ms.

For `gym-cliffwalking`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.5417, E2E overrun rate 0.5417, and p99 latency 26.697 ms.

For `gym-cliffwalking`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 23.852 ms.

For `gym-frozenlake-4x4`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.5583, E2E overrun rate 0.5583, and p99 latency 26.369 ms.

For `gym-frozenlake-4x4`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 23.583 ms.

For `gym-frozenlake-4x4-deterministic`, `relaxed-delta-min` uses `relaxed_delta_min` and reports loop overrun rate 0.5917, E2E overrun rate 0.5917, and p99 latency 26.711 ms.

For `gym-frozenlake-4x4-deterministic`, `strict-delta-max` uses `strict_delta_max` and reports loop overrun rate 0.0000, E2E overrun rate 0.0000, and p99 latency 23.678 ms.

This paragraph should be used to explicitly separate the theorem-backed strict rule from the relaxed diagnostic variant.


## Figure interpretation scaffold

- `allocation_share_gym-blackjack.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_gym-cliffwalking.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_gym-frozenlake-4x4-deterministic.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_gym-frozenlake-4x4.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `allocation_share_minigrid-empty-5x5.png`: This figure shows how DLGPR allocates atomic steps across GA, PSO, and RL over planning intervals. It should be used to show whether the scheduler collapses to a fixed split or dynamically reallocates compute.
- `final_return_gym-blackjack.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_gym-cliffwalking.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_gym-frozenlake-4x4-deterministic.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_gym-frozenlake-4x4.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `final_return_minigrid-empty-5x5.png`: This figure compares final local validation return by method. It should be interpreted with the claim boundary that these are self-contained tasks.
- `latency_cdf_gym-blackjack.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_gym-cliffwalking.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_gym-frozenlake-4x4-deterministic.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_gym-frozenlake-4x4.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `latency_cdf_minigrid-empty-5x5.png`: This figure shows the empirical distribution of per-interval charged E2E time. Curves farther left indicate lower latency. Use it to discuss tail-latency behavior under matched budgets.
- `overrun_cdf_gym-blackjack.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_gym-cliffwalking.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_gym-frozenlake-4x4-deterministic.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_gym-frozenlake-4x4.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
- `overrun_cdf_minigrid-empty-5x5.png`: This figure shows loop-budget overrun magnitudes. A mass at zero and a left-shifted curve indicate better budget compliance.
