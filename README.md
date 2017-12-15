# Quantum Mobile

*Quantum Mobile* is a Virtual Machine for computational materials science.

It comes with a collection of software packages for quantum
mechanical calculations, including

 * [Quantum ESPRESSO](http://www.quantum-espresso.org/)
 * [Yambo](http://www.yambo-code.org/)
 * [fleur](http://www.flapw.de/)
 * [Siesta](https://launchpad.net/siesta)
 * [CP2K](https://www.cp2k.org)

all of which are set up and ready to be used through the
[AiiDA](http://www.aiida.net) python framework for automated workflows and
provenance tracking.

Please see [releases](https://github.com/marvel-nccr/quantum-mobile/releases) for the latest VM image and installation instructions.

This repository contains the vagrant and ansible scripts to set up the VM.

## Prerequisites

- [vagrant](https://www.vagrantup.com/downloads.html) >= 2.0
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
# optional: reduce size of VM
#ansible-playbook playbook.yml --extra-vars "clean=true"
bash create_image.sh
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

This work is supported by the [MARVEL National Centre for Competency in
Research](http://nccr-marvel.ch) and the [MaX European centre of
excellence](http://www.max-centre.eu/)
