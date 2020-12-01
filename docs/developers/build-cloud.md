# Build a cloud VM

In the following, we explain how to install Quantum Mobile on your own virtual machine in the cloud.

This procedure is automated entirely using an [ansible playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html) in the [quantum mobile repository](https://github.com/marvel-nccr/quantum-mobile).
It has been used successfully to deploy Quantum Mobile on servers from Amazon Web Services, Google Compute Cloud, Huawei Cloud, Openstack as well as on bare metal servers.

:::{note}
This process essentially a sub-set of the process to build the Desktop Edition ([see the instructions here](./build-vagrant.md)),
in that we are provisioning an existing VM, rather than creating one from scratch.
:::

## Prerequisites

### Server

- A server running Ubuntu 18.04 LTS
  Can be hardware or virtual machine (tested on OpenStack, Amazon Web Services and Huawei Cloud).
- At least 12GB disk size (including Ubuntu); better 15GB or more.
  Note: After cleaning temporary files, QM occupies ~6GB of disk space.
- Access to server via SSH key as user with `sudo` rights

Security rules:

- Port 22 open (for SSH access)
- You may want to open further ports (optional):
  - port 8888 to connect to the AiiDA Lab Server
  - port 8890 to connect to thr Jupyter Lab Server
  - port 5000 to connect to the AiiDA REST API

### Client (your computer)

- [python](https://www.python.org/) >= 3.6
- [git](https://git-scm.com)

## Provisioning the server

To get set up, run the following on your client (e.g. your laptop -- *not* on the server itself):

```bash
git clone https://github.com/marvel-nccr/quantum-mobile.git
cd quantum-mobile
```

The `inventory.yml` already contains templates for connecting to servers from different cloud providers, which are easy to populate with the connection details for your server.
For example, to connect to an `aws` host, adapt:

```yaml
    aws:
      cloud_platform: aws
      ansible_host: 34.250.68.129 # change this
      ansible_ssh_common_args: -i ./keys/quantum-mobile.pem -o StrictHostKeyChecking=no
      ansible_user: ubuntu
```

with:

- the IP of the server
- the path to your private SSH key for connecting to the server
- the user to connect as via SSH

:::{seealso}
The [ansible inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) and [playbook variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) documentation.
:::

You may also want to "tune" the variables under `vars:` in `inventory.yml`, such as:

- `vm_user`: the user for which to install the simulation environment (usually *not* the admin user you are connecting as)
- `vm_memory`, `vm_cpus`
- If you want to pre-load an SSH public key for the `vm_user` to connect with (as opposed to the admin key set above),
  uncomment and set the `add_user_public_key` variable.

Finally, to run the ansible playbook against the required host, use:

```bash
pip install tox
tox -e ansible -- --extra-vars "build_hosts=aws"
```

This will take of the order of one hour, after which your server should be fully deployed and operational.

:::{tip}
The ansible steps are idempotent, meaning they will essentially do nothing when run again on the same machine.

This means, if the build was interrupted for any reason, you can simply re-run the above command.
:::

You can log in to the server as the `vm_user` via the public SSH key you provided.

## Saving the image

Before creating an image from the disk volume of the server you provisioned:

1. Remove unnecessary temporary build files:

   ```bash
   tox -e ansible -- --tags quantum_espresso,qm_customizations,simulationbase,ubuntu_desktop --extra-vars "build_hosts=aws clean=true"
   ```

2. Clear bash history:  SSH to the VM and run `cat /dev/null > ~/.bash_history && history -c && exit`

3. Shut down instance (this will clear temporary data in `/tmp`)

Now follow the instructions of your platform for creating an image from your server.

## Platform specific guidance

### AWS

- Create new keypair from the GUI - note: this will always be added to the `ubuntu` user.

- If you intend to publish the image, follow AWS instructions to remove system SSH keys:  
   `sudo shred -u /etc/ssh/*_key /etc/ssh/*_key.pub`

- Listing an image publicly: After creation of the image, edit its properties and select "public"

### GCP

- GCP lets you create the SSH key-pair by yourself:
  - Create new SSH keypair on your machine.
  - Edit the `user@server` bit at the end of the public key to user "ubuntu" (GCP detects this user and adds the SSH public key for this user in the VM)
  - add public key to VM

- VM IP seems to be stable even between stop/start of VM

- Creating the image
  - GCP distinguishes between "Machine images" (private) and "Images" (can be public). You want the second option.
  - List image publicly: (not sure whether there is a way to do this via the GUI)
    - Click on "cloud shell" logo on the top right
    - Paste command:

      ```bash
      gcloud compute images add-iam-policy-binding quantum-mobile-20-05-0 \
         --member='allAuthenticatedUsers' \
         --role='roles/compute.imageUser'
      ```

## Troubleshooting

### Slow network connection

When provisioning machines in remote networks (e.g. Asia), the time needed for establishing an SSH connection can be prohibitively slow.
In such cases, the "mitogen" connection plugin can lead to dramatic speedups (it uses python remote procedure calls).

In order to enable mitogen, execute the following command:

```bash
wget https://networkgenomics.com/try/mitogen-0.2.8.tar.gz && tar xf mitogen-0.2.8.tar.gz
```

and uncomment the corresponding lines in the `ansible.cfg` file.

In my tests, an example task (adding the "max" user to two new user groups) took 15s on an AWS VM in the hongkong region, and 156s on a Huawei Cloud VM in the Guangzhou region (and that's after turning on "pipelining" to reduce the number of SSH connections).
Switching to mitogen brought down the timings to 1s for the AWS hongkong machine and 3s on the Huawei VM (i.e. more than one order of magnitude).
