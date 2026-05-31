# Timing Claim Boundary

This artifact separates **charged-time simulated budget compliance** from **raw CPU wall-clock timing**.

## Charged-time simulated budget compliance

The main local and Gymnasium validation logs use the disclosed `simulated_charged` timing mode. The 24 ms result means that the strict `delta_max` do-not-start rule produces zero charged loop and end-to-end overruns under that declared accounting model. This is the result used for the manuscript's primary timing-compliance claim.

## Raw CPU wall-clock timing

The raw-CPU timing profile uses `actual_cpu_raw` timing and a separate calibrated 100 ms interval budget. It measures Python CPU behavior of the implementation and is useful for diagnostics, but it is not a 24 ms game-engine wall-clock guarantee.

## Required wording

Use: `zero strict-rule charged-time overruns under the disclosed 24 ms charged-time budget`.

Do not use: `zero 24 ms wall-clock overruns` or `deployment-grade real-time guarantee`.
