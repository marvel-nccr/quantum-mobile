# Changelog

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
  `ansible-playbook playbook.yml -i inventory_file`
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
