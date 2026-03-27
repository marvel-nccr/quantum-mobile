# Changelog

## Quantum Mobile v26.03

### Highlights

✨ **ARM64 / Apple Silicon support.** Quantum Mobile now builds and runs natively on ARM64 hardware (Apple Silicon Macs, ARM64 Linux).
NWChem, Quantum ESPRESSO, Yambo, Siesta, and Wannier90 are available on both `x86_64` and `aarch64`.
ABINIT, BigDFT, CP2K, and Fleur remain `x86_64`-only for now (pending conda-forge feedstock support).

📦 **Updated simulation codes.** All codes updated to their latest conda-forge versions, with explicit dependency pins for reproducible builds:

| Code | Version | libxc | MPI |
|------|---------|-------|-----|
| ABINIT | 10.0.3 | 4.3.4 | mpich 4.3.2 |
| BigDFT | 1.9.5 | 4.3.4 | mpich 4.3.2 |
| CP2K | 2024.2 | 6.2.2 | openmpi 4.1.6 |
| Fleur | 8.0 | — | openmpi 5.0.8 |
| NWChem | 7.3.1 | 7.0.0 | openmpi 5.0.8 |
| Quantum ESPRESSO | 7.5 | — | openmpi 5.0.8 |
| Siesta | 5.4.2 | 7.0.0 | openmpi 5.0.8 |
| Wannier90 | 3.1.0 | — | — |
| Yambo | 5.3.0 | 6.2.2 | openmpi 4.1.6 |

📦 **Updated AiiDA stack.** Upgraded to aiida-core v2.8 and Python 3.10.
`aiida-nwchem` bumped to v3.

📦 **Ubuntu 24.04 LTS.** The base OS has been upgraded from Ubuntu 20.04 to 24.04.
Default VM memory has been increased from 1536 MB to 2048 MB.

👌 **Cleaner PATH management.** Code binaries are now symlinked to `~/.local/bin` instead of adding full conda environment `bin/` directories to `PATH`.
This prevents dependency binaries (Python, `pip`, `mpirun`, etc.) from leaking into the user's `PATH`.

---

### Full changelog

#### ✨ New features

- ARM64: add support for Siesta and Wannier90 on `aarch64` ([1e2c276](https://github.com/marvel-nccr/quantum-mobile/commit/1e2c2769291ab862441968f0248da1a90a2721f3))
- ARM64: add architecture-specific support for codes and plugins (NWChem, QE, Yambo) ([cd89e42](https://github.com/marvel-nccr/quantum-mobile/commit/cd89e42201093b75691f88d32bad33fdee4991ed))

#### 👌 Improvements

- Conda: symlink code binaries to `~/.local/bin` instead of adding full env to `PATH` ([c463929](https://github.com/marvel-nccr/quantum-mobile/commit/c463929beabecb28e7bc31255a153dd2864acada))
- Conda: replace `install_pkgs` module with direct mamba calls ([ae8e04c](https://github.com/marvel-nccr/quantum-mobile/commit/ae8e04c468e76453142865e262f815d4e8edec98))
- Package: include architecture in output image filename ([1daf04f](https://github.com/marvel-nccr/quantum-mobile/commit/1daf04f1737538c780de26fa276c890bf41a448d))
- Package: use flexible regex for vdisk detection ([42d818e](https://github.com/marvel-nccr/quantum-mobile/commit/42d818ed9c0add7f8450121217ad243866770782))
- Pseudopotentials: add retry logic for downloads ([d1d21a7](https://github.com/marvel-nccr/quantum-mobile/commit/d1d21a7087c1fddf72abd454d13f58999e6c887b))
- User: explicitly set shell to bash ([46b3441](https://github.com/marvel-nccr/quantum-mobile/commit/46b34415034704c04016e4cb6fa2c30e94ff792b))

#### 🐛 Bug fixes

- AiiDA profile: fix PostgreSQL setup order and ownership ([aba3179](https://github.com/marvel-nccr/quantum-mobile/commit/aba31796c71819171f261133bfd978bdf3734e88))
- Build: use kernel-specific linux-headers instead of generic ([a41a543](https://github.com/marvel-nccr/quantum-mobile/commit/a41a543b1c6f8b9660c67c718a0ffd7203737122))
- Desktop: prevent NetworkManager from breaking network during install ([43fbc47](https://github.com/marvel-nccr/quantum-mobile/commit/43fbc4739bb3b32d7dd66721958c7fb789f5ede0))
- NWChem: fix periodic boundary conditions for H2O example input ([dd49a6e](https://github.com/marvel-nccr/quantum-mobile/commit/dd49a6e9ba4299906e616c9cd335567e3e8ceaa4))
- Package: remove broken NIC2 cleanup task ([dd5a24c](https://github.com/marvel-nccr/quantum-mobile/commit/dd5a24ca49d23673ab03d7a03f85b77da6a8f26c))
- Plotting: fix XCrySDen OpenGL initialisation in VMs (accumulation buffer) ([e6e2d31](https://github.com/marvel-nccr/quantum-mobile/commit/e6e2d319e1b65ef87b1cd9650682e575e6bd1348))
- Pseudopotentials: fix idempotency and status detection ([c2306ba](https://github.com/marvel-nccr/quantum-mobile/commit/c2306ba015e9279f8616d567c0a27f7cb9a5de6f))
- RabbitMQ: set `consumer_timeout` to `undefined` to prevent dropping long-running tasks ([fdec8f1](https://github.com/marvel-nccr/quantum-mobile/commit/fdec8f1c4f787e3dacf320d4e7cfc461d71cfc03))
- System: remove pip upgrade to comply with PEP 668 ([0e0fb4e](https://github.com/marvel-nccr/quantum-mobile/commit/0e0fb4e42d4b9026ecc0f3612cbea9f5de59acf0))

#### ❌ Removals

- Desktop: install JupyterLab shortcut to applications, remove homepage desktop icon ([6c2aec3](https://github.com/marvel-nccr/quantum-mobile/commit/6c2aec38df14c10cc4826fdda70363aac7ae8c37))
- Disabled 3D acceleration (incompatible with vmsvga in VirtualBox 7.2.6) ([8a470ec](https://github.com/marvel-nccr/quantum-mobile/commit/8a470ec7f2184c955d5402cc08bcb2fd620897f5))
- Disabled `aiida-examples` task (gets stuck, needs debugging) ([8a470ec](https://github.com/marvel-nccr/quantum-mobile/commit/8a470ec7f2184c955d5402cc08bcb2fd620897f5))

#### 📦 Dependencies

- VM: base OS upgraded from Ubuntu 20.04 to 24.04 LTS, memory 1536 → 2048 MB ([3e1934a](https://github.com/marvel-nccr/quantum-mobile/commit/3e1934aa7d9fd0da4a4aa36d5403ed8d1800a333))
- Conda: upgrade from deprecated Mambaforge 22.11.1-4 to Miniforge3 25.11.0-1 ([b457fed](https://github.com/marvel-nccr/quantum-mobile/commit/b457fed2bfecae683803e83d8de1de73d696d50e))
- Ansible: update to 13.4 (`ansible-core` 2.20) ([04e2104](https://github.com/marvel-nccr/quantum-mobile/commit/04e2104c1f8e7b619da64c8343553d0f645e439c))
- Roles: `marvel-nccr.ubuntu_desktop` v1.1.0 → v2.0.0, `marvel-nccr.slurm` v2.0.2 → v3.0.0 ([fd03637](https://github.com/marvel-nccr/quantum-mobile/commit/fd03637a55a61b84b84b504d7919b7943e11e0e4))
- Codes: all updated to latest conda-forge versions (see Highlights) ([5874507](https://github.com/marvel-nccr/quantum-mobile/commit/58745073919adfcec6b79c335ba8f9e77b8c6352))
- aiida-nwchem: bump to v3 ([b400e09](https://github.com/marvel-nccr/quantum-mobile/commit/b400e09d4c84af4e433d2087e28acc5b48650b70))

#### 🔄 Refactoring

- Conda: unify AiiDA and code environment installation into a single task file ([b82d17c](https://github.com/marvel-nccr/quantum-mobile/commit/b82d17c7f6e8926f68878d668ff0e3b61d7df9ba))
- Editors: replace `marvel-nccr.editors` role with local tasks ([c4f74ab](https://github.com/marvel-nccr/quantum-mobile/commit/c4f74ab6585120553d9074989c3e12a558bdbc7d))
- User: replace `marvel-nccr.add_user` role with local tasks, remove unused `marvel-nccr.current_user` dependency ([31e628a](https://github.com/marvel-nccr/quantum-mobile/commit/31e628a4c7bf193d0ed4794e47901bb948eedd1f))

#### 🔧 DevOps / CI

- CI: migrate from Vagrant/macOS to Docker/Ubuntu multi-arch (x86_64 + ARM64) ([e6729ba](https://github.com/marvel-nccr/quantum-mobile/commit/e6729ba6a657d4d833a0f27b2791b206693b7769))
- CI: skip RabbitMQ install in Docker (no systemd) ([431afa0](https://github.com/marvel-nccr/quantum-mobile/commit/431afa01d1585e646bbd191e98dfea8c994d819e))
- GitHub Actions: update all actions to latest versions ([6b53857](https://github.com/marvel-nccr/quantum-mobile/commit/6b53857f55f5ebd63558f580fb3653092a2f6f8e))
- pre-commit: migrate to `ansible-lint` for YAML linting (replaces `yamllint`) ([2e3abe2](https://github.com/marvel-nccr/quantum-mobile/commit/2e3abe2506940631c88808a480e0a43c3f813442))
- tox: update to Python 3.13 ([540058b](https://github.com/marvel-nccr/quantum-mobile/commit/540058b6f97cabf504e3766e050d891262499097))
- Vagrant: unify provisioning workflow, separate VM creation from Ansible provisioning ([7290779](https://github.com/marvel-nccr/quantum-mobile/commit/729077907e62798ddd5382f0a374bd893656d1a7))

---

## Quantum Mobile v20.06.1a1

### Improvements

- First official Quantum Mobile release with AiiDA 1.3.0

### Software summary

- OS: Ubuntu 18.04.4 LTS, VirtualBox 6.1.10
- tools: atomistic (xcrysden, jmol, cif2cell, ase, pymatgen, seekpath, spglib, pycifrw), visualization (grace, gnuplot, matplotlib, bokeh, jupyter), simulation environment (slurm, OpenMPI, FFT/BLAS/LAPACK, gcc, gfortran, singularity)
- aiida-core                      1.3.0
  - aiida-bands-inspect             0.4.0
  - aiida-codtools                  2.1.0
  - aiida-cp2k                      1.1.0
  - aiida-ddec                      1.0.0a1
  - aiida-diff                      1.2.0
  - aiida-fleur                     1.1.0
  - aiida-lsmo                      1.0.0b2
  - aiida-optimize                  0.3.1
  - aiida-qeq                       1.0.0a1
  - aiida-quantumespresso           3.0.0
  - aiida-raspa                     1.1.1
  - aiida-siesta                    1.0.1
  - aiida-tbmodels                  0.4.0rc1
  - aiida-tools                     0.3.3
  - aiida-vasp                      0.2.4
  - aiida-wannier90                 2.0.1
  - aiida-wannier90-workflows       1.0.1
  - aiida-yambo                     1.1.1
  - aiida-zeopp                     1.1.1
  - aiidalab                        20.7.0b2
- simulation codes:
  - Quantum Espresso 6.5
  - Yambo     4.5.1
  - fleur     0.30 MaX4
  - siesta    v4.1-rc1
  - cp2k      7.1
  - Wannier90 3.1.0
- pseudopotentials
  - SSSP (PBE) accuracy v1.1
  - SSSP (PBE) precision v1.1
  - SG15 ONCV v1.1

### Build process

- ansible 2.9.10
- Vagrant v2.2.9
  - vbguest v0.24.0
  - bento/ubuntu-18.04 v202005.21.0
- Virtualbox v6.1.10

### Known Issues

BigDFT is not installed, since a fix is outstanding for <https://github.com/marvel-nccr/ansible-role-bigdft/issues/8>.

## Quantum Mobile v20.03.0

### Improvements

- add WannierTools
- add bigdft 1.9.0
- add aiida-bigdft v0.1.0a0

### Build process

- ansible 2.9.5
- Vagrant v2.2.7
  - vbguest v0.23.0
  - bento/ubuntu-18.04 v202002.04.0
- Virtualbox v6.1.4

### Software updates

- yambo 4.5.1
- siesta 4.1-rc1
- cp2k 7.1
- wannier90 3.1
- aiida v1.1.0
  - aiida-yambo 1.0
  - aiidalab v20.2.0b2
  - aiida-wannier90 v2.0.0

## Quantum Mobile v19.12.0

### Improvements

- first Quantum Mobile release with AiiDA 1.0

### Software updates

- Ubuntu 18.04.3 LTS
- aiida-core v1.0.1
  - aiida-cp2k v1.0.0b4
  - aiida-quantumespresso v3.0.0a5
  - aiida-siesta v1.0.0
  - aiida-fleur v1.0.0a0
- aiidalab v19.11.0a2
- yambo 4.4
- QE 6.5 with EPW and Wannier90
- fleur 0.30 MaxR4

## Quantum Mobile v19.09.0

### Improvements

- first official Quantum Mobile release with AiiDA 1.0
- python environment switched from 2.7 to 3.6

### Software updates
- aiida-core v1.0.0b6
  - aiida-quantumespresso v3.0.0a4
- aiidalab v19.08.0a1

## Quantum Mobile v19.07.0

### Improvements
- now installing fixed versions of ansible roles for improved reproducibility
  and tracking of changes between Quantum Mobile releases
- now installing codes system-wide for better reuse in servers 
  - following ansible conventions

### Software updates
- aiidalab v19.05.3

### Build process
- ansible 2.7.10
- Vagrant v2.2.5
  - vbguest v0.19.0
  - bento/ubuntu-18.04 v201906.18.0
- Virtualbox v6.0.10

## Quantum Mobile v19.03.0

### Improvements

- add link to FAQ on desktop
- switch from torque to slurm scheduler

### Software updates

- Ubuntu 18.04 LTS
- Quantum Espresso v6.3
- cp2k v6.1
- yambo v4.3.2
- fleur 0.27 MaXR3
- siesta v4.0.2
- aiida-core v0.12.3
- aiidalab v19.03.0

### Build process

- ansible 2.7.5
- Vagrant v2.2.4
  - vbguest v0.17.1
  - bento/ubuntu-18.04 v201812.27.0
- Virtualbox v6.0.4


## Quantum Mobile v18.06.0

### Software updates

- aiida-core v0.12.0
- aiida-quantumespresso v2.0.1

### Improvements

- Add /scratch directory
- Using shared folders no longer requires sudo

### Build process

- Separate roles into independent repositories
- Roles are installed via ansible-galaxy
- Continuous integration tests for individual roles 

## Quantum Mobile v18.04.0

### Software updates

- aiida-core v0.11.4
- aiida-quantumespresso v2.0.0
- aiida-cp2k v0.9.0
- aiida-yambo v0.2.5

### Improvements

- Switch to Chromium browser as Firefox struggles with WebGL
- Add cp2k data directory
- AiiDA Daemon is now a system service - no need to start it or shut it down
- Import SSSP from AiiDA export files hosted on the Materials Cloud Archive

### Build process

- Add variables that can be used to turn on/off features for
  increased flexibility (e.g. to install Quantum Mobile as a
  server):
  - 'headless': if true, avoids GUI-related setup
  - 'release_notes': if false, does not add release notes
- Running the ansible roles on a different host is now as easy as
  `ansible-playbook playbook-build.yml -i inventory_file`
- Adjustments for ansible 2.5

## Quantum Mobile v18.03.0

### Improvements

- Add Wannier90 v2.1 + aiida-wannier90 v1.0.0

### Build process

- VM image built using Virtualbox 5.2.8

## Quantum Mobile v18.02.2

### Software updates

- aiida-core v0.11.0
- aiida-siesta v0.11.5

## Quantum Mobile v18.02.0

### Improvements

- Add jupyter apps (just like on [aiidalab.materialslcoud.org](aiidalab.materialscloud.org))

### Software updates

- aiida-yambo v0.2.4
- aiida-siesta v0.9.8
- QE 6.2.1
- SSSP (PBE) accuracy 1.0
- SSSP (PBE) efficiency 1.0

## Build process

- VM image built using Virtualbox 5.2.6 + Guest Additions 5.2.7

## Quantum Mobile v17.12.0

### Improvements

- Add Quantum Mobile Logo
- Add AiiDA Demos

### Software updates

- yambo 4.2.1
- fleur 0.27 MaXR2.1
- aiida 0.10.1
- aiida-cp2k 0.7

### Build process

- VM image built using Virtualbox 5.2.4
- Size of VM image and virtual disk added to install instructions

## Quantum Mobile v17.11.0

### Initial release

- Operating System: Ubuntu 16.04.3 LTS
- Tools:
  - torque server
  - openmpi libraries
  - xmgrace, gnuplot, xcrysden, jmol
- Quantum Espresso v6.2
- Yambo v4.2.0
- fleur v0.27 MaXR2
- siesta v4.0.1
- cp2k v5.1
- aiida v0.10.0
  - aiida-fleur v0.6.0
  - aiida-quantumespresso v1.0.1
  - aiida-siesta v0.9.7.1
  - aiida-cp2k v0.2.2
- pseudopotentials:
  - sssp-pbe-accuracy v0.7
  - sg15-oncv-1.1
