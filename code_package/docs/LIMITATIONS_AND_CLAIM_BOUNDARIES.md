# Timing Claim Boundary

The main 24 ms timing result is a **charged-time simulated budget-compliance** result. It states that, under the disclosed charged-time accounting model and the strict `delta_max` do-not-start rule, logged loop and end-to-end charged-time overruns are zero in the reported local and Gymnasium validations.

Raw CPU wall-clock timing is reported separately in the `tog2026_timing_profile` experiment under a calibrated 100 ms budget. That profile is diagnostic and must not be interpreted as a 24 ms deployment or engine-level real-time guarantee.

# Limitations and Claim Boundaries

This package is designed to close reviewer-identified reproducibility and metadata gaps. It does not, by itself, prove general Game AI superiority.

## Claims supported by this package

- The code can run a matched-budget GA/PSO/RL scheduler harness.
- The harness logs complete environment metadata for the included local tasks.
- Strict and relaxed do-not-start rules are separable and auditable.
- Cross-layer handoff is implemented and can be ablated.
- Baseline and ablation outputs are generated in manuscript-ready CSV form.
- Robust-versus-standard methods can be compared under a rollout-equivalent online compute account that charges evaluation, RL-training, and RL-to-population injection rollouts.
- The MiniGrid `Empty-5x5` fully observable adapter experiment demonstrates bounded recognized-benchmark integration.

## Claims not supported without additional external experiments

- Superiority on GVGAI, MicroRTS, Procgen, or commercial game engines.
- Real engine wall-clock latency unless an engine-integrated timing mode is used.
- Broad generalization across opponents, procedural seeds, or genres.
- Broad MiniGrid-suite superiority from the single fully observable `Empty-5x5` experiment.
- Production real-time guarantees beyond the declared charged-time contract.


## Method-equivalence disclosure

See `METHOD_EQUIVALENCE.md`. These pairs are behaviorally equivalent under the reported configuration: `DLGPR-full` / `strict-delta-max`, and `fixed-split` / `round-robin`. They are retained as diagnostic labels, not independent baselines.
