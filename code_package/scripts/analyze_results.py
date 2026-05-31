#!/usr/bin/env python3
"""Analyze generated interval logs and produce manuscript-ready CSV tables and figures.

Official invocation from the artifact root:

    python code_package/scripts/analyze_results.py

Relative CLI paths are interpreted from the artifact root.  The import path is
kept compatible with the official ``code_package`` source layout and with
``pip install -e .``.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_PATH = Path(__file__).resolve()
CODE_ROOT = SCRIPT_PATH.parents[1]
ARTIFACT_ROOT = SCRIPT_PATH.parents[2]
sys.path.insert(0, str(CODE_ROOT))

from dlgpr.analysis import analyze


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return ARTIFACT_ROOT / path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-dir", default="code_package/logs/full_validation")
    parser.add_argument("--table-dir", default="code_package/paper/revised/tables")
    parser.add_argument("--fig-dir", default="code_package/paper/revised/figures")
    args = parser.parse_args()
    outputs = analyze(resolve_path(args.log_dir), resolve_path(args.table_dir), resolve_path(args.fig_dir))
    print("Analysis complete")
    for k, v in outputs.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
