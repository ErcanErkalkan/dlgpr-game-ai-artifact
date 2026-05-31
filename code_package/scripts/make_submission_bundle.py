#!/usr/bin/env python3
"""Create a zip bundle of logs, tables, figures, and source code."""
from __future__ import annotations

from pathlib import Path
import zipfile

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
RELEASE_ROOT = SCRIPT_PATH.parents[2]
OUT = RELEASE_ROOT.parent / "dlgpr-game-ai-artifact-v0.5.0.zip"
INCLUDE = [
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "LICENSE",
    "CITATION.cff",
    ".zenodo.json",
    "VERSION",
    "RELEASE_CONSISTENCY.md",
    "RELEASE_CLEAN_AUDIT.md",
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
]

def _is_forbidden(path: Path) -> bool:
    parts = set(path.parts)
    if ".git" in parts or "__pycache__" in parts or ".pytest_cache" in parts:
        return True
    if path.suffix in {".pyc", ".pyo", ".zip"}:
        return True
    if any(part.endswith(".egg-info") for part in path.parts):
        return True
    return False


with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for item in INCLUDE:
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
                    z.write(f, f.relative_to(RELEASE_ROOT))
print(OUT)
