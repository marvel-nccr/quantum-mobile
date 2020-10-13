# Developing Quantum Mobile

## Preparing a release

### Versions to check/update

* [Vagrant](https://www.vagrantup.com/downloads.html)
* Vagrant [vbguest plugin](https://github.com/dotless-de/vagrant-vbguest) (`vagrant plugin update`)
* [bento/ubuntu-18.04](https://app.vagrantup.com/bento/boxes/ubuntu-18.04) Vagrant image (`vagrant box update`)
* [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* QM codes
  * [Quantum Espresso](https://gitlab.com/QEF/q-e/tags)
  * [cp2k](https://github.com/cp2k/cp2k/releases)
  * [siesta](https://gitlab.com/siesta-project/siesta/-/releases)
  * [yambo](https://github.com/yambo-code/yambo/wiki/Releases-(tar.gz-format))
  * [fleur](https://www.flapw.de/master/downloads/)
  * [wannier90](https://github.com/wannier-developers/wannier90/releases)
  * [bigdft](https://gitlab.com/l_sim/bigdft-suite/-/releases)
* [AiiDA packages on PyPI](https://pypi.org/search/?q=aiida&o=-created)
* Quantum Mobile itself

### Building the VM

```bash
vagrant up
```

In case the build is interrupted at some point, continue with

```bash
./setup_ansible.sh
ansible-playbook playbook.yml --tags cp2k,siesta,...
```

### After building the VM

All items listed here are candidates for automation.

* Possibly restart the VM if you are not logged in (on still cannot log in once logged out ...)
* Doubleclick on the Desktop symbols to show the icons
* clear bash history: `cat /dev/null > ~/.bash_history && history -c && exit`
* restart VM to clear content of `/tmp`
* run `ansible-playbook playbook.yml --tags ubuntu_desktop,qm_customizations,simulationbase --extra-vars "clean=true"`
* `./compact_hd.sh`
* `./create_image.sh`
* upload to object store
  * `openstack object create marvel-vms INSTALL_<version>.txt`
  * `openstack object create marvel-vms quantum_mobile_<version>.ova`
* Prepare release:
  * update `CHANGELOG.md`
  * Commit changes of quantum-mobile repository to `develop` branch
  * merge into `master`
  * `git tag 19.12.0RC1 && git push --tags`
  * [draft new release](https://github.com/marvel-nccr/quantum-mobile/releases/new), copying content of `INSTALL_...` file and `CHANGELOG.md`
  * replace URL to object store by [bit.ly](https://bitly.com/) shortlink

Extra modifications for QM 20.03.1:
 * delete examples/ icon on desktop
 * fix issue with clipboard not working (#112)
 * fix issue with rabbitmq not shutting down (#111)

## Preparing a cloud image

### General guidelines

 * For the server to build the VM, choose e.g. 2 CPUs with 4GB of RAM
   * Your configuration may also be the standard configuration shown to users creating a VM using your image (to figure out?)
   * You won't need it for long, so price for CPU/RAM is of no concern
 * Exemplary metadata:
   * name: `quantum-mobile-20-05-0`  (GCP only allows alphanumeric characters + dashes)
   * family: `quantum-mobile`
   * description: 

          Quantum Mobile Cloud Edition Server v20.05.0
          See https://github.com/marvel-nccr/quantum-mobile-cloud-edition

### AWS peculiarities

 * Create new keypair from the GUI - note: will always be added to `ubuntu` user
 * If you intend to publish the image, follow AWS instructions to remove system SSH keys:  
   `sudo shred -u /etc/ssh/*_key /etc/ssh/*_key.pub`
 * List image publicly: After creation, edit the properties and select "public"


### GCP peculiarities

 * GCP lets you create the SSH keypair by yourself:
   * Create new SSH keypair on your machine. 
   * Edit the `user@server` bit at the end of the public key to user "ubuntu" (GCP detects this user and adds the SSH public key for this user in the VM)
   * add public key to VM
 * VM IP seems to be stable even between stop/start of VM
 * Creating the image
   * GCP distinguishes between "Machine images" (private) and "Images" (can be public). You want the second option.
 * List image publicly: (not sure whether there is a way to do this via the GUI)
   * Click on "cloud shell" logo on the top right
   * Paste command

          gcloud compute images add-iam-policy-binding quantum-mobile-20-05-0 \
              --member='allAuthenticatedUsers' \
              --role='roles/compute.imageUser'

### Pricing

   * Image pricing (for us to host it):
     * magnetic: 8.5c/GB/month (GCP)
   * Disk pricing (for users): 
     * magnetic: 4c/GB/month (GCP), 2.5c/GB/month (AWS)
     * SSD: 10c/GB/month (AWS)