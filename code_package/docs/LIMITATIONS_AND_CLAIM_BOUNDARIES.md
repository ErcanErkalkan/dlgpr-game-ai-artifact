# Limitations and Claim Boundaries

This package is designed to close reviewer-identified reproducibility and metadata gaps. It does not, by itself, prove general Game AI superiority.

## Claims supported by this package

- The code can run a matched-budget GA/PSO/RL scheduler harness.
- The harness logs complete environment metadata for the included local tasks.
- Strict and relaxed do-not-start rules are separable and auditable.
- Cross-layer handoff is implemented and can be ablated.
- Baseline and ablation outputs are generated in manuscript-ready CSV form.

## Claims not supported without additional external experiments

- Superiority on GVGAI, MicroRTS, Procgen, or commercial game engines.
- Real engine wall-clock latency unless an engine-integrated timing mode is used.
- Broad generalization across opponents, procedural seeds, or genres.
- Production real-time guarantees beyond the declared charged-time contract.
