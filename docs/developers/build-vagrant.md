# Build a Desktop VM

In the following, we explain how to build your own custom Quantum Mobile VirtualBox image from scratch.

Calculate at around two hours for building the full VM:

````{dropdown} Approximate Timings
```
marvel-nccr.bigdft : Compile bigdft executables ----------------------- 906.73s
marvel-nccr.quantum_espresso : Make QE executables -------------------- 867.71s
marvel-nccr.abinit : Make abinit executable (2 cpu) ------------------- 807.30s
marvel-nccr.wannier90 : run Wannier90 default tests ------------------- 720.07s
marvel-nccr.libxc : Compile libxc executable (2 cpu) ------------------ 678.97s
marvel-nccr.ubuntu_desktop : Install ubuntu-desktop (apt) ------------- 532.78s
marvel-nccr.yambo : Make Yambo executables ---------------------------- 406.67s
marvel-nccr.fleur : run fleur tests ----------------------------------- 395.95s
marvel-nccr.fleur : Make fleur executables ---------------------------- 345.77s
marvel-nccr.abinit : run the tests (2 cpu) ---------------------------- 315.32s
marvel-nccr.libxc : Run make check for libxc -------------------------- 313.18s
marvel-nccr.siesta : Make siesta executable --------------------------- 308.16s
marvel-nccr.aiida : Install aiida-core + plugins into venv ------------ 262.80s
marvel-nccr.slurm : Install apt packages ------------------------------ 211.29s
marvel-nccr.simulationbase : Install plotting tools, etc. ------------- 187.73s
marvel-nccr.siesta : Make xmlf90 -------------------------------------- 179.07s
marvel-nccr.bigdft : run test suite ----------------------------------- 143.86s
marvel-nccr.aiidalab : install server-side (aiida) dependencies ------- 120.63s
marvel-nccr.cp2k : download cp2k binary ------------------------------- 108.26s
marvel-nccr.ansible_prerequisites : Install aptitude ------------------ 104.13s
```
:::{seealso}
See the [continuous deployment (CD) workflow](https://github.com/marvel-nccr/quantum-mobile/actions?query=workflow%3ACD) for up-to-date timings
:::
````

## Prerequisites & Installation

- Operating system: Building Quantum Mobile has been tested on MacOS, Ubuntu and Windows.
- [Vagrant](https://www.vagrantup.com/downloads.html) >= 2.0.1
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) >= 6.1.6
- [Python](https://www.python.org/) >= 3.6

````{dropdown} Building on Windows
- Install [Windows Subsystem for Linux](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux)
- Install VirtualBox under *Windows*
- Add the following lines to your `.bashrc` in WSL:

  ```bash
  # Enable WSL feature in vagrant
  export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"  
  # Add virtualbox under Windows to $PATH
  export PATH="${PATH}:/mnt/c/Program Files/Oracle/VirtualBox"
  ```
````

Clone the repository:

```bash
git clone https://github.com/marvel-nccr/quantum-mobile.git
cd quantum-mobile
```

Install [tox](https://tox.readthedocs.io/) and the `vagrant-vbguest` plugin:

```bash
pip install tox
# improves interface
vagrant plugin install vagrant-vbguest
```
:::{tip}
For those using [Conda](https://docs.conda.io/), it is recommended to also install [tox-conda](https://github.com/tox-dev/tox-conda):

```bash
pip install tox-conda
```

:::

## Create the Virtual Machine

:::{seealso}
If you would like to [customise](customize.md) any aspects of the VM, now would be a good time to do so.
:::


Use [tox](https://tox.readthedocs.io/) to set up the Python environment and run the build steps.

```bash
tox -a -v        # shows available automations
tox -e vagrant
```
This will call `vagrant up`, to initialise the VM, which then calls `ansible-playbook playbook-build.yml`, to configure the VM and build the required software on it.

:::{tip}
If you get an error during the installation of the VirtualBox Guest Additions, you may need to perform additional steps (see [issue #60](https://github.com/marvel-nccr/quantum-mobile/issues/60)).
:::
:::{tip}
Building the Desktop Edition is tested on GitHub Actions on every commit to the repository.
For the tested steps see the `.github/workflows/build.yml` file.
:::


### Continuing a failed build

If the build fails or is interrupted at any step (for example a failed download, due to a bad connection),
you can continue the build with:

```bash
# output the vagrant box connection details
vagrant ssh-config > vagrant-ssh
tox -e ansible
```

The ansible automation steps are generally idempotent, meaning that if they have been previously run successfully, then they will be skipped in any subsequent runs.

### Running only selected steps

All steps of the ansible build process are "tagged", which allows you to select to run only certain steps, or skip others.

To list all the tags:

```bash
tox -e ansible -- --list-tags
```

or look at `playbook-build.yml`.

To run only certain tags, use either:

```bash
ANSIBLE_ARGS="--tags tag1,tag2 --skip-tags tag3" tox -e vagrant
```

or

```bash
tox -e ansible -- --tags tag1,tag2 --skip-tags tag3
```

## Creating the image

First, clean unnecessary build files:

```bash
tox -e ansible -- --tags qm_customizations,simulationbase,ubuntu_desktop --extra-vars "clean=true"
```

Then run `playbook-package.yml` *via*:

```bash
tox -e package -- --skip-tags validate
```

This will compact the hard disk of the virtual machine and export the image and release notes to the `dist/` folder.

:::{note}
The `validate` tag checks that the repositories git tag is the same as the `vm_version` specified in `inventory.yml`, and is only needed for new releases by Quantum Mobile maintainers.
:::

## Other Useful commands

- `vagrant reload`: restart machine
- `vagrant halt`: stop machine

Vagrant keeps information on how to connect in a folder called `.vagrant`.
If you would like to create a new machine, `vagrant destroy` will remove the `.vagrant` folder and allow you to create a new VM (note: you may want to keep a copy in case you want to reconnect later).
