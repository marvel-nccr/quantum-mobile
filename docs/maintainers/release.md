# Preparing releases

## Versions to check/update

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

## Provisioning the VM

### Desktop Edition

Follow the [desktop build instructions](../developers/build-vagrant.md).

:::{note}
Manual modifications required, as of QM 20.03.1:

* double-click on the Desktop symbols to show the icons
* delete examples/ icon on desktop
* fix issue with rabbitmq not shutting down ([#111](https://github.com/marvel-nccr/quantum-mobile/issues/111))

:::

### Cloud Edition

Follow the [cloud build instructions](../developers/build-cloud.md).

* For the server to build the VM, choose e.g. 2 CPUs with 4GB of RAM
  * Your configuration may also be the standard configuration shown to users creating a VM using your image (to figure out?)
  * You won't need it for long, so price for CPU/RAM is of no concern
* Exemplary metadata:
  * name: `quantum-mobile-20-05-0`  (GCP only allows alphanumeric characters + dashes)
  * family: `quantum-mobile`
  * description:

      Quantum Mobile Cloud Edition Server v20.05.0
      See https://github.com/marvel-nccr/quantum-mobile-cloud-edition

## Releasing the VM image

### Desktop Edition

* Fill in the manual sections of `dist/Release-<version>.md`
* upload contents of `dist/` to object store
  * `openstack object create marvel-vms Release-<version>.md`
  * `openstack object create marvel-vms quantum_mobile_<version>.ova`

* Prepare release:
  * in `dist/Release-<version>.md`, replace URL to object store by [bit.ly](https://bitly.com/) short-link
  * Copy `dist/Release-<version>.md` to `docs/releases/` and add the top-matter section.
  * update `CHANGELOG.md`
  * Commit changes of quantum-mobile repository to `develop` branch
  * merge into `master`
  * [create new GitHub release](https://github.com/marvel-nccr/quantum-mobile/releases/new), copying content of `dist/Release-<version>.md` (replace `Changelog` section with link to documentation) file and `CHANGELOG.md`



### Cloud Edition

* see [cloud build instructions](../developers/build-cloud.md).

:::{note}
Here are some indicative prices for hosting public images and disk pricing:

* Image pricing (for us to host it):
  * magnetic: 8.5c/GB/month (GCP)
* Disk pricing (for users):
  * magnetic: 4c/GB/month (GCP), 2.5c/GB/month (AWS)
  * SSD: 10c/GB/month (AWS)
