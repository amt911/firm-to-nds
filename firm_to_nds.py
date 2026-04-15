#!/usr/bin/env python3
"""
firm_to_nds.py - Converts a .firm file to .nds by prepending header.bin.

Usage:
    python firm_to_nds.py [--dev] <input.firm> [output.nds]

Options:
    --dev   Use header_dev.bin instead of header.bin (for 3DS dev consoles)

If no output path is given, the output file will have the same name
as the input but with a .nds extension.
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HEADER_PATH = os.path.join(SCRIPT_DIR, "header.bin")
HEADER_DEV_PATH = os.path.join(SCRIPT_DIR, "header_dev.bin")


def convert(firm_path: str, nds_path: str, header_path: str) -> None:
    header_name = os.path.basename(header_path)

    if not os.path.isfile(header_path):
        sys.exit(f"Error: {header_name} not found at {header_path}")

    if not os.path.isfile(firm_path):
        sys.exit(f"Error: input file not found: {firm_path}")

    with open(header_path, "rb") as f:
        header = f.read()

    with open(firm_path, "rb") as f:
        firm = f.read()

    with open(nds_path, "wb") as f:
        f.write(header)
        f.write(firm)

    total_kb = (len(header) + len(firm)) / 1024
    print(f"OK: {nds_path}  ({total_kb:.1f} KB)")


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--dev"]
    dev_mode = len(args) != len(sys.argv[1:])

    if len(args) < 1:
        print(__doc__.strip())
        sys.exit(1)

    firm_path = args[0]
    if len(args) >= 2:
        nds_path = args[1]
    else:
        nds_path = os.path.splitext(firm_path)[0] + ".nds"

    header_path = HEADER_DEV_PATH if dev_mode else HEADER_PATH
    convert(firm_path, nds_path, header_path)


if __name__ == "__main__":
    main()
