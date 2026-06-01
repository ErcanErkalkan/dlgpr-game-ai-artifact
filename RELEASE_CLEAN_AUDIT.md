# Release Clean Audit

Official release version: `v0.6.0`

Cleaning actions applied before packaging:

- Removed `.git/` from the distributed archive.
- Removed all `__pycache__/` directories.
- Removed all `*.pyc` and `*.pyo` files.
- Removed Python `*.egg-info` install metadata.
- Removed nested ZIP archives from the distributed tree, including legacy bundle names.
- Regenerated current audit reports after metadata normalization.
- Normalized version metadata across `README.md`, `pyproject.toml`, `code_package/dlgpr/__init__.py`, `CITATION.cff`, `.zenodo.json`, `VERSION`, and the release archive name.

The clean archive should be published from a repository tag named `v0.6.0`. The `.git/` directory is intentionally excluded from the artifact ZIP, so the tag is represented in the metadata and archive name rather than embedded as Git history.
