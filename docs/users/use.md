# Using Quantum Mobile

:::{note}
This guide assumes the standard build of Quantum Mobile.
:::

Once you have launched a flavour of Quantum Mobile, login in as the `max` user.

In the `/home/max/Desktop` directory, you will find two files with helpful information about the software available on you VM:

- `${HOME}/Desktop/release_notes.txt`
- `${HOME}/Desktop/README.md`

## Checking the services (systemd)

The VM utilises [systemd](https://en.wikipedia.org/wiki/Systemd) to manage the services required for running AiiDA.

To check the running service, open a terminal and run:

```console
max@qmobile:/$ systemctl --type=service
UNIT                               LOAD   ACTIVE SUB     DESCRIPTION
aiida-daemon@generic.service       loaded active running AiiDA daemon service for pro
postgresql@10-main.service         loaded active running PostgreSQL Cluster 10-main
rabbitmq-server.service            loaded active running RabbitMQ Messaging Server  
slurmctld.service                  loaded active running Slurm controller daemon
slurmd.service                     loaded active running Slurm node daemon
ssh.service                        loaded active running OpenBSD Secure Shell server
```

This highlights the core services required for running computations with AiiDA:

- postgresql: Database service for storing data
- rabbitmq: Messaging service for storage of running AiiDA process data
- slurm: Scheduler service for managing computation processes
- aiida-daemon: Daemon service for running (non-blocking) processes in the background

For slurm, there is also an start-up service, to set the correct hostname and CPU resources of the VM:

```console
$ systemctl status slurm-resources
 slurm-resources.service - Set SLURM compute resources
   Loaded: loaded (/etc/systemd/system/slurm-resources.service; enabled; vendor prese
   Active: inactive (dead) since Wed 2020-12-09 15:20:34 UTC; 17min ago
  Process: 43 ExecStart=/usr/bin/ansible-playbook /etc/slurm-llnl/update-playbook.yml
 Main PID: 43 (code=exited, status=0/SUCCESS)
```

If a service has failed, you can try starting again, and also check for failures in other parts of its dependency chain:

```console
$ systemctl start slurmd.service
$ systemd-analyze critical-chain slurmd.service
$ systemctl list-dependencies --before slurm-resources
```

## Checking the slurm scheduler

As discussed above, the slurm scheduler is initialised on start-up,
with automation for configuration the correct hostname and CPU resources.
You can check the slurm configured node and partition:

```console
$ sinfo
$ scontrol show node
$ scontrol show partition
```

The CPU resources should match those shown with `lscpu`.

You can reset the resources and also change the maximum number of CPUs available to the partition using the `slurm-resources` CLI:

```console
$ slurm-resources -e restart_on_change=true -e slurm_max_cpus=2
```

## Working with AiiDA

In the terminal, you can enable python environments using the [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io) commands.
To enable the the environment that AiiDA is installed in, to use the `verdi` CLI:

```console
max@qmobile:/$ workon aiida
(aiida) max@qmobile:/$ verdi status
 ✔ config dir:  /home/max/.aiida
 ✔ profile:     On profile generic
 ✔ repository:  /home/max/.aiida/repository/generic
 ✔ postgres:    Connected as aiida@localhost:5432
 ✔ rabbitmq:    Connected as amqp://guest:guest@127.0.0.1:5672?heartbeat=600
 ✔ daemon:      Daemon is running as PID 1009 since 2020-12-08 04:47:01
```

A computer is set-up to run jobs on the slurm scheduler.
You can check that it is working correctly using:

```console
(aiida) max@qmobile:/$ verdi computer test localhost
Info: Testing computer<localhost> for user<aiida@localhost>...
* Opening connection... [OK]
* Checking for spurious output... [OK]
* Getting number of jobs from scheduler... [OK]: 0 jobs found in the queue
* Determining remote user name... [OK]: max
* Creating and deleting temporary file... [OK]
Success: all 5 tests succeeded
```

Each AiiDA plugin has one or more codes set up with this computer:

```console
(aiida) max@f7762ccd7ce9:/$ verdi code list
# List of configured codes:
# (use 'verdi code show CODEID' to see the details)
* pk 1 - abinit-0.1.0a0-abinit@localhost
* pk 2 - bigdft-0.2.1a2-bigdft@localhost
* pk 3 - cp2k-1.2.0-cp2k@localhost
* pk 4 - fleur-1.1.2-fleur_MPI@localhost
* pk 5 - fleur-1.1.2-inpgen@localhost
* pk 6 - qe-3.2.0-pw@localhost
* pk 7 - qe-3.2.0-cp@localhost
* pk 8 - qe-3.2.0-pp@localhost
* pk 9 - qe-3.2.0-ph@localhost
* pk 10 - qe-3.2.0-neb@localhost
* pk 11 - qe-3.2.0-projwfc@localhost
* pk 12 - qe-3.2.0-pw2wannier90@localhost
* pk 13 - qe-3.2.0-q2r@localhost
* pk 14 - qe-3.2.0-dos@localhost
* pk 15 - qe-3.2.0-matdyn@localhost
* pk 16 - siesta-1.1.0-siesta@localhost
* pk 17 - siesta-1.1.0-plstm@localhost
* pk 18 - wannier90-2.0.1-wannier@localhost
* pk 19 - yambo-1.1.3-yambo@localhost
* pk 20 - yambo-1.1.3-p2y@localhost
```

:::{note}
All codes are set to default to use
2 CPUs, irrespective of the number available on the VM.
Set the number specifically if you require a different amount.
:::

An example of a simple process run test is to use the auxiliary `aiida-quantumespresso` CLI:

```console
(aiida) max@qmobile:/$ aiida-quantumespresso calculation launch pw -d -i -X qe-3.2.0-pw@localhost -p SSSP_1.1_efficiency
Submitted PwCalculation<205> to the daemon
(aiida) max@qmobile:/$ verdi process list -a
  PK  Created    Process label    Process State    Process status
----  ---------  ---------------  ---------------  ----------------
 205  21s ago    PwCalculation    ⏹ Finished [0]

Total results: 1

Info: last time an entry changed state: 8s ago (at 05:12:38 on 2020-12-08)
```

:::{seealso}
The [aiida-core documentation](https://aiida.readthedocs.io)
:::

## Working with Jupyter and AiiDA Lab

It is important to note that the Jupyter Python environment is **different** to that of the AiiDA one,
the `aiida` environment is instead installed as a kernel for Jupyter to use.

To activate the `jupyter` environment and check the kernels installed:

```console
$ workon jupyter
(jupyter) max@qmobile:/$ jupyter kernelspec list
Available kernels:
  python3    /home/max/.local/share/jupyter/kernels/python3
(jupyter) max@qmobile:/$ cat /home/max/.local/share/jupyter/kernels/python3/kernel.json
{
 "argv": [
  "/home/max/.virtualenvs/aiida/bin/python",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "Python 3",
 "language": "python"
```

To check the currently running servers:

```console
(jupyter) max@qmobile:/$ jupyter notebook list
```

You can start Jupyter Lab by either running `jupyter lab` in the `jupyter` environment or running `aiida-jupyterlab` from anywhere.
The latter is preferred, since will only ever open the same port and not create duplicate servers.
You should also ensure that you are in the $HOME directory:

```console
$ cd $HOME
$ aiida-jupyterlab
```

Similarly you can start AiiDA Lab using the `aiida-aiidalab` command.

:::{seealso}
The [AiiDAlab documentation](https://www.materialscloud.org/aiidalab/)
:::

If you are using the VirtualBox GUI, you can also double-click on the short-cut icons.

![VM Desktop](../_static/quantum_mobile.png)
