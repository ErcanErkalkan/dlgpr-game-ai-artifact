#!/usr/bin/env python3
"""Analyze generated interval logs and produce manuscript-ready CSV tables and figures."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dlgpr.analysis import analyze


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-dir", default="logs/full_validation")
    parser.add_argument("--table-dir", default="paper/revised/tables")
    parser.add_argument("--fig-dir", default="paper/revised/figures")
    args = parser.parse_args()
    outputs = analyze(ROOT / args.log_dir, ROOT / args.table_dir, ROOT / args.fig_dir)
    print("Analysis complete")
    for k, v in outputs.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
