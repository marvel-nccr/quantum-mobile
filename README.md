[![Build Status](https://travis-ci.org/marvel-nccr/quantum-mobile.svg?branch=master)](https://travis-ci.org/marvel-nccr/quantum-mobile)

# Quantum Mobile Desktop Edition

## What is Quantum Mobile

*Quantum Mobile* is a Virtual Machine for computational materials science.

It comes with a collection of software packages for quantum
mechanical calculations, including

 * [Quantum ESPRESSO](http://www.quantum-espresso.org/)
 * [Yambo](http://www.yambo-code.org/)
 * [fleur](http://www.flapw.de/)
 * [Siesta](https://gitlab.com/siesta-project/siesta)
 * [CP2K](https://www.cp2k.org)
 * [Wannier90](http://www.wannier.org)
 * [BigDFT](http://www.bigdft.org)

all of which are set up and ready to be used on their own or through the
[AiiDA](http://www.aiida.net) python framework for automated workflows and
provenance tracking.

Quantum Mobile is available in two editions:

  * *Quantum Mobile Desktop Edition* [**(download)**](https://github.com/marvel-nccr/quantum-mobile/releases) comes with the familiar Ubuntu Desktop and runs on your Windows, MacOS or Linux computer using the [VirtualBox](http://virtualbox.org/) software.
    The Desktop Edition is tailored to provide students with a familiar working environment.

  * *Quantum Mobile Cloud Edition* [**(download)**](https://github.com/marvel-nccr/quantum-mobile-cloud-edition/releases) is intended for use on servers using cloud services like Amazon Web Services. Google Cloud, or OpenStack.
    The Cloud Edition targets advanced users who are familiar with the command line & SSH and prefer to run calculations on a remote server.

![Demo](https://image.ibb.co/n50SdT/quantum_mobile.gif "A brief impression of the Quantum Mobile interface.")


## Build it from scratch

You would like to add/remove some components of Quantum Mobile and produce your own customised image?

This git repository contains the vagrant and ansible scripts required to
set up the virtual machine from scratch (note: [plan >1h](other_stuff/timings.txt) for
this).

### Prerequisites

- [vagrant](https://www.vagrantup.com/downloads.html) >= 2.0.1
- [virtualbox](https://www.virtualbox.org/wiki/Downloads)
- [python](https://www.python.org/)
- Host OS: Building Quantum Mobile has been tested on MacOS, Ubuntu
  and Windows (see [instructions](https://github.com/marvel-nccr/quantum-mobile/wiki/Instructions-for-building-Quantum-Mobile)).

### Create Virtual Machine

```
git clone https://github.com/marvel-nccr/quantum-mobile.git
cd quantum-mobile
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
vagrant plugin install vagrant-vbguest  # optional, improves interface
vagrant up  # build vm from scratch (takes some tens of minutes)
```

Note: If you get an error during the installation of the VirtualBox Guest Additions, you may need to perform additional
steps (see [issue #60](https://github.com/marvel-nccr/quantum-mobile/issues/60)).

### Create image
```
# optional: reduce size of VM
ansible-playbook playbook.yml --extra-vars "clean=true"
./compact_hd.sh

./create_image.sh
```

### Useful commands

 * `vagrant provision --provision-with ansible`: re-run ansible scripts
 * `vagrant reload`: restart machine
 * `vagrant halt`: stop machine
 * `ANSIBLE_ARGS="-twannier90" vagrant provision --provision-with=ansible`: run ansible scripts for the `wannier90` tag
 * ```
   ./setup-ansible.sh             # inform ansible about ssh config
   ansible-playbook playbook.yml  # run ansible directly, add tags, ...
   ansible-playbook playbook.yml  --tags wannier90
   ```
 * `ssh -F vagrant-ssh default`
 * `scp -F vagrant-ssh default:/path/on/vm  my/path`
 * ```./reconnect_vagrant.sh  # reconnect vagrant to an old VM```
 * `ansible-galaxy install -r requirements.yml --ignore-errors`

## Customizing Quantum Mobile

Please see the [Quantum Mobile Wiki](https://github.com/marvel-nccr/quantum-mobile/wiki) on how to adapt Quantum Mobile for your course / tutorial / ....

## Contact

Please direct inquiries regarding Quantum Mobile to the [AiiDA mailinglist](http://www.aiida.net/mailing-list/)

For issues encountered during installation of the VM, see the [FAQ](https://github.com/marvel-nccr/quantum-mobile/wiki/Frequently-Asked-Questions).

## Acknowledgements

This work is supported by the [MARVEL National Centre for Competency in Research](http://nccr-marvel.ch)
funded by the [Swiss National Science Foundation](http://www.snf.ch/en),
as well as by the [MaX European Centre of Excellence](http://www.max-centre.eu/) funded by
the Horizon 2020 EINFRA-5 program, Grant No. 676598.

![MARVEL](other_stuff/logos/MARVEL.png)
![MaX](other_stuff/logos/MaX.png)
