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
| Actual CPU loop wall ms | Lower is better for deployment diagnostics | Measured wall-clock duration of the budget-critical atomic-step loop, excluding offline evaluation/logging. |
| Actual CPU E2E ms | Lower is better for deployment diagnostics | Measured budget-critical atomic loop plus the disclosed guard margin, logged separately from simulated charged-time accounting. |
| Wall-clock interval ms | Diagnostic | Script-level interval duration including offline evaluation and logging; not used as the real-time engine budget metric. |
| Holm-adjusted p-value | Lower is stronger evidence | Holm-Bonferroni adjusted paired-test p-value across the reported comparator family. |

## Timing-mode caution

The default `simulated_charged` timing mode is intended to stress the scheduler deterministically. It is not a claim of real engine wall-clock performance. The separate `actual_cpu_raw` timing profile charges measured CPU time without clipping and uses a disclosed 100 ms interval budget. Manuscript text must keep charged-time validation and raw-CPU timing diagnostics separate.
