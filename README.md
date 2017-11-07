# Quantum Mobile Virtual Machine

*Quantum Mobile* is a Virtual Machine for computational materials science.

This repository contains the vagrant and ansible scripts to set up the VM.

## Prerequisites

- [vagrant](https://www.vagrantup.com/downloads.html)
- [virtualbox](https://www.virtualbox.org/wiki/Downloads)
- `pip install -r requirements.txt`

## Create Virtual Machine

```
vagrant plugin install vagrant-vbguest  # optional, improves interface
vagrant up  # build vm from scratch (takes some tens of minutes)
```

Note: So far tested only on Unix, but should work on Windows as well.

## Create image
```
bash create_image.sh
```

## Upload image
```
openstack object create marvel-vms marvel_vm_<version>.ova
openstack object create marvel-vms INSTALL_<version>.txt
```


## Useful commands

 * `vagrant provision --provision-with ansible`: re-run ansible scripts
 * `vagrant reload`: restart machine
 * `vagrant halt`: stop machine
 * ```
   ./setup-ansible.sh             # inform ansible about ssh config
   ansible-playbook playbook.yml  # run ansible directly, add tags, ...
   ```
 * ```scp -F vagrant-ssh default:/path/on/vm  my/path```

# Acknowledgements

This work is supported by the ["MARVEL National Centre for Competency in
Research](http://nccr-marvel.ch) and the [MaX European centre of
excellence](http://www.max-centre.eu/)


