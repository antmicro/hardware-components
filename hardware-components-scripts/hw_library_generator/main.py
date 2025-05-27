import typer

import hw_library_generator.kicad_lib_generator as kicad_generator

app = typer.Typer()
app.add_typer(
    kicad_generator.app,
    name="kicad",
    help="Generate and manage KiCad library",
)


if __name__ == "__main__":
    app()
