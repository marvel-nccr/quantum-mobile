# mini-ASESMA school 2026

> [!IMPORTANT]
> If something you need is missing, or you encounter any bugs, raise an issue via the following link:
> 
> https://github.com/marvel-nccr/quantum-mobile/issues/new?template=mini-asesma.md

## Installation

Download the OVA matching your architecture from Google drive:

https://drive.google.com/drive/folders/1JGBqjOIx96TXVBnjkBF3mXef8L8bnGRI

- Apple Silicon Mac (M1/M2/M3/M4): `quantum_mobile_2026_arm64.ova`
- Intel/AMD laptop (Linux/Windows/Intel Mac): `quantum_mobile_2026_x86_64.ova`

Install VirtualBox 7.2.6 or later from https://www.virtualbox.org/wiki/Downloads. Match your host OS.

Import the VM.
Typically: just double click from your file browser. Alternatively:

1. Open VirtualBox → File → Import Appliance.
2. Select the .ova file. Click Next → Finish. Import takes a few minutes.
3. Select the new VM in the sidebar → Start.

## What's available

Codes (on `PATH`, run from any terminal):
- Quantum ESPRESSO 7.5: `pw.x`, `ph.x`, `pp.x`, ...
- Siesta 5.4.2: `siesta`, `tbtrans`, `vibra`, ...

Python notebook environment — double-click the JupyterLab icon on the desktop. A terminal opens, JupyterLab starts, browser launches automatically. The `Python (asesma)` kernel includes `numpy`, `scipy`, `matplotlib`, `ase`, `dftpy`, and `qepy`.

You can also start the environment from the terminal:

```console
workon asesma
```

## Course materials

Materials live in `~/materials/` (cloned from `asesma-org/miniASESMA2026`).
Pull fresh upstream material at any time:

```console
update
```

Your local edits are preserved; the command rebases upstream changes on top.
If the `.ansible/` playbook bundled in the repo changed, `update` also replays
it to apply system-level fixes (new packages, file tweaks) to the running VM.

## Known limits

- QEpy on Apple Silicon (arm64 image): built from source against QE 7.2 (separate from the system QE 7.5). Slower to provision but _should_ work the same: **test carefully!**
- VirtualBox graphics: if the desktop looks distorted, set Display → Graphics Controller to VBoxSVGA in the VM settings.

## Resources

- VM specs by default: 2 CPUs, 2 GB RAM. Bump in VirtualBox → Settings → System if your machine has the headroom.
