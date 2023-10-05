# Antmicro Hardware Components

Copyright (c) 2023 [Antmicro](https://www.antmicro.com)

This project contains a collection of KiCad components used in open hardware designs made by Antmicro.
Most of the components have design assets provided (3D Blender models, KiCad symbols and footprints).
The current collection consists mainly of components prepared and maintained in KiCad 6.x.

This project is currently a Work-in-Progress.
The project's primary goal is to aggregate a collection of hardware components in a form suitable both for manual and automated (i.e. scriptable) processing.
A secondary goal of this project is to make it browsable through the Antmicro [Open Hardware Portal](https://openhardware.antmicro.com).

## Project structure

The main directory includes this README and a LICENSE file.
There is also a meta.json file which provides generated meta data about file checksums and sizes.
The component-related assets are stored in the following directories:

* [components](components) - this folder includes subfolders with component definitions.
The subfolders are named after a component's manufacturer (MFR) and Manufacturer Part Number (MPN) concatenated with dashes. 
Each subfolder includes component-related assets.
* [kicad-symbols](kicad-symbols) - this folder contains symbol library files in KiCad format (``*.kicad_sym``). Each file represents a single symbol.
* [kicad-footprints](kicad-footprints) - this folder contains footprint definitions in KiCad format (``*.kicad_mod``) files.
* [blender-models](blender-models) - this folder contains component Blender models and its rendered previews.

Each of the component-related assets described above includes JSON files which summarize an asset's definitions in a unified, machine-readable form.
Symbols, footprints, and Blender models common to several components are interconnected to respective component definitions via JSON files or symbolic links.

## License

This project is licensed under the [Apache-2.0](LICENSE) license.
