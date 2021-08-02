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

One way to check that the latest ansible roles are being used in the `requirements.yml` file,
is to use the [GitHub GraphQL](https://developer.github.com/v4/) query:

```
# endpoint = https://api.github.com/graphql
{
  search(query: "org:marvel-nccr ansible-role in:repo", type: REPOSITORY, first: 100) {
    nodes {
      ... on Repository {
        name
        refs(refPrefix: "refs/tags/", last: 1) {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}
```

After updating `requirements.yml`, be sure to run:

```bash
tox -e update-ansible
```

to force upgrade of the downloaded roles.

## Provisioning the VM

### Desktop Edition

Ensure Vagrant is updated , and to update the base box and plugins you can run:

```bash
tox -e update-vagrant
```

Follow the [desktop build instructions](../developers/build-vagrant.md).

:::{note}
Manual modifications required, as of QM 20.03.1:

* Double-click on the Desktop symbols to show the icons (see [#150](https://github.com/marvel-nccr/quantum-mobile/issues/150)) or just run in the VM terminal (press F5 after to refresh):

  ```bash
  for FILE in ${HOME}/Desktop/*.desktop; do gio set "$FILE" "metadata::trusted" yes; done
  ```

:::

### Cloud Edition

Follow the [cloud build instructions](../developers/build-cloud.md).

* For the server to build the VM, choose e.g. 2 CPUs with 4GB of RAM, with at least 16GB of storage.
  * Your configuration may also be the standard configuration shown to users creating a VM using your image
  * Currently Ubuntu Server 18.04 LTS
  * Expose ports as listed in instructions
  * You won't need it for long, so price for CPU/RAM is of no concern
* Exemplary metadata:
  * name: `quantum-mobile-20-05-0`  (GCP only allows alphanumeric characters + dashes)
  * family: `quantum-mobile`
  * description:

      Quantum Mobile Cloud Edition Server v20.05.0
      See https://github.com/marvel-nccr/quantum-mobile-cloud-edition

## Releasing the VM image

To prepare the release:

* Fill in the manual sections of `dist/Release-<version>.md`
* Release the distributions (see below)
* Copy `dist/Release-<version>.md` to `docs/releases/` and add the top-matter section.
* Update `CHANGELOG.md`
* Commit changes of quantum-mobile repository to `main` branch
* [create new GitHub release](https://github.com/marvel-nccr/quantum-mobile/releases/new), copying content of `dist/Release-<version>.md` (replace `Changelog` section with link to documentation) file and `CHANGELOG.md`

### Desktop Edition

Releases should be uploaded to the `mrcloud` openstack account and `marvel-vms` container.

If you have authentication to this project, you can generate the API key and other environmental variables necessary to connect using:

(this will ask for your username and password)
```console
$ tox -e openstack-api
...
TASK [Print environment]
ok: [localhost] =>
  msg:
  - |-
    export OS_AUTH_URL=https://pollux.cscs.ch:13000/v3
    export OS_IDENTITY_PROVIDER_URL=https://auth.cscs.ch/auth/realms/cscs/protocol/saml/
    export OS_PROTOCOL=mapped
    export OS_IDENTITY_API_VERSION=3
    export OS_AUTH_TYPE=token
    export OS_IDENTITY_PROVIDER=cscskc
    export OS_INTERFACE=public
...
```

Copy/paste these export commands into the terminal, then you can use the openstack CLI *via*:

```console
$ tox -e openstack -- object list marvel-vms
```

Upload contents of `dist/` to object store
  
```console
$ tox -e openstack -- openstack object create marvel-vms dist/Release-<version>.md
$ tox -e openstack -- openstack object create marvel-vms dist/quantum_mobile_<version>.ova
```

Finally generate a short-link for the object store URL with [bit.ly](https://bitly.com/),
then replace the URL in `dist/Release-<version>.md`.

### Cloud Edition

* see [cloud build instructions](../developers/build-cloud.md).

:::{note}
Here are some indicative prices for hosting public images and disk pricing:

* Image pricing (for us to host it):
  * magnetic: 8.5c/GB/month (GCP)
* Disk pricing (for users):
  * magnetic: 4c/GB/month (GCP), 2.5c/GB/month (AWS)
  * SSD: 10c/GB/month (AWS)
:::

### Docker Image

You can either build the container locally, using the [Docker build instructions](../developers/build-docker.md), then commit the (stopped) instance:

```bash
docker commit -a "Chris Sewell" -m "Container provisioned by ansible" qm_instance marvelnccr/quantum-mobile:20.11.2a
```

or (recommended) first tag the release commit with a `docker-` tag, to trigger the GitHub Action (see [Testing on GH Actions](./develop.md)).
Then, once the build has successfully run and uploaded to Docker Hub, pull the created image and create the new tag:

```bash
docker pull marvelnccr/quantum-mobile:develop
docker tag marvelnccr/quantum-mobile:develop marvelnccr/quantum-mobile:20.11.2a
```

Next use the `docker-compose.yml` in the repository base (changing the image name) to launch the container and check that you can correctly run through the commands in [Using Quantum Mobile](../users/use.md).

Finally, upload the tag to Docker Hub.

```bash
docker login -u username -p password
docker push marvelnccr/quantum-mobile:20.11.2a
```
