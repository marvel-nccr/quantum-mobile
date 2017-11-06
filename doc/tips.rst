Modifying the VM
----------------
When modifying properties of the virtual machine, such as the #CPUs or the
amount of RAM, please note that you may need to update this information
in part of the installed software as well:

 * scheduler: The number of processors for the torque queue is pre-configured.
   <add instructions on how to change this>.
   See also `roles/scheduler/tasks/main.yml <https://github.com/marvel-nccr/marvel-virtualmachine/blob/master/roles/scheduler/tasks/main.yml>`_
 * aiida: The number of cores of the `localhost` computer are pre-configured.
   Just delete the computer and re-configure it again.
   See also `roles/aiida/templates/localhost.computer <https://github.com/marvel-nccr/marvel-virtualmachine/blob/master/roles/aiida/templates/localhost.computer>`_
