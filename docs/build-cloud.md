# Building cloud

If your platform of choice is not listed above or if you would like to customize Quantum Mobile, you will need to build the image yourself.

This procedure is automated entirely using the [ansible playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html) in this repository, which has been used successfully to deploy Quantum Mobile on Amazon Web Services, Google Compute Cloud, Huawei Cloud, Openstack as well as on bare metal servers.

## Prerequisites

### Server
- A server running Ubuntu 18.04 LTS
  Can be hardware or virtual machine (tested on OpenStack, Amazon Web Services and Huawei Cloud).
- At least 12GB disk size (including Ubuntu); better 15GB or more.  
  Note: After cleaning temporary files, QM 20.3.1 occupied 6.1GB of disk space.
- Access to server via SSH key as user with sudo rights

For peculiarities of different platforms, see [the wiki](https://github.com/marvel-nccr/quantum-mobile-cloud-edition/wiki/Preparing-a-cloud-image).

Security rules:
- Port 22 open (for SSH access)
- You may want to open further ports (optional):
  - port 8888 to connect to Jupyter Notebook Servers (AiiDA lab)
  - port 5000 to connect to the AiiDA REST API

### Client (your computer)
- [python](https://www.python.org/)
- [git](https://git-scm.com)

To get set up, run the following on your client (e.g. your laptop -- *not* on the server itself):
```
git clone https://github.com/marvel-nccr/quantum-mobile-cloud-edition.git
cd quantum-mobile-cloud-edition
pip install -r requirements.txt  # installs python requirements
ansible-galaxy install -r requirements.yml  # installs ansible roles
```

## Provisioning the server

1. Add your server to the [ansible inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) in the `hosts` file, e.g.
   ```
   [myplatform]
   qm ansible_host=1.1.1.1
   ```
1. Adapt the corresponding `./group_vars/*.yml` file (or create your own), with
   * the path to your private SSH key for connecting to the server
   * the user to connect as via SSH
1. Tune the `globalconfig.yml` file, in particular:
   * `vm_user`: the user for which to install the simulation environment (usually *not* the admin user you are connecting as)
   * `vm_memory`, `vm_cpus`
1. (optional) adaptation of the ansible `playbook.yml`
   * 
   * You want to preload a SSH public key for the `vm_user`?  
   Then uncomment the `"add user {{ vm_user }} with key"` role and adjust the path to the public key in the lookup for the `add_user_public_key` variable
   * Add/remove further roles depending on what you want to have in the image
1. run `ansible-playbook playbook.yml`

Your server should now be fully deployed and operational.

You can log in to the server as the `vm_user` via the public SSH key you provided.

## Saving the image

Before creating an image from the disk volume of the server you provisioned:

1. Remove unnecessary temporary files:  
   `ansible-playbook playbook.yml --extra-vars "clean=true" --tags qm_customizations,simulationbase`

1. Clear bash history: `cat /dev/null > ~/.bash_history && history -c && exit`

1. Shut down instance (this will clear temporary data in `/tmp`)

Now follow the instructions of your platform for creating an image from your server.

Note: If you plan to *publish* the image, see [the wiki](https://github.com/marvel-nccr/quantum-mobile-cloud-edition/wiki/Preparing-a-cloud-image) for further tips.

## Tweaks

### Slow network connection

When provisioning machines in remote networks (e.g. Asia), the time needed for establishing an SSH connection can be prohibitively slow.
In such cases, the "mitogen" connection plugin can lead to dramatic speedups (it uses python remote procedure calls).

In order to enable mitogen, execute the following command
```
wget https://networkgenomics.com/try/mitogen-0.2.8.tar.gz && tar xf mitogen-0.2.8.tar.gz
```
and uncomment the corresponding lines in the `ansible.cfg` file.

In my tests, an example task (adding the "max" user to two new user groups) took 15s on an AWS VM in the hongkong region, and 156s on a Huawei Cloud VM in the Guangzhou region (and that's after turning on "pipelining" to reduce the number of SSH connections).
Switching to mitogen brought down the timings to 1s for the AWS hongkong machine and 3s on the Huawei VM (i.e. more than one order of magnitude).
