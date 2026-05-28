# Publishing Notes

## GitHub

This directory is the GitHub repository root. The manuscript submission directory `Paper/` is excluded by design.

The repository is connected to:

```bash
https://github.com/ErcanErkalkan/dlgpr-game-ai-artifact.git
```

To push updates:

```bash
git status -sb
git push origin main
```

## Zenodo

Zenodo can archive the GitHub repository after GitHub integration is enabled for this repository. The repository includes `.zenodo.json` so Zenodo can pre-fill title, creator, version, license, keywords, and description.

Before creating the Zenodo release, verify that:

- `CITATION.cff`, `.zenodo.json`, `code_package/pyproject.toml`, and `code_package/dlgpr/__init__.py` all report version `0.4.0`.
- `RELEASE_CONSISTENCY.md` reports `Overall status: PASS`.
- `code_package/PACKAGE_AUDIT_REPORT.md`, `experiments/tog2026_external_gymnasium/PACKAGE_AUDIT_REPORT.md`, and `experiments/tog2026_timing_profile/PACKAGE_AUDIT_REPORT.md` report `Overall status: PASS`.

The manuscript source and manuscript PDF should not be uploaded as part of this artifact unless the journal policy explicitly permits it.
