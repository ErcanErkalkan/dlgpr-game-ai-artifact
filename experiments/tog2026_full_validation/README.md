# ToG-2026-0045 Full Local Validation

This directory stores the full matched-budget local validation run used by the revised manuscript.

## Generation commands

Run from `code_package/`:

```bash
python scripts/run_full_validation.py --full --output ..\experiments\tog2026_full_validation\logs\full_validation
python scripts/analyze_results.py --log-dir ..\experiments\tog2026_full_validation\logs\full_validation --table-dir ..\experiments\tog2026_full_validation\paper\revised\tables --fig-dir ..\experiments\tog2026_full_validation\paper\revised\figures
python scripts/make_manuscript_assets.py --log-dir ..\experiments\tog2026_full_validation\logs\full_validation --table-dir ..\experiments\tog2026_full_validation\paper\revised\tables --fig-dir ..\experiments\tog2026_full_validation\paper\revised\figures --out-dir ..\experiments\tog2026_full_validation\paper\revised\manuscript_assets
python scripts/audit_package.py --log-dir ..\experiments\tog2026_full_validation\logs\full_validation
```

## Run summary

- Interval log rows: 16,800
- Atomic-step log rows: 131,718
- Tasks: `line-duel`, `grid-treasure`, `resource-defense`
- Methods: 14, including core baselines, scheduler baselines, ablations, strict timing, and relaxed timing
- Seeds: 10
- Planning intervals per run: 40
- Step 4 coverage audit: `STEP4_EXPERIMENT_AUDIT.md`

## Claim boundary

These logs support implementation-level claims about matched-budget accounting, metadata completeness, scheduler behavior, ablation plumbing, and strict-versus-relaxed timing. They do not establish broad performance generalization to GVGAI, MicroRTS, Procgen, OpenSpiel, or other external Game AI benchmarks.
