# Duplicate Method Validation

The audit checks behavioral equivalence on interval-level performance, timing, allocation, and overrun columns while ignoring method labels, run identifiers, timestamps, and metadata fields that are expected to differ by label.

| Pair | Rows A | Rows B | Behavioral equality on checked columns | Mismatches |
|---|---:|---:|---|---|
| `DLGPR-full vs strict-delta-max` | 1200 | 1200 | yes | none |
| `fixed-split vs round-robin` | 1200 | 1200 | yes | none |

> These pairs are behaviorally equivalent under the reported configuration.

The labels are retained for traceability and timing/scheduler taxonomy, not as independent algorithmic baselines.
