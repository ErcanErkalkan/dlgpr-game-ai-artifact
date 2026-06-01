# Log Replacement Audit
Status: PASS for requested log replacement.
The previous non-robust 14-method logs were removed from the official experiment directories and replaced with the robust source-of-truth logs.
## Official full validation
- Path: `experiments/tog2026_full_validation/logs/full_validation/`
- Interval rows: 19,200
- Atomic rows: 150,297
- Methods: 16
- Robust methods present: yes
- Method list: `DLGPR-full`, `GA-only`, `PSO-only`, `RL-only`, `fixed-split`, `greedy-improvement`, `no-diversity`, `no-handshake`, `no-learning-progress`, `no-non-starvation`, `no-ucb`, `relaxed-delta-min`, `robust-DLGPR`, `robust-near-elite-DLGPR`, `round-robin`, `strict-delta-max`

## Official external validation
- Path: `experiments/tog2026_external_gymnasium/logs/external_validation/`
- Interval rows: 3,840
- Atomic rows: 29,698
- Methods: 8
- Robust methods present: yes
- Method list: `DLGPR-full`, `fixed-split`, `greedy-improvement`, `no-handshake`, `no-non-starvation`, `robust-DLGPR`, `robust-near-elite-DLGPR`, `round-robin`

## Copy checks
| Item | Exact source copy | SHA-256 of official target |
|---|---:|---|
| full interval logs | yes | `162cac37296f7be06187975e231baf0cda7ec7fec178104d769b1abcbe578f12` |
| full atomic logs | yes | `a30e765039d1282c692107d3dc74c48d52fb03abd38660ce6e5b9ab01cc7e2e7` |
| full environment metadata | yes | `a63c6eb05a6b9a495d111879b59c1ccf6eb0ab00b451f847fe48edbdf9e6a40a` |
| external interval logs | yes | `9b9f0f09eb893cf8a46c00eb24a53981aa280e1005ff3de957c44e74ee375908` |
| external atomic logs | yes | `608eabd4748e37f30b173baa91c2ccfa2e6ac2051b226eeecf07483638d18d42` |
| external environment metadata | yes | `94bf99430282c9e0cbe4f47bdfd1890ca7b6668774f6803c0afdff33f9fedf3b` |

## Notes
- This audit verifies the requested log replacement only. It does not claim that the package-level audit script is fixed.
- The root README and experiment READMEs were updated to remove stale 14-method row counts.

## v0.6.0 supplementary compute-matched logs

The immutable replacement audit above remains valid. Version `v0.6.0` adds:

- `experiments/ec2026_compute_matched_rollout/`: 9,600 interval rows and
  134,027 atomic rows under rollout-equivalent online accounting.
- `experiments/ec2026_minigrid_performance/`: 960 interval rows and 13,543
  atomic rows for the fully observable MiniGrid Empty-5x5 integration.

These supplementary logs are audited separately by `audit_package.py` profiles
`compute-matched` and `minigrid-performance`.


## Method-equivalence note

These pairs are behaviorally equivalent under the reported configuration: `DLGPR-full` / `strict-delta-max`, and `fixed-split` / `round-robin`. The logs preserve scheduler labels for traceability; they should not be counted as independent algorithmic baselines.
