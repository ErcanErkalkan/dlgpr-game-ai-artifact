# Publishing Notes

## GitHub

This directory is ready to become the GitHub repository root. The `Paper/` directory is excluded.

Recommended repository name:

```bash
dlgpr-game-ai-artifact
```

After logging in with GitHub CLI:

```bash
gh auth login
cd release/dlgpr-game-ai-artifact
git remote add origin https://github.com/<OWNER>/dlgpr-game-ai-artifact.git
git push -u origin main
```

Or create the repository directly with GitHub CLI:

```bash
gh repo create dlgpr-game-ai-artifact --public --source . --remote origin --push
```

Use `--private` instead of `--public` if the artifact should stay private before review.

## Zenodo

Zenodo can archive the GitHub repository after it is public and enabled in Zenodo, or the ZIP archive generated from this directory can be uploaded manually.

The repository includes `.zenodo.json` so Zenodo can pre-fill the title, creator, version, license, keywords, and description.

Recommended archive file:

```bash
dist/dlgpr-game-ai-artifact-v0.3.0.zip
```

For API upload, define `ZENODO_ACCESS_TOKEN` first. Do not commit tokens to this repository.

