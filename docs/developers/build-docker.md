# Build a Docker container

The procedure to build the docker container is the same as the for [building cloud VMs](./build-cloud.md).

Before running `tox -e ansible -- --extra-vars "build_hosts=docker"` though, initialise the base Docker container by running the `playbook-docker.yml` *via*:

```console
$ tox -e docker
```

Once provisioned, stop the container (to wipe the `/tmp` folder), then you can create a new image from the container by:

```console
$ docker commit -a "Author Name" -m "Container provisioned by ansible" qm_instance organisation/quantum-mobile:20.11.2a
```

If you have a Docker Hub account then you can also upload your image:

```console
$ docker login -u username -p password
$ docker push organisation/quantum-mobile:20.11.2a
```

:::{seealso}
The Visual Studio Code [Docker Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
:::
