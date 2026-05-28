# ToG-2026-0045 External Gymnasium Validation

This directory stores the matched-budget external benchmark extension used by the revised manuscript.

## Generation commands

Run from `code_package/`:

```bash
python scripts/run_external_validation.py --full
python scripts/analyze_results.py --log-dir ../experiments/tog2026_external_gymnasium/logs/external_validation --table-dir ../experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir ../experiments/tog2026_external_gymnasium/paper/revised/figures
python scripts/make_manuscript_assets.py --log-dir ../experiments/tog2026_external_gymnasium/logs/external_validation --table-dir ../experiments/tog2026_external_gymnasium/paper/revised/tables --fig-dir ../experiments/tog2026_external_gymnasium/paper/revised/figures --out-dir ../experiments/tog2026_external_gymnasium/paper/revised/manuscript_assets
python scripts/audit_package.py --log-dir ../experiments/tog2026_external_gymnasium/logs/external_validation --table-dir ../experiments/tog2026_external_gymnasium/paper/revised/tables --out ../experiments/tog2026_external_gymnasium/PACKAGE_AUDIT_REPORT.md
```

## Run summary

- Interval log rows: 6,720
- Atomic-step log rows: 52,687
- Tasks: `gym-frozenlake-4x4`, `gym-frozenlake-4x4-deterministic`, `gym-cliffwalking`, `gym-blackjack`
- Methods: 14, including core baselines, scheduler baselines, ablations, strict timing, and relaxed timing
- Seeds: 10
- Planning intervals per run: 12
- Audit report: `PACKAGE_AUDIT_REPORT.md`

## Claim boundary

These logs support named-task external adapter evidence and strict charged-time timing checks. They do not establish broad performance generalization to GVGAI, MicroRTS, Procgen, OpenSpiel, or MiniGrid.
