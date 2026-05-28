# Release Consistency Check

Overall status: **PASS**

Compared against manuscript source in the local working tree: `../../Paper/elsarticle-template-num.tex`

| Check | Status | Detail |
|---|---:|---|
| Paper source exists outside release | PASS | `../../Paper/elsarticle-template-num.tex` |
| No manuscript source in release | PASS | excluded |
| No manuscript PDF in release | PASS | excluded |
| Interval rows match manuscript | PASS | computed=16800, manuscript_has_16,800=True |
| Atomic rows match manuscript | PASS | computed=131718, manuscript_has_131,718=True |
| Task count/name match manuscript | PASS | ['grid-treasure', 'line-duel', 'resource-defense'] |
| Method count matches manuscript | PASS | computed=14 |
| Seed count matches manuscript | PASS | computed=10 |
| Interval count matches manuscript | PASS | computed=40 |
| Evaluation rollout statement present | PASS | manuscript wording found |
| Strict overrun rates are zero | PASS | [{'task_name': 'grid-treasure', 'loop_overrun_rate_down': 0.0, 'e2e_overrun_rate_down': 0.0}, {'task_name': 'line-duel', 'loop_overrun_rate_down': 0.0, 'e2e_overrun_rate_down': 0.0}, {'task_name': 'resource-defense', 'loop_overrun_rate_down': 0.0, 'e2e_overrun_rate_down': 0.0}] |
| Relaxed overrun range matches abstract | PASS | computed=58.25--62.75% |
| Strict/relaxed table values appear in manuscript | PASS | all rounded values found |
| All manuscript-result figures are in release artifact | PASS | 12 figures present |
| Release version is 0.3.0 in metadata/code | PASS | CITATION, package __version__, Zenodo metadata checked |
