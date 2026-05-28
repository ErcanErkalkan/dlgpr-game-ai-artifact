#!/usr/bin/env python3
"""Create a zip bundle of logs, tables, figures, and source code."""
from __future__ import annotations

from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / "tog2026_dlgpr_submission_artifacts.zip"
INCLUDE = ["dlgpr", "scripts", "tests", "docs", "configs", "logs/full_validation", "paper/revised", "README.md", "RUN_REPORT.md", "FIXES_APPLIED.md", "PACKAGE_AUDIT_REPORT.md", "LICENSE", "CITATION.cff", "requirements.txt", "pyproject.toml"]

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for item in INCLUDE:
        p = ROOT / item
        if p.is_file():
            z.write(p, p.relative_to(ROOT.parent))
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file():
                    z.write(f, f.relative_to(ROOT.parent))
print(OUT)
