# Build a VM from scratch

> You would like to add/remove some components of Quantum Mobile and produce your own customised image?

This quantum mobile repository contains the Vagrant and Ansible scripts required to
set up the virtual machine from scratch.

Allow at least one hour:

````{dropdown} Approximate Timings
```
marvel-nccr.quantum_espresso : Make QE executables -------------------------------------------------------------------- 2085.47s
marvel-nccr.fleur : run fleur tests ----------------------------------------------------------------------------------- 1454.29s
marvel-nccr.yambo : Make Yambo executables ---------------------------------------------------------------------------- 1167.91s
marvel-nccr.fleur : Make fleur executables ---------------------------------------------------------------------------- 1002.09s
marvel-nccr.ubuntu_desktop : Install ubuntu-desktop (apt) -------------------------------------------------------------- 978.57s
marvel-nccr.wannier90 : run Wannier90 default tests -------------------------------------------------------------------- 972.97s
marvel-nccr.aiidalab : Install aiidalab -------------------------------------------------------------------------------- 749.07s
marvel-nccr.siesta : Make siesta executables --------------------------------------------------------------------------- 422.45s
marvel-nccr.cp2k : download cp2k binary -------------------------------------------------------------------------------- 349.02s
marvel-nccr.slurm : Install apt packages ------------------------------------------------------------------------------- 246.30s
marvel-nccr.simulationbase : Install plotting tools, etc. -------------------------------------------------------------- 227.87s
marvel-nccr.wannier90 : Get Wannier90 source --------------------------------------------------------------------------- 203.48s
marvel-nccr.simulationbase : Install packages for build environment (apt) ---------------------------------------------- 187.30s
marvel-nccr.wannier90 : Make Wannier90 executables --------------------------------------------------------------------- 179.31s
marvel-nccr.siesta : Compile "tbtrans" --------------------------------------------------------------------------------- 173.52s
marvel-nccr.simulationbase : Install apt, pip3 ------------------------------------------------------------------------- 151.31s
marvel-nccr.aiida : Install DB & more ---------------------------------------------------------------------------------- 146.25s
marvel-nccr.wannier_tools : Get wannier_tools source ------------------------------------------------------------------- 131.27s
marvel-nccr.ubuntu_desktop : install chromium-browser ------------------------------------------------------------------ 129.00s
marvel-nccr.editors : Install some common editors ---------------------------------------------------------------------- 126.35s
```
````

:::{seealso}
See the continuous deployment (CD) workflow, for up-to-date timings <https://github.com/marvel-nccr/quantum-mobile/actions?query=workflow%3ACD>
:::

## Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads.html) >= 2.0.1
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Python](https://www.python.org/) >= 3.6
- Host OS: Building Quantum Mobile has been tested on MacOS, Ubuntu
  and Windows (see [instructions](https://github.com/marvel-nccr/quantum-mobile/wiki/Instructions-for-building-Quantum-Mobile)).

## Create Virtual Machine

```bash
git clone https://github.com/marvel-nccr/quantum-mobile.git
cd quantum-mobile
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
vagrant plugin install vagrant-vbguest  # optional, improves interface
vagrant up  # build vm from scratch (takes some tens of minutes)
```

:::{note}
If you get an error during the installation of the VirtualBox Guest Additions, you may need to perform additional
steps (see [issue #60](https://github.com/marvel-nccr/quantum-mobile/issues/60)).
:::

## Create image


```bash
# optional: reduce size of VM
ansible-playbook playbook-build.yml --extra-vars "clean=true"
./compact_hd.sh

./create_image.sh
```

## Useful commands

- `vagrant provision --provision-with ansible`: re-run ansible scripts
- `vagrant reload`: restart machine
- `vagrant halt`: stop machine
- `ANSIBLE_ARGS="-twannier90" vagrant provision --provision-with=ansible`: run ansible scripts for the `wannier90` tag

- ```bash
   ./setup-ansible.sh             # inform ansible about ssh config
   ansible-playbook playbook-build.yml  # run ansible directly, add tags, ...
   ansible-playbook playbook-build.yml  --tags wannier90
   ```

- `ssh -F vagrant-ssh default`
- `scp -F vagrant-ssh default:/path/on/vm  my/path`
- ```./reconnect_vagrant.sh  # reconnect vagrant to an old VM```
- `ansible-galaxy install -r requirements.yml --ignore-errors`

## Tips

When modifying properties of the virtual machine, such as the #CPUs or the
amount of RAM, please note that you may need to update this information
in part of the installed software as well:

 * scheduler: The number of processors for the torque queue is pre-configured.
   <add instructions on how to change this>.
   See also `roles/scheduler/tasks/main.yml <https://github.com/marvel-nccr/marvel-virtualmachine/blob/master/roles/scheduler/tasks/main.yml>`_
 * aiida: The number of cores of the `localhost` computer are pre-configured.
   Just delete the computer and re-configure it again.
   See also `roles/aiida/templates/localhost.computer <https://github.com/marvel-nccr/marvel-virtualmachine/blob/master/roles/aiida/templates/localhost.computer>`_

## Windows

 * Install [Windows Subsystem for Linux](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux)
 * Install VirtualBox under *Windows*
 * Add the following lines to your `.bashrc` in WSL:
   ```bash
   # Enable WSL feature in vagrant
   export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"  
   # Add virtualbox under Windows to $PATH
   export PATH="${PATH}:/mnt/c/Program Files/Oracle/VirtualBox"
   ```
 * Then, follow the usual instructions from the [README](https://github.com/marvel-nccr/quantum-mobile/blob/master/README.md#build-it-from-scratch)

## Miscellaneous

Vagrant keeps information on how to connect in a folder called `.vagrant`.
If you would like to create a new machine, `vagrant destroy` will remove the `.vagrant` folder and allow you to create a new VM (note: you may want to keep a copy in case you want to reconnect later).