# Build for Apple Silicon

Apple Silicon is the new CPU architecture for Apple Macs. 
The new architecture is based on ARM64, which means that software compiled for x86_64 will not run on Apple Silicon without translation. 
The VirtualBox software is not yet available for Apple Silicon, so we need to use a different virtualization software which is the [UTM](https://mac.getutm.app/).

## Install and start the VM
- Download latest version of UTM
- browse gallery to have a image setup, we select ubuntu 20.04 LTS https://docs.getutm.app/guides/ubuntu/
- The arm64 ISO image can be dowloaded from https://cdimage.ubuntu.com/releases/focal/release/
- During import and setup from ISO, select settings with: 64GB disk space (default), 4096MB RAM (default), 4 (works for 2020 macbook air so should be good for other later model) cores.
- Remember to install OpenSSH server during setup, so we can ssh to the VM for ansible deployment.
- Create system user `max` with password `moritz` and enable auto login. This will be used for ansible deployment.
- Create a new network setting with type "Emulated VLAN" and forward port 22 to 2200 of localhost so you can ssh to VM from localhost.

<img src="images/utm_ports_mapping.png" width="350px">

You can config ssh with setting in `~/.ssh/config`:

```
Host qmobile
  HostName 127.0.0.1
  User max
  Port 2200
```

- The default `max` user is granted with the sudo permission and the password is `moritz`.
- To reboot, remember to unmount the image and boot again.

## Configure the VM

In the localhost (control machine), prepare the python environment and tox.
Check the [prerequisites section](../build-vagrant.md#prerequisites-installation) for detailes

Run with ansible playbook
```
BUILD_PLAYBOOK=playbook-aiidalab-qe.yml tox -e ansible -- --extra-vars "build_hosts=utm" -kK
```

It will ask for the password of `max` user, which is `moritz`.

## troubleshotings

### import from utm copy

- If you see "Failed to access data from shortcut", try the methods from https://github.com/utmapp/UTM/discussions/3774