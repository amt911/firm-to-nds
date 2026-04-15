# firm-to-nds

Tool to convert `.firm` (binary firmware) files to `.nds` format by prepending the required header.

## Description

This script takes a `.firm` file and generates an `.nds` file by automatically adding `header.bin` to the beginning. It's useful for preparing Nintendo DS/DSi firmware for use on official development flashcards (DSPico and other compatible devices).

## Requirements

- Python 3.6 or higher
- The `header.bin` file must be in the same directory as the script
- For 3DS dev consoles, `header_dev.bin` must also be present in the same directory

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/amt911/firm-to-nds.git
   cd firm-to-nds
   ```

2. Verify that `header.bin` is present in the directory.

## Usage

### Basic syntax

```bash
python firm_to_nds.py [--dev] <input_file.firm> [output_file.nds]
```

### Options

| Option       | Description                                                        |
|--------------|--------------------------------------------------------------------|
| `-h, --help` | Show the help message and exit                                     |
| `--dev`      | Use `header_dev.bin` instead of `header.bin` (for 3DS dev consoles) |

### Examples

**Automatic conversion** (creates `firmware.nds` in the same directory):
```bash
python firm_to_nds.py firmware.firm
```

**Specify output file**:
```bash
python firm_to_nds.py firmware.firm my_output.nds
```

**On Windows**:
```cmd
python firm_to_nds.py C:\roms\firmware.firm C:\output\firmware.nds
```

**For 3DS dev consoles** (uses `header_dev.bin`):
```bash
python firm_to_nds.py --dev firmware.firm
```

### Help

Without arguments (or with `-h` / `--help`), the script displays help:
```bash
python firm_to_nds.py
python firm_to_nds.py --help
```

## Project structure

```
firm-to-nds/
├── header.bin          # Binary header prepended to the output
├── header_dev.bin      # Alternative header for 3DS dev consoles
├── firm_to_nds.py      # Conversion script
└── README.md           # This file
```

## How it works

The process is simple:

1. Reads the contents of `header.bin`
2. Reads the contents of the specified `.firm` file
3. Writes a new `.nds` file by concatenating: `header.bin` + `firmware.firm`

```
[header.bin] + [input.firm] = [output.nds]
```

## Notes

- The script looks for `header.bin` (or `header_dev.bin` when using `--dev`) in the same directory where it's located, regardless of where you run it from.
- If the output file already exists, it will be overwritten without confirmation.
- The script displays the total size of the generated file upon completion.

## Compatibility

Cross-platform: works on Windows, Linux, and macOS without external dependencies.

## License

This project is open source. Feel free to use and modify it according to your needs.

## Author

[@amt911](https://github.com/amt911)
