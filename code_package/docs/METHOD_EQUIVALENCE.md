# Method-equivalence disclosure

This artifact keeps the 16 local scheduler labels used by the manuscript source-of-truth logs so that row counts, run identifiers, and generated tables remain traceable. However, two label pairs are **not** presented as independent behavioral methods.

> These pairs are behaviorally equivalent under the reported configuration.

## Equivalent diagnostic pairs

| Pair | Status | Why this is not an independent method comparison |
|---|---|---|
| `DLGPR-full` vs `strict-delta-max` | Timing-rule alias | In the reported local configuration, `DLGPR-full` already uses the strict `delta_max` do-not-start rule. The `strict-delta-max` label is retained as a timing diagnostic label, not as a separate algorithmic baseline. |
| `fixed-split` vs `round-robin` | Static-allocation alias | In the reported configuration, the fixed-split pattern cycles `GA -> PSO -> RL`, matching the round-robin scheduler. The labels are retained to make the scheduler taxonomy explicit, not to inflate the number of independent baselines. |

## Reporting policy

- The full local validation contains `19,200` interval rows, `150,297` atomic-step rows, and `16` logged scheduler labels.
- Because of the two equivalence pairs above, the local suite should be described as **16 scheduler labels with two behaviorally equivalent diagnostic pairs**, not as 16 independent algorithms.
- When counting behaviorally distinct local configurations, the conservative count is **14 behaviorally distinct configurations**.
- The external robust validation contains `8` logged scheduler labels and also includes the `fixed-split` / `round-robin` static-allocation equivalence pair.

The machine-readable version of this disclosure is `table_method_equivalence.csv` in the generated table directories.
