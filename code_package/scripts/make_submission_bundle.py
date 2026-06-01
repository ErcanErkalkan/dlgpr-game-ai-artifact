#!/usr/bin/env python3
"""Create public and double-anonymized review bundles for the artifact."""
from __future__ import annotations

from pathlib import Path
import zipfile

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
RELEASE_ROOT = SCRIPT_PATH.parents[2]
VERSION = (RELEASE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
OUT = RELEASE_ROOT.parent / f"dlgpr-game-ai-artifact-{VERSION}.zip"
ANONYMOUS_OUT = RELEASE_ROOT.parent / f"dlgpr-game-ai-anonymous-artifact-{VERSION}.zip"
PUBLIC_INCLUDE = [
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "LICENSE",
    "CITATION.cff",
    ".zenodo.json",
    "VERSION",
    "RELEASE_CONSISTENCY.md",
    "RELEASE_CLEAN_AUDIT.md",
    "ZENODO_NEW_VERSION_UPLOAD.md",
    "Dockerfile",
    "Makefile",
    "code_package/dlgpr",
    "code_package/scripts",
    "code_package/tests",
    "code_package/docs",
    "code_package/configs",
    "experiments/SOURCE_OF_TRUTH.md",
    "experiments/LOG_REPLACEMENT_AUDIT.md",
    "experiments/tog2026_full_validation",
    "experiments/tog2026_external_gymnasium",
    "experiments/tog2026_timing_profile",
    "experiments/ec2026_compute_matched_rollout",
    "experiments/ec2026_minigrid_performance",
]
ANONYMOUS_INCLUDE = [
    "requirements.txt",
    "pyproject.toml",
    "Dockerfile",
    "Makefile",
    "code_package/dlgpr",
    "code_package/scripts",
    "code_package/tests",
    "code_package/docs",
    "code_package/configs",
    "experiments/SOURCE_OF_TRUTH.md",
    "experiments/LOG_REPLACEMENT_AUDIT.md",
    "experiments/tog2026_full_validation",
    "experiments/tog2026_external_gymnasium",
    "experiments/tog2026_timing_profile",
    "experiments/ec2026_compute_matched_rollout",
    "experiments/ec2026_minigrid_performance",
]
ANONYMOUS_README = """# DLGPR Game AI Artifact

This anonymized review artifact accompanies the Entertainment Computing
submission. It contains the implementation, tests, metadata-complete logs,
generated tables, figures, and audit documentation used for the reported
results.

The archival repository identifier, public source mirror, author metadata, and
version metadata are intentionally omitted during double-anonymized review.

## Validation

Run from the extracted artifact root:

```bash
python -m pip install -e .
python code_package/tests/run_tests.py
python code_package/scripts/audit_package.py --profile full --out experiments/tog2026_full_validation/PACKAGE_AUDIT_REPORT.md
python code_package/scripts/audit_package.py --profile external --log-dir experiments/tog2026_external_gymnasium/logs/external_validation --table-dir experiments/tog2026_external_gymnasium/paper/revised/tables --out experiments/tog2026_external_gymnasium/PACKAGE_AUDIT_REPORT.md
python code_package/scripts/audit_package.py --profile timing --log-dir experiments/tog2026_timing_profile/logs/timing_profile --table-dir experiments/tog2026_timing_profile/paper/revised/tables --out experiments/tog2026_timing_profile/PACKAGE_AUDIT_REPORT.md
python code_package/scripts/audit_package.py --profile compute-matched --log-dir experiments/ec2026_compute_matched_rollout/logs/compute_matched_rollout --table-dir experiments/ec2026_compute_matched_rollout/paper/revised/tables --out experiments/ec2026_compute_matched_rollout/PACKAGE_AUDIT_REPORT.md
python code_package/scripts/audit_package.py --profile minigrid-performance --log-dir experiments/ec2026_minigrid_performance/logs/minigrid_performance --table-dir experiments/ec2026_minigrid_performance/paper/revised/tables --out experiments/ec2026_minigrid_performance/PACKAGE_AUDIT_REPORT.md
```

Expected result: 17 tests pass and all five audit profiles report `PASS`.
"""
ANONYMOUS_LICENSE = (RELEASE_ROOT / "LICENSE").read_text(encoding="utf-8").replace(
    "Ercan Erkalkan", "Anonymous Author(s)"
)

def _is_forbidden(path: Path) -> bool:
    parts = set(path.parts)
    if ".git" in parts or "__pycache__" in parts or ".pytest_cache" in parts:
        return True
    if path.suffix in {".pyc", ".pyo", ".zip"}:
        return True
    if any(part.endswith(".egg-info") for part in path.parts):
        return True
    return False


def _write_items(z: zipfile.ZipFile, include: list[str], anonymous: bool = False) -> None:
    for item in include:
        p = RELEASE_ROOT / item
        if not p.exists():
            print(f"warning: missing bundle input: {item}")
            continue
        if _is_forbidden(p):
            continue
        if p.is_file():
            z.write(p, p.relative_to(RELEASE_ROOT))
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and not _is_forbidden(f):
                    if anonymous and f.name == "make_submission_bundle.py":
                        continue
                    if anonymous and f.name in {
                        ".zenodo.json",
                        "CITATION.cff",
                        "VERSION",
                        "RELEASE_CONSISTENCY.md",
                        "RELEASE_CLEAN_AUDIT.md",
                    }:
                        continue
                    z.write(f, f.relative_to(RELEASE_ROOT))


with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    _write_items(z, PUBLIC_INCLUDE)
print(OUT)

with zipfile.ZipFile(ANONYMOUS_OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.md", ANONYMOUS_README)
    z.writestr("LICENSE", ANONYMOUS_LICENSE)
    _write_items(z, ANONYMOUS_INCLUDE, anonymous=True)
print(ANONYMOUS_OUT)
