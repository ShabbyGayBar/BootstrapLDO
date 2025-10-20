# Bootstrap LDO

## Overview

This repository contains the design, simulation files, scripts, and documentation for a low-dropout (LDO) voltage regulator with a bootstrap circuit to enhance power supply rejection ratio (PSRR) performance at low supply voltages.

This is a course project for 2025-1-ECEN7020-001 ADVANCED TOPICS IN ANALOG AND MIXED-SIGNAL INTEGRATED CIRCUITS at the University of Macau.

## Repository Structure

- `assets/`: Contains simulation data `csv` files such as waveforms and regulation performance metrics as well as a [bootstrap_ldo.vsdx](assets/bootstrap_ldo.vsdx) visio diagram file containing the circuit schematics in the report.
- `documentation/`: Includes the main report pdf([`main.pdf`](documentation/main.pdf)), typst source code ([`main.typ`](documentation/main.typ)) and references ([`refs.bib`](documentation/refs.bib)) detailing the design and analysis of the bootstrap LDO.
- `figures/`: Stores figures used in the documentation and analysis.
- `scripts/`: Contains Python scripts for generating plots and analyzing simulation results.

## License

This project is licensed under the terms of the MIT License. See the [`LICENSE`](LICENSE) file for details.
