# Manuscript Integration Notes

This package now generates manuscript-ready conservative text with:

```bash
python scripts/make_manuscript_assets.py
```

Output:

- `paper/revised/manuscript_assets/MANUSCRIPT_INSERTS.md`

Use this file to update the Results and Limitations sections, but preserve the claim boundary: local self-contained tasks are implementation-validation evidence, not a replacement for GVGAI/MicroRTS/Procgen/OpenSpiel evidence.

## Recommended placement

- Environment-disclosure appendix draft → Experimental Setup or Appendix.
- Main results narrative → Results after tables.
- Strict vs relaxed timing paragraph → Timing compliance subsection.
- Claim-boundary paragraph → Limitations.
- Figure scaffold → rewrite as figure-specific discussion paragraphs.
