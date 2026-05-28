# Manuscript Integration Notes

This package generates manuscript-ready conservative text with:

```bash
python scripts/make_manuscript_assets.py
```

Output:

- `paper/revised/manuscript_assets/MANUSCRIPT_INSERTS.md`

Use this file to update the Results and Limitations sections, but preserve the claim boundary: local self-contained tasks are implementation-validation evidence, and the Gymnasium extension supports only the named external tasks that were logged. The artifact still is not GVGAI/MicroRTS/Procgen/OpenSpiel evidence.

## Recommended placement

- Environment-disclosure appendix draft -> Experimental Setup or Appendix.
- Main results narrative -> Results after tables.
- External Gymnasium tables -> bounded external benchmark subsection.
- Raw-CPU timing profile -> separate timing diagnostics subsection.
- Strict vs relaxed timing paragraph -> Timing compliance subsection.
- Claim-boundary paragraph -> Limitations.
- Figure scaffold -> rewrite as figure-specific discussion paragraphs.
