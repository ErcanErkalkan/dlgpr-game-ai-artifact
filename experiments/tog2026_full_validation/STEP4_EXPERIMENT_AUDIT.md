# Step 4 Experiment Audit

Target journal: Entertainment Computing

Status: UPDATED TO 16-METHOD ROBUST SOURCE OF TRUTH

## Experiment Directory

- Required directory: `experiments/tog2026_full_validation/`
- Log directory: `experiments/tog2026_full_validation/logs/full_validation/`
- Previous non-robust 14-method logs removed: yes
- Official full-validation interval rows: 19,200
- Official full-validation atomic-step rows: 150,297
- Tasks: `grid-treasure`, `line-duel`, `resource-defense`
- Seeds: 10, `0` through `9`
- Planning intervals per run: 40
- Robust variants present: yes

## Method Coverage

| Method | Status |
|---|---|
| `DLGPR-full` | present |
| `GA-only` | present |
| `PSO-only` | present |
| `RL-only` | present |
| `fixed-split` | present |
| `greedy-improvement` | present |
| `no-diversity` | present |
| `no-handshake` | present |
| `no-learning-progress` | present |
| `no-non-starvation` | present |
| `no-ucb` | present |
| `relaxed-delta-min` | present |
| `robust-DLGPR` | present |
| `robust-near-elite-DLGPR` | present |
| `round-robin` | present |
| `strict-delta-max` | present |

## Required Interval-Log Fields

All required fields are present in `interval_logs.csv`. The robust source-of-truth log has 67 columns and includes method-specific rollout metadata where available.

## Required Atomic-Step Fields

The atomic-step log provides per-step selected module, charged duration, CPU time, scheduler quantities, and remaining-budget fields. The robust source-of-truth atomic log has 20 columns.

## Replacement Verification

See `../LOG_REPLACEMENT_AUDIT.md` for checksum-level verification that the official experiment logs were copied from the robust source directories.
