import json
import re
import shutil
from os import listdir
from pathlib import Path
from typing import Dict
from rich.console import Console

import typer
from kiutils.symbol import SymbolLib
from unidecode import unidecode


app = typer.Typer()

__file__path = Path(__file__)
# Default paths
repo_root = Path.resolve(__file__path / "../../../")
def_components_path = repo_root / "components"
def_libs_path = repo_root / "kicad-libraries"
def_footprints_path = "footprints"
def_symbols_path = "symbols"
footprit_extenstion = ".kicad_mod"
symbol_lib_extension = ".kicad_sym"
sexp_symbol_start_index = 3
def_kicad_lib = "Hardware Components"

symbol_lib_header = "(kicad_symbol_lib (version 20220914) (generator kicad_symbol_editor))"

err_console = Console(stderr=True)


def to_id(string: str) -> str:
    # optional step, remove accents
    string_2 = unidecode(string)
    string_3 = string_2.lower()
    string_4 = re.sub(r"[^a-z0-9]", " ", string_3)
    string_5 = string_4.strip()
    string_6 = re.sub(r"\s+", "-", string_5)
    return string_6


class KiCadLibManager:
    # Create dict for created libs
    symbols_libs: Dict[str, SymbolLib] = {}

    def copy_footprint(self, footprint: str, libs_path: Path, footprint_lib: str) -> None:
        # Check if footprint exists
        src = repo_root / "kicad-footprints" / to_id(footprint) / (footprint + footprit_extenstion)
        if not Path.exists(src):
            print(f"Footprint: {footprint} does not exist. Skipping")
            return

        # Make sure that destination lib exists
        footprint_lib_path = libs_path / def_footprints_path / footprint_lib
        if not Path.exists(footprint_lib_path):
            Path.mkdir(footprint_lib_path, parents=True)

        # Copy footprint file
        dest = footprint_lib_path / (footprint + footprit_extenstion)

        shutil.copy(src, dest)

    def copy_symbol(self, symbol: str, dest_lib: str, footprint_lib: str) -> None:
        # Check if symbol exists
        src = repo_root / "kicad-symbols" / to_id(symbol) / (symbol + symbol_lib_extension)
        if not Path.exists(src):
            print(f"Symbol: {symbol} does not exist. Skipping")
            return

        # Load symbol as lib
        src_lib = SymbolLib.from_file(str(src))

        # Process symbol and its optional template
        for lib_symbol in src_lib.symbols:
            # Update footprint property
            # Footprint is __always__ third property
            src_footprint = lib_symbol.properties[2].value.split(":")
            if len(src_footprint) == 2:
                src_footprint = src_footprint[1]
            lib_symbol.properties[2].value = f"{footprint_lib}:{src_footprint}"

            # Skip symbols already in lib (filter out duplicate templates)
            if lib_symbol in self.symbols_libs[dest_lib].symbols:
                continue

            self.symbols_libs[dest_lib].symbols.append(lib_symbol)
        return

    def add_component_to_lib(self, component_json: Dict, libs_path: Path) -> None:
        symbol_lib = component_json.get("symbol_lib")
        symbol = component_json.get("symbol")

        footprint_lib = component_json.get("footprint_lib")
        footprint = component_json.get("footprint")

        # If no `lib` is defined for component place it in default symbol lib
        if symbol_lib is None:
            symbol_lib = def_kicad_lib
        symbol_lib_file_name = symbol_lib + symbol_lib_extension
        symbol_lib_path = Path.resolve(libs_path / def_symbols_path / symbol_lib_file_name)

        # Create symbol library if not exists
        if symbol_lib not in self.symbols_libs:
            dest_lib = SymbolLib()
            dest_lib.filePath = str(symbol_lib_path)
            self.symbols_libs[symbol_lib] = dest_lib

        if footprint_lib is None:
            footprint_lib = "Hardware Components Footprints"

        if footprint is not None:
            self.copy_footprint(footprint, libs_path, footprint_lib)

        if symbol is not None:
            self.copy_symbol(symbol, symbol_lib, footprint_lib)


@app.command()
def generate(
    components_path: Path = typer.Option(None, help="Path to KiCad library repository"),
    target_dir: Path = typer.Option(None, help="Path to generated library directory"),
    clean_target_dir: bool = typer.Option(False, help="Remove target dir before generation"),
) -> None:

    # Check if target directory exists, if None use default
    if target_dir is None:
        err_console.print("Unspecified target directory")
        exit(-1)

    if components_path is None:
        components_path = def_components_path
        print(f"Components path is [None]\nDefaulting to [{components_path}]")

    # Check if components directory exists
    if not Path.exists(components_path):
        print(f"Components directory [{components_path}] does not exist! Exit")
        exit(1)

    components_dirs = listdir(Path.resolve(components_path))
    data_json = "data.json"

    if clean_target_dir:
        shutil.rmtree(target_dir)

    # Make sure that target directory is empty or does not exists
    if Path.exists(target_dir):
        target_content = [t_c for t_c in Path.iterdir(target_dir)]
        if len(target_content):
            print(f"Target directory [{target_dir}] is not empty! Exit")
            exit(1)

    lib_manager = KiCadLibManager()

    # Create kicad-libraries/symbol and /footprints directory if they don't exist
    if not Path.exists(target_dir / def_symbols_path):
        Path.mkdir(target_dir / def_symbols_path, parents=True)
    if not Path.exists(target_dir / def_footprints_path):
        Path.mkdir(target_dir / def_footprints_path, parents=True)

    for component in components_dirs:
        component_json = Path.resolve(components_path / component / data_json)
        with open(component_json) as symbol_data:
            lib_manager.add_component_to_lib(json.load(symbol_data), target_dir)

    for lib in lib_manager.symbols_libs:
        lib_manager.symbols_libs[lib].to_file()


if __name__ == "__main__":
    app()
