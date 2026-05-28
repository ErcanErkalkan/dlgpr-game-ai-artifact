#!/usr/bin/env python3
"""Create a zip bundle of logs, tables, figures, and source code."""
from __future__ import annotations

from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = ROOT.parent
OUT = RELEASE_ROOT / "tog2026_dlgpr_submission_artifacts.zip"
INCLUDE = [
    "code_package/dlgpr",
    "code_package/scripts",
    "code_package/tests",
    "code_package/docs",
    "code_package/README.md",
    "code_package/PACKAGE_AUDIT_REPORT.md",
    "code_package/LICENSE",
    "code_package/CITATION.cff",
    "code_package/requirements.txt",
    "code_package/pyproject.toml",
    "experiments/tog2026_full_validation",
    "experiments/tog2026_external_gymnasium",
    "experiments/tog2026_timing_profile",
    "README.md",
    "RELEASE_CONSISTENCY.md",
    "LICENSE",
    "CITATION.cff",
    ".zenodo.json",
]

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for item in INCLUDE:
        p = RELEASE_ROOT / item
        if p.is_file():
            z.write(p, p.relative_to(RELEASE_ROOT))
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file():
                    z.write(f, f.relative_to(RELEASE_ROOT))
print(OUT)
