# MARVEL Virtual Machine

This repository contains the vagrant and ansible scripts to set up the "standard" MARVEL virtual machine.

## Prerequisites

- [vagrant](https://www.vagrantup.com/downloads.html)
- [virtualbox](https://www.virtualbox.org/wiki/Downloads)
- ansible >= 2.4 (`pip install ansible`)

Note: So far tested only on Unix, but should work on Windows as well.

## Create Virtual Machine

```
vagrant plugin install vagrant-vbguest  # optional, improves interface
vagrant up  # build vm from scratch (takes some tens of minutes)
```

# Create image
```
bash create_image.sh
```

## Useful commands

 * `vagrant provision --provision-with ansible`: re-run ansible scripts
 * `vagrant reload`: restart machine
 * `vagrant halt`: stop machine

## Virtualbox optimisations

 * Make mouse/typing more responsive: 
   * Shut down machine
   * Machine => Settings => Display => 'Enable 3D acceleration' 
   * Start machine
 * Enable clipboard sharing
   * Devices => Shared clipboard => bidirectional

