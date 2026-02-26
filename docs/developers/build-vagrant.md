# Build a Desktop VM

In the following, we explain how to build your own custom Quantum Mobile VirtualBox image from scratch.

Note that building the full VM can take around 15 minutes.


## Prerequisites & Installation

Building Quantum Mobile requires and has been tested on:

- Operating system: MacOS Sequoia 15.5 and Ubuntu 24.04.
- [Vagrant](https://www.vagrantup.com/downloads.html) 2.4.9
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) 7.2.6
- [Python](https://www.python.org/) 3.13

But may also work for more recent versions.

````{dropdown} Building on Windows

:::{warning}
This has not been tested in some time, here be dragons. 🐉
:::

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

Install [tox](https://tox.readthedocs.io/):

```bash
pip install tox
```

## Create the Virtual Machine

We use [tox](https://tox.readthedocs.io/) to set up the Python environment and run the build steps.

```bash
tox -e vagrant      # create and start the VM
tox -e ansible      # provision the VM with Ansible
```

This will:
1. `tox -e vagrant`: Call `vagrant up` to create and start the VM
2. `tox -e ansible`: Generate the SSH configuration file (`vagrant-ssh`) and call `ansible-playbook playbook-build.yml` to provision the VM and build the required software on it

You can see all available `tox` environments with:

```bash
tox -a -v           # shows available automations
```

### Continuing a failed build

If the build fails or is interrupted at any step (for example a failed download, due to a bad connection),
you can continue the build with:

```bash
tox -e ansible
```

The ansible automation steps are generally idempotent, meaning that if they have been previously run successfully, then they will be skipped in any subsequent runs.

:::{note}
You don't need to manually run `vagrant ssh-config > vagrant-ssh` - `tox -e ansible` does this automatically.
:::

### Running only selected steps

All steps of the ansible build process are "tagged", which allows you to select to run only certain steps, or skip others.

To list all the tags:

```bash
tox -e ansible -- --list-tags
```

or look at `playbook-build.yml`.

To run only certain tags, use:

```bash
tox -e ansible -- --tags tag1,tag2 --skip-tags tag3
```

### Creating the image

First, clean unnecessary build files:

```bash
tox -e ansible -- --tags cleanup
```

Then run `playbook-package.yml` *via*:

```bash
tox -e package -- --skip-tags validate
```

This will compact the hard disk of the virtual machine and export the image and release notes to the `dist/` folder.

:::{note}
The `validate` tag checks that the repositories git tag is the same as the `vm_version` specified in `inventory.yml`, and is only needed for new releases by Quantum Mobile maintainers.
:::

### Other Useful commands

- `vagrant reload`: restart machine
- `vagrant halt`: stop machine

Vagrant keeps information on how to connect in a folder called `.vagrant`.
If you would like to create a new machine, `vagrant destroy` will remove the `.vagrant` folder and allow you to create a new VM (note: you may want to keep a copy in case you want to reconnect later).

## Troubleshooting

### VirtualBox Guest Additions Issues

If you experience issues with shared folders, clipboard sharing, or graphics performance, you may need to manage VirtualBox Guest Additions manually.
Install the `vagrant-vbguest` plugin:

```bash
vagrant plugin install vagrant-vbguest
```

Then you can:

```bash
# Check Guest Additions status
vagrant vbguest --status

# Manually install/update Guest Additions
vagrant vbguest --do install

# Rebuild Guest Additions
vagrant vbguest --do rebuild
```

:::{note}
VirtualBox Guest Additions are tools that run inside the VM to provide features like shared folders, seamless mouse integration, and better graphics. The base Ubuntu box comes with Guest Additions pre-installed, but version mismatches can occur when you upgrade VirtualBox, potentially causing shared folder or clipboard issues. This plugin helps resolve such mismatches.
:::
