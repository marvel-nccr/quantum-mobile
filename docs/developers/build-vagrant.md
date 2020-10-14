# Build a desktop VM

In the following, we explain how to build your own custom Quantum Mobile image, allowing you to remove components you don't need and add new ones.

The [quantum mobile repository](https://github.com/marvel-nccr/quantum-mobile) contains the Vagrant and [Ansible playbooks]([ansible playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)) required to set up the virtual machine from scratch.

Calculate at least one hour for building the VM:

````{dropdown} Approximate Timings
```
marvel-nccr.quantum_espresso : Make QE executables ---------------------------------------------------------- 2085.47s
marvel-nccr.fleur : run fleur tests ------------------------------------------------------------------------- 1454.29s
marvel-nccr.yambo : Make Yambo executables ------------------------------------------------------------------ 1167.91s
marvel-nccr.fleur : Make fleur executables ------------------------------------------------------------------ 1002.09s
marvel-nccr.ubuntu_desktop : Install ubuntu-desktop (apt) ---------------------------------------------------- 978.57s
marvel-nccr.wannier90 : run Wannier90 default tests ---------------------------------------------------------- 972.97s
marvel-nccr.aiidalab : Install aiidalab ---------------------------------------------------------------------- 749.07s
marvel-nccr.siesta : Make siesta executables ----------------------------------------------------------------- 422.45s
marvel-nccr.cp2k : download cp2k binary ---------------------------------------------------------------------- 349.02s
marvel-nccr.slurm : Install apt packages --------------------------------------------------------------------- 246.30s
marvel-nccr.simulationbase : Install plotting tools, etc. ---------------------------------------------------- 227.87s
marvel-nccr.wannier90 : Get Wannier90 source ----------------------------------------------------------------- 203.48s
marvel-nccr.simulationbase : Install packages for build environment (apt) ------------------------------------ 187.30s
marvel-nccr.wannier90 : Make Wannier90 executables ----------------------------------------------------------- 179.31s
marvel-nccr.siesta : Compile "tbtrans" ----------------------------------------------------------------------- 173.52s
marvel-nccr.simulationbase : Install apt, pip3 --------------------------------------------------------------- 151.31s
marvel-nccr.aiida : Install DB & more ------------------------------------------------------------------------ 146.25s
marvel-nccr.wannier_tools : Get wannier_tools source --------------------------------------------------------- 131.27s
marvel-nccr.ubuntu_desktop : install chromium-browser -------------------------------------------------------- 129.00s
marvel-nccr.editors : Install some common editors ------------------------------------------------------------ 126.35s
```
````

:::{seealso}
See the continuous deployment (CD) workflow, for up-to-date timings <https://github.com/marvel-nccr/quantum-mobile/actions?query=workflow%3ACD>
:::

## Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads.html) >= 2.0.1
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) >= 6.1.6
- [Python](https://www.python.org/) >= 3.6
- Host OS: Building Quantum Mobile has been tested on MacOS, Ubuntu and Windows.

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

## Create the Virtual Machine

:::{tip}
Building the Desktop Edition is tested on GitHub Actions on every commit to the repository.
For the tested steps see the `.github/workflows/build.yml` file.
:::

First clone the repository:

```bash
git clone https://github.com/marvel-nccr/quantum-mobile.git
cd quantum-mobile
```

Then use [tox](https://tox.readthedocs.io/) to set up the Python environment and run the build steps.

```bash
pip install tox
# to show all available automations
tox -a -v        # shows available automations
# improves interface
vagrant plugin install vagrant-vbguest
```

:::{tip}
If you get an error during the installation of the VirtualBox Guest Additions, you may need to perform additional steps (see [issue #60](https://github.com/marvel-nccr/quantum-mobile/issues/60)).
:::

To build and provision the machine, you can then run:

```bash
tox -e py37-vagrant
```

This will call `vagrant up`, to initialise the VM, which then calls `ansible-playbook playbook-build.yml`, to configure the VM and build the required software on it.

## Continuing a failed build

If the build fails or is interrupted at any step (for example a failed download, due to a bad connection),
you can continue the build with:

```bash
# output the vagrant box connection details
vagrant ssh-config > vagrant-ssh
tox -e py38-ansible
```

The ansible automation steps are generally idempotent, meaning that if they have been previously run successfully, then they will be skipped in any subsequent runs.

## Customising the build

The `inventory.yml` file contains all the variables used during the VM build.
You can modify this to control aspects of the build, such as the default #CPUs and what web-browser to install.

:::{seealso}
The [ansible inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) and [playbook variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) documentation.
:::

## Running only selected steps

All steps of the ansible build process are "tagged", meaning you can select to run only certain steps, or skip others.

To list all the tags:

```bash
tox -e py38-ansible -- --list-tags
```

or look at `playbook-build.yml`.

To run run only certain tags, use either:

```bash
ANSIBLE_ARGS="--tags tag1,tag2 --skip-tags tag3" tox -e py38-vagrant
```

or

```bash
tox -e py38-ansible -- --tags tag1,tag2 --skip-tags tag3
```

## Creating the image

First, clean unnecessary build files:

```bash
tox -e py38-ansible -- --tags quantum_espresso,qm_customizations,simulationbase,ubuntu_desktop --extra-vars "clean=true"
```

Then run `playbook-package.yml` *via*:

```bash
tox -e py38-package -- --skip-tags validate
```

This will compact the hard disk of the virtual machine and export the image and release notes to the `dist/` folder.

:::{note}
The `validate` tag checks that the repositories git tag is the same as the `vm_version` specified in `inventory.yml`, and is only needed for strict releases.
:::

## Other Useful commands

- `vagrant reload`: restart machine
- `vagrant halt`: stop machine

Vagrant keeps information on how to connect in a folder called `.vagrant`.
If you would like to create a new machine, `vagrant destroy` will remove the `.vagrant` folder and allow you to create a new VM (note: you may want to keep a copy in case you want to reconnect later).
