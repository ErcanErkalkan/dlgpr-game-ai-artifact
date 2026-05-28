# ToG-2026-0045 Raw-CPU Timing Profile

This directory stores the raw-CPU timing diagnostic used by the revised manuscript.

## Generation commands

Run from `code_package/`:

```bash
python scripts/run_timing_profile.py --full
python scripts/analyze_results.py --log-dir ../experiments/tog2026_timing_profile/logs/timing_profile --table-dir ../experiments/tog2026_timing_profile/paper/revised/tables --fig-dir ../experiments/tog2026_timing_profile/paper/revised/figures
python scripts/make_manuscript_assets.py --log-dir ../experiments/tog2026_timing_profile/logs/timing_profile --table-dir ../experiments/tog2026_timing_profile/paper/revised/tables --fig-dir ../experiments/tog2026_timing_profile/paper/revised/figures --out-dir ../experiments/tog2026_timing_profile/paper/revised/manuscript_assets
python scripts/audit_package.py --log-dir ../experiments/tog2026_timing_profile/logs/timing_profile --table-dir ../experiments/tog2026_timing_profile/paper/revised/tables --out ../experiments/tog2026_timing_profile/PACKAGE_AUDIT_REPORT.md
```

## Run summary

- Interval log rows: 1,500
- Atomic-step log rows: 16,158
- Tasks: `line-duel`, `resource-defense`, `gym-frozenlake-4x4`, `gym-cliffwalking`, `minigrid-empty-5x5`
- Methods: `DLGPR-full`, `strict-delta-max`, `relaxed-delta-min`
- Seeds: 5
- Planning intervals per run: 20
- Timing mode: `actual_cpu_raw`
- Budget: `B_tau_ms=100`, loop budget `90`, guard `10`, `delta_max=40`
- Audit report: `PACKAGE_AUDIT_REPORT.md`

## Claim boundary

These logs support measured-CPU timing diagnostics for the strict and relaxed stopping rules. They are not the main performance validation because the budget and rollout horizon differ from the 24 ms charged-time validation.
