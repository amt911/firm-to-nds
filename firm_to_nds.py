#!/usr/bin/env python3
"""
firm_to_nds.py - Converts a .firm file to .nds by prepending header.bin.

Usage:
    python firm_to_nds.py <input.firm> [output.nds]

If no output path is given, the output file will have the same name
as the input but with a .nds extension.
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HEADER_PATH = os.path.join(SCRIPT_DIR, "header.bin")


def convert(firm_path: str, nds_path: str) -> None:
    if not os.path.isfile(HEADER_PATH):
        sys.exit(f"Error: header.bin not found at {HEADER_PATH}")

    if not os.path.isfile(firm_path):
        sys.exit(f"Error: input file not found: {firm_path}")

    with open(HEADER_PATH, "rb") as f:
        header = f.read()

    with open(firm_path, "rb") as f:
        firm = f.read()

    with open(nds_path, "wb") as f:
        f.write(header)
        f.write(firm)

    total_kb = (len(header) + len(firm)) / 1024
    print(f"OK: {nds_path}  ({total_kb:.1f} KB)")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    firm_path = sys.argv[1]
    if len(sys.argv) >= 3:
        nds_path = sys.argv[2]
    else:
        nds_path = os.path.splitext(firm_path)[0] + ".nds"

    convert(firm_path, nds_path)


if __name__ == "__main__":
    main()
