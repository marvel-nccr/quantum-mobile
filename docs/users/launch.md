# Launching Quantum Mobile

(launch/vagrant)=
## Desktop Edition with VirtualBox

- Download the latest VirtualBox image from [the releases](../releases/index.md)
- Install [Virtual Box](https://www.virtualbox.org) 6.1.6 or later
- Import the virtual machine image into Virtualbox: `File => Import Appliance`

(launch/docker)=
## Docker Container

The Docker images can be found on [DockerHub](https://hub.docker.com/r/marvelnccr/quantum-mobile).
The easiest way to spawn a working container is to create a `docker-compose.yml`, and launch it with `docker-compose up -d`.

```yaml
version: '3.4'

services:
  quantum-mobile:
    # using the required tag
    image: "marvelnccr/quantum-mobile:20.11.2a"
    container_name: quantum-mobile
    expose:
      - "8888" # AiiDa Lab
      - "8890" # Jupyter Lab
      # - "5000" # REST API
    ports:
      # local:container
      - 8888:8888
      - 8890:8890
      # - 5000:5000
    # privileged mode and mounting the cgroup are required for correctly running sytsemd inside the container (set as the default command)
    privileged: true
    volumes:
      - "/sys/fs/cgroup:/sys/fs/cgroup:ro"
    environment:
      LC_ALL: "en_US.UTF-8"
      LANG: "en_US.UTF-8"
    healthcheck:
      # check that the daemon has been started for the 'generic' profile
      # can take a few minutes to start
      test: systemctl is-active --quiet aiida-daemon@generic.service
      interval: 30s
      retries: 6
      start_period: 30s
```

Once launched, the container should take a minute or two to begin the required services for AiiDA, at which point it will report healthy:

```console
$ docker inspect --format "{{.State.Health.Status}}" quantum-mobile
healthy
```

You can then enter the container as the `max` user:

```console
$ docker exec -it --user max quantum-mobile /bin/bash
$ max@qmobile:/$ workon aiida
(aiida) max@qmobile:/$ verdi status
```

When you are finished with the container, you can destroy it:

```console
$ docker-compose down -v
```

:::{seealso}
The Visual Studio Code [Docker Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
:::

(launch/cloud)=
## Cloud Edition on remote server

:::{note}
Although Quantum Mobile is free and open-source, running a server on a cloud platform cloud will incur a cost.
:::

- Find the latest [Cloud Edition image](../releases/index.md)
- Follow the instructions below for the cloud platform of your choice
- If the cloud platform of your choice is not among the list, you can [build your own cloud VM](../developers/build-cloud.md)

We have started offering pre-built Quantum Mobile images on a selection of cloud providers, such as Amazon Web Services and the Google Cloud Platform, since this allows launching a VM from such an image with just a few clicks.

We are in the process of evaluating which platforms to target and whether to release a separate image for the Cloud Edition (e.g. in `ova` format).
Your feedback is welcome!

(launch/aws)=
### Amazon Web Services (AWS)

:::{admonition} Prerequisites

- An account on [aws.amazon.com](https://aws.amazon.com/account/)
:::

- Open the Amazon EC2 console at <https://console.aws.amazon.com/ec2/>.
- Click "Launch instance"
- Select "Community AMIs"
- Enter AMI ID in search bar (without `ami-` prefix, e.g.: `006638a0a99849fc3`)
- Select Quantum Mobile AMI
- Select instance type depending on your computational needs (e.g. `t2.medium`)
- (optional) click through to storage section if you need to change the disk size from the default of 15GB
- Click "Review and Launch"
- Click "Launch"
- Create a new key pair
- Launch the VM

:::{important}
Since Quantum Mobile is based on the Ubuntu image, the SSH public key will be added to the `ubuntu` user (hardcoded by AWS),
while the simulation environment has been set up for the `max` user.

In order to log in as the `max` user using your key, do the following:

```bash
ssh ubuntu@<IP> -i /path/to/key.pem  # or use putty, ...
sudo cat ~ubuntu/.ssh/authorized_keys >> ~max/.ssh/authorized_keys
exit
```

Now you can log in as the `max` user:

```bash
ssh max@<IP> -i /path/to/key.pem
```

:::

(launch/gcp)=
### Google Cloud Platform (GCP)

:::{admonition} Prerequisites

- An account on [cloud.google.com](https://cloud.google.com/)
- A project with Compute Engine API enabled (see their [quickstart docs](https://cloud.google.com/compute/docs/quickstart-linux))
:::

- Go to one of the links in [the releases page](../releases/index.md), such as [quantum-mobile-20-05-0](https://console.cloud.google.com/compute/imagesDetail/projects/marvel-nccr/global/images/quantum-mobile-20-05-0)  
- Click on "CREATE INSTANCE"
- Adapt VM to your needs
- Use `ssh-keygen` on your machine to create an SSH private-public key pair
- Open the public key in a text editor & edit the `user@server` bit at the end, replacing `user` by `max`
- Under "Security", copy-paste the public SSH key  
 (GCP will add this key to the `max` user)
- Click on "Create"
- Copy IP address

After a few seconds, you should be able to log in to your new server *via*:

```bash
ssh max@<IP> -i /path/to/key.pem
```

### Setting up the SSH connection

#### Linux and MacOS

Place the private ssh key that provides access to your server in the SSH key directory:

- If you don't already have a `.ssh` directory in your homefolder, create it and set its permissions:
  ```bash
  mkdir ~/.ssh
  chmod 700 ~/.ssh
  ```
- Copy the private key (let's call it `key.pem`) into the `~/.ssh` directory
- Set the correct permissions on the private key `chmod 600 ~/.ssh/key.pem`. 
  The permissions shown by `ls -l` should be `-rw-------`.

Once the ssh key is in place, add the following block your `~/.ssh/config` file (create it if it does not exist):

```bash
Host qmcloud
   Hostname IP_ADDRESS
   User max
   IdentityFile ~/.ssh/key.pem
   ForwardX11 yes
   ForwardX11Trusted yes
   LocalForward 8888 localhost:8888
   LocalForward 8890 localhost:8890
   LocalForward 5000 localhost:5000
   ServerAliveInterval 120
```

replacing the IP address (`IP_ADDRESS`) with the one for the cloud VM.

Afterwards you can connect to the server using:

```console
$ ssh qmcloud
```

:::

:::{note}
On MacOS you need to install [XQuartz](https://xquartz.macosforge.org/landing/) in order to use X-forwarding.
:::

:::{tip}
If your port 8888 is already occupied (e.g. because you are running a `jupyter notebook` server locally), you may see the following warning when connecting to the server:

```
bind [127.0.0.1]:8888: Address already in use
channel_setup_fwd_listener_tcpip: cannot listen to port: 8888
```
We suggest you stop any locally running jupyter notebook servers before connecting to the VM.
If necessary, you can start them again *after* you have connected (`jupyter notebook` will then realize that port 8888 is already taken and simply serve the notebook on a different port).

:::

#### Windows

If you're running Windows 10, consider [installing the Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) (and then follow the instructions above).

Alternatively:

- Install the [PuTTY SSH client](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
- Run PuTTYGen
  - Load the `key.pem` private key (button "Load").
    You may need to choose to show "All files (*.*)", and select the file without any extension (Type: File).
  - In the same window, click on "Save private Key", and save the key with the name `key.ppk` (don't specify a password).

- Run Pageant
  - It will add a new icon near the clock, in the bottom right of your screen.
  - Right click on this Pageant icon, and click on “View Keys”.
  - Click on "Add key" and select the `key.ppk` you saved a few steps above.

- Run PuTTY
  - Put the given IP address as hostname, type `qmcloud` in "Saved Sessions" and click "Save".
  - Go to Connection > Data and put `max` as autologin username.
  - Go to Connection > SSH > Tunnels, type `8888` in the "Source Port" box, type `localhost:8888` in "Destination" and click "Add".
  - Repeat the previous step for port `5000` and `8890` instead of `8888`.
  - Go back to the "Session" screen, select "qmcloud" and click "Save"
  - Finally, click "Open" (and click "Yes" on the putty security alert to add the VM to your known hosts).
    You should be redirected to a bash terminal on the virtual machine.

:::{note}
Next time you open PuTTY, select `qmcloud` and click "Load" before clicking "Open".
:::

In order to enable X-forwarding:

- Install the [Xming X Server for Windows](http://sourceforge.net/projects/xming/).
- Configure PuTTy as described in the [Xming wiki](https://wiki.centos.org/HowTos/Xming).
