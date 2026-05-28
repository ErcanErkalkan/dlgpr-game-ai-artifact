# Metric Definitions

| Metric | Direction | Definition |
|---|---|---|
| Return | Higher is better | Mean episode return under the disclosed evaluation seed schedule. |
| Score | Higher is better | Task score. In the self-contained harness, score equals return. External adapters must define score explicitly. |
| Win rate | Higher is better | Fraction of evaluation episodes ending in task success/win. |
| Steps-to-T | Lower is better | First interval where mean score reaches threshold T, converted by the environment-step cap. Blank/negative means threshold not reached. |
| p95 latency | Lower is better | 95th percentile of per-interval end-to-end charged time. |
| p99 latency | Lower is better | 99th percentile of per-interval end-to-end charged time. |
| Loop overrun rate | Lower is better | Fraction of intervals where charged loop time exceeds the loop budget. |
| E2E overrun rate | Lower is better | Fraction of intervals where charged loop time plus guard margin exceeds the gross interval budget. |
| Diversity value | Diagnostic | Mean behavioral-descriptor dispersion used by the scheduler. |
| Learning progress | Diagnostic | Nonnegative short-horizon progress proxy for the RL module and distillation updates. |
| Improvement rate | Diagnostic | Short-horizon improvement divided by charged atomic-step time. |
| Handshake events | Diagnostic | Count of cross-layer injection/distillation events. |
| Actual CPU E2E ms | Diagnostic | Local Python wall-clock runtime for an interval, logged separately from charged-time accounting. |

## Timing-mode caution

The default `simulated_charged` timing mode is intended to stress the scheduler deterministically. It is not a claim of real engine wall-clock performance. For a journal submission, external benchmark runs should disclose whether timing is simulated charged-time, actual CPU time, or engine-integrated wall-clock time.
