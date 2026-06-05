#!/usr/bin/env python3
"""Converts a .firm file to .nds by prepending header.bin."""

import argparse
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
    parser = argparse.ArgumentParser(
        description="Converts a .firm file to .nds by prepending header.bin.",
    )
    parser.add_argument(
        "input",
        help="path to the input .firm file",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="path to the output .nds file (default: input name with .nds extension)",
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="use header_dev.bin instead of header.bin (for 3DS dev consoles)",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    firm_path = args.input
    nds_path = args.output if args.output else os.path.splitext(firm_path)[0] + ".nds"

    out_dir = os.path.dirname(nds_path)
    if out_dir and not os.path.isdir(out_dir):
        sys.exit(f"Error: output directory does not exist: {out_dir}")

    header_path = HEADER_DEV_PATH if args.dev else HEADER_PATH
    convert(firm_path, nds_path, header_path)


if __name__ == "__main__":
    main()
