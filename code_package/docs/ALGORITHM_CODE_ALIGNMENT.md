# Algorithm-to-code alignment disclosure

This artifact aligns the manuscript algorithm section with the executable code.

## Implemented representation

The released local and Gymnasium validation harnesses optimize continuous policy/controller parameter vectors only. In code this is `LinearSoftmaxPolicy`: a candidate `theta` is reshaped into a linear softmax weight matrix. Projection is implemented by `repair_theta`, which clips the vector to the disclosed bounds.

The released artifact does **not** implement discrete PCG encodings, difficulty vectors, level artifacts, or environment-configuration optimization. Those targets must not be claimed as evaluated results.

## Scheduler index

The implemented DLGPR index contains:

- exponentially smoothed improvement rate per charged millisecond;
- GA-only diversity from behavioral descriptors of the GA population;
- RL-only learning progress from the RL surrogate-loss proxy;
- UCB-style exploration pressure using cumulative scheduler-state counts.

The UCB counts are cumulative over the scheduler state (`selection_counts` and `total_selections`), not reset at each interval.

## Non-starvation implementation

Non-starvation is **not** an additive `w_S S_m` index bonus in the released code. The default DLGPR implementation uses an explicit `n_min` minimum-selection safeguard: before applying the index, `select()` checks current-interval module counts and selects missing modules until each active module reaches `n_min`. `DLGPR-full`, `strict-delta-max`, and `robust-DLGPR` use `n_min=1`; the `no-non-starvation` ablation uses `n_min=0`.

## Candidate exchange and handoff

The code does not maintain one materialized global shared candidate pool. It maintains module-local memories plus a run-level incumbent:

- GA keeps a population and fitness values.
- PSO keeps particle positions, velocities, and personal-best values.
- RL keeps one parameter vector and a surrogate-loss proxy.
- The experiment loop keeps the best evaluated incumbent `best_theta` and `best_value`.

Cross-layer handoff is explicit:

- if RL is selected, its candidate can be injected into GA and PSO memories via `inject_candidate`;
- if GA or PSO is selected, RL can distill toward that candidate via `distill_toward`;
- there is no direct GA-to-PSO or PSO-to-GA transfer in the released code.

## Manuscript implication

The manuscript describes the implemented policy-vector scheduler, not a broader artifact/PCG/difficulty optimizer. Any future extension to PCG or difficulty control would require a concrete codec, candidate fields, objective, and logs.
