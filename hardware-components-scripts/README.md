# Antmicro Hardware Components Scripts

Scripts for generating library files for EDA tools.

## Installation

Dependencies: `python3`, `python3-pip`

To install library generator run:

```bash
cd hardware-components-scripts/
python3 -m pip install -e .
```

## Usage

To generate symbol and footprint libraries in KiCad friendly format run:

```bash
hw-library-generator kicad generate --target-dir <libraries_target_directory>
```

The script has following command line options:

```
--target-dir <PATH>         Path to generated library, mandatory.
--components-path <PATH>    Path to KiCad components [default: components/ directory in hardware-components/ repository].
--clean-target-dir          Remove target directory before generation.
--no-clean-target-dir       Do not clean target directory before generation, default.
--help                      Show help message and exit.
```

To use generated libraries in KiCad user needs to configure the library paths. In order to do so open KiCad and follow these instructions for symbols and footprints:

- Symbols:
  - navigate to `Preferences -> Manage Symbol Libraries...`
  - add new entry
  - select generated libraries (`kicad_sym` files), name it freely
  - confirm: `OK`
- Footprints:
  - navigate to `Preferences -> Manage Footprint Libraries...`
  - add new entry
  - select directory with generated footprints (`kicad_mod` files)
  - name it **Hardware Components Footprints**
  - confirm: `OK`
