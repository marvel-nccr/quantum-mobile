# MARVEL-ICTP QE School 2026

> [!IMPORTANT]
> If something you need is missing, or you encounter any bugs, raise an issue via the following link:
>
> https://github.com/marvel-nccr/quantum-mobile/issues/new?template=marvel-ictp-school.md

## Installation

Download the OVA matching your architecture from Google drive:

https://drive.google.com/drive/folders/1xSy4f8rbx04Lm1CV9kWCVbl8t2BPjxkA

- Apple Silicon Mac (M1/M2/M3/M4): `quantum_mobile_2026_arm64.ova`
- Intel/AMD laptop (Linux/Windows/Intel Mac): `quantum_mobile_2026_x86_64.ova`

Install VirtualBox 7.2.6 or later from https://www.virtualbox.org/wiki/Downloads. Match your host OS.

Import the VM.
Typically: just double click from your file browser. Alternatively:

1. Open VirtualBox → File → Import Appliance.
2. Select the .ova file. Click Next → Finish. Import takes a few minutes.
3. Select the new VM in the sidebar → Start.

## Workshop conda environments

Six pre-installed envs, one per session. Activate any of them in a terminal with `workon <env>` (tab-completion works):

- `koopmans` — Koopmans toolchain (built from source: KCP, QE `pw`/`pp`/`kcw`, utils)
- `metatomic` — LAMMPS (`lmp`) patched for ML potentials, plus `i-pi`, `chemiscope`, `flashmd`, `metatrain`, `upet`, py3Dmol
- `qe` — Quantum ESPRESSO 7.5 with `ase`, `numpy`, `matplotlib`, `spglib`
- `wannier` — Wannier90 3.1.0 with `pythtb` and `tbmodels`
- `yambo` — Yambo 5.3.0 with `yambopy`
- `sscha` — `cellconstructor`, `python-sscha`, `tdscha`, plus Julia 1.12.5 wired through the PyCall.jl bridge

### What's available without activating

A few binaries are exposed on `$PATH` directly so you can run them from any cwd:

- Quantum ESPRESSO: `pw.x`, `ph.x`, `pp.x`, ... (from the `qe` env)
- Wannier90: `wannier90.x`, `w90*`, `postw90.*` (from the `wannier` env)

For everything else (LAMMPS, Yambo, sscha, koopmans, ...) activate the matching env first.

## JupyterLab

Double-click the JupyterLab icon on the desktop. A terminal opens, JupyterLab starts, and the browser launches automatically. To stop the server, press `Ctrl+C` in the terminal window.

Each workshop env is registered as a Jupyter kernel — pick `Python (qe)`, `Python (metatomic)`, `Python (wannier)`, `Python (yambo)`, `Python (sscha)`, or `Python (koopmans)` from the launcher.

## Resources

- VM specs by default: 2 CPUs, 2 GB RAM. Bump in VirtualBox → Settings → System if your machine has the headroom.
