# Manuscript Integration Notes

This package generates manuscript-ready conservative text with the root-relative command:

```bash
python code_package/scripts/make_manuscript_assets.py
```

Default output:

- `code_package/paper/revised/manuscript_assets/MANUSCRIPT_INSERTS.md`

For the manuscript-consistent full-validation assets, run from the artifact root:

```bash
python code_package/scripts/make_manuscript_assets.py --log-dir experiments/tog2026_full_validation/logs/full_validation --table-dir experiments/tog2026_full_validation/paper/revised/tables --fig-dir experiments/tog2026_full_validation/paper/revised/figures --out-dir experiments/tog2026_full_validation/paper/revised/manuscript_assets
```

Use this file to update the Results and Limitations sections, but preserve the claim boundary: local self-contained tasks are implementation-validation evidence, and the Gymnasium extension supports only the named external tasks that were logged. The artifact still is not GVGAI/MicroRTS/Procgen/OpenSpiel evidence.

## Recommended placement

- Environment-disclosure appendix draft -> Experimental Setup or Appendix.
- Main results narrative -> Results after tables.
- Robust-DLGPR and robust-near-elite-DLGPR -> Proposed Method and ablation/sensitivity subsections. State that robust variants use `atomic_eval_rollouts = K` for atomic candidate scoring.
- Aggregate-vs-DLGPR table -> empirical summary paragraph only; do not use it to override per-task statistical tests.
- External Gymnasium tables -> bounded external benchmark subsection.
- Raw-CPU timing profile -> separate timing diagnostics subsection.
- Strict vs relaxed timing paragraph -> Timing compliance subsection.
- Claim-boundary paragraph -> Limitations.
- Figure scaffold -> rewrite as figure-specific discussion paragraphs.


## Method-equivalence disclosure

See `METHOD_EQUIVALENCE.md`. These pairs are behaviorally equivalent under the reported configuration: `DLGPR-full` / `strict-delta-max`, and `fixed-split` / `round-robin`. They are retained as diagnostic labels, not independent baselines.
