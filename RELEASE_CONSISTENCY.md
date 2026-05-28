# Release Consistency Check

Overall status: **PASS**

Compared against manuscript source in the local working tree: `../../Paper/elsarticle-template-num.tex`

| Check | Status | Detail |
|---|---:|---|
| Paper source exists outside release | PASS | `../../Paper/elsarticle-template-num.tex` |
| No manuscript source in release | PASS | excluded |
| No manuscript PDF in release | PASS | excluded |
| Main local interval rows match manuscript | PASS | computed=16,800 |
| Main local atomic rows match manuscript | PASS | computed=131,718 |
| External Gymnasium interval rows match manuscript | PASS | computed=6,720 |
| External Gymnasium atomic rows match manuscript | PASS | computed=52,687 |
| Raw-CPU timing interval rows match manuscript | PASS | computed=1,500 |
| Raw-CPU timing atomic rows match manuscript | PASS | computed=16,158 |
| Local task count/name match manuscript | PASS | `grid-treasure`, `line-duel`, `resource-defense` |
| External task count/name match manuscript | PASS | `gym-blackjack`, `gym-cliffwalking`, `gym-frozenlake-4x4`, `gym-frozenlake-4x4-deterministic` |
| Raw-CPU profile task count/name match manuscript | PASS | local + Gymnasium + `minigrid-empty-5x5` timing diagnostics |
| Method count matches local/external validations | PASS | 14 methods |
| Timing profile method count matches manuscript | PASS | `DLGPR-full`, `strict-delta-max`, `relaxed-delta-min` |
| Seed counts match manuscript | PASS | local/external=10; timing=5 |
| Strict charged overrun rates are zero | PASS | local and Gymnasium strict loop/E2E overrun rates are 0.0 |
| Strict raw-CPU overrun rates are zero | PASS | timing-profile strict actual CPU overrun rates are 0.0 |
| Relaxed overrun range matches manuscript | PASS | local=58.25--62.75%; Gymnasium=54.17--60.00%; raw CPU=89--100% |
| Holm-adjusted statistical interpretation matches manuscript | PASS | no reported performance comparison remains significant after Holm correction |
| Release version is 0.4.0 in metadata/code | PASS | CITATION, package `__version__`, pyproject, and Zenodo metadata checked |
