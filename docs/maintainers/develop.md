# Developing Quantum Mobile

## Code style

Code style is tested using pre-commit:

```bash
pip install pre-commit
pre-commit run --all
```

## Updating the documentation

```bash
pip install tox
# to build from scratch
tox -e docs-clean
# to start a live server (reloads automatically on changes to documentation)
tox -e docs-live
```

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

Follow the [vagrant build instructions](../developers/build-vagrant.md)

:::{note}
One step that is currently not automated is to double-click on the Desktop symbols to show the icons.
:::

### Releasing the VM

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
  * [create new release](https://github.com/marvel-nccr/quantum-mobile/releases/new), copying content of `dist/Release-<version>.md` (replace `Changelog` section with link to documentation) file and `CHANGELOG.md`

Extra modifications as of QM 20.03.1:

* delete examples/ icon on desktop
* fix issue with rabbitmq not shutting down ([#111](https://github.com/marvel-nccr/quantum-mobile/issues/111))

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

### Pricing

Although quantum-mobile is free and open-source, hosting a server on a cloud platform like Amazon (AWS) and Google (GCP) cloud, will incur a cost.

Here are some indicative prices for this service:

* Image pricing (for us to host it):
  * magnetic: 8.5c/GB/month (GCP)
* Disk pricing (for users):
  * magnetic: 4c/GB/month (GCP), 2.5c/GB/month (AWS)
  * SSD: 10c/GB/month (AWS)
