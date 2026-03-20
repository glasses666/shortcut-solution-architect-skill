#!/usr/bin/env python3
"""Wrap `shortcuts sign` with basic checks."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Input shortcut payload path")
    parser.add_argument("--output", required=True, help="Signed output path")
    parser.add_argument("--mode", choices=("anyone", "people-who-know-me"), default="people-who-know-me")
    args = parser.parse_args()

    if shutil.which("shortcuts") is None:
        print("shortcuts CLI not found on PATH", file=sys.stderr)
        return 2

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "shortcuts",
        "sign",
        "--mode",
        args.mode,
        "--input",
        str(input_path),
        "--output",
        str(output_path),
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr)
        return completed.returncode

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
