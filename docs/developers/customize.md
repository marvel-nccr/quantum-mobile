# Customizing Quantum Mobile

There are at least two ways to customize Quantum Mobile in order to fit your needs:

## Manual approach (quick & dirty)

* **PRO**: quick, no need to learn how to use ansible / vagrant
* **CON**: no clear record of changes; you may need to redo this the next time

If you just need minor modifications (e.g. add a PDF to the Desktop / install a simple tool),
you can do the following:

 1. Download the latest version of the Quantum Mobile VirtualBox image
 2. Start it and modify according to your needs
 3. Create a new image of the modified virtual machine:
    * Perform a clean shutdown from the Ubuntu menu, wait for the VM window to close
    * In the main VirtualBox window, select the VM and rename it to a short and specific name
    * With the VM still selected, go to `File => "Export Appliance"`.
    * Default parameters should be ok but feel free to adapt them to your needs.

This creates a new OVA file that you can share.
You might want to test reimporting it on a different computer to check that it works correctly.

:::{tip}
We suggest you keep an eye on the size of your VM and the final OVA image as there are often users who don't have much disk space to spare.
When you modify the VM, the size of the (virtual) disk increases automatically as needed but it may **not shrink when you delete files**.

When following the reproducible approach (see below), you can use the `playbook-package.yml` (specifically the `clean` and `compact` tags) to shrink the disk back to the size that is actually needed, which can dramatically reduce image size.
:::

## Reproducible approach (suggested)

* **PRO**: reusable & automatic - next time, you can apply the same recipe to a newer version of Quantum Mobile
* **PRO**: easy to decrease size by removing components from Quantum Mobile that you don't need
* **PRO**: others can benefit from your work; your additions might become part of a future Quantum Mobile release
* **CON**: need to learn how to work with ansible / vagrant

Quantum Mobile encapsulates components in
[ansible roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html), which are selected in the `playbook-build.yml` file.
You can choose from our [growing repository of roles](https://galaxy.ansible.com/marvel-nccr) or write your own.

If you need to install a new simulation code or want to remove components from quantum mobile:

1. See [Creating and testing roles](./roles.md) on how to create an ansible role for your code
2. Fork the quantum-mobile GitHub repository
3. Add/remove roles in the `playbook-build.yml` file
4. Adapt `inventory.yml`, `resources/EULA.txt` and `README.md` appropriately
5. Follow the [Instructions for building Quantum Mobile](./build-vagrant.md) to build your VM from scratch

## Publishing customized VMs

You are free to publish customized images of Quantum Mobile, as long as you include with it the original `LICENSE.txt`.

If you do so, we recommend that you:

* Give your VM a different name to avoid confusion
* Adapt the EULA appropriately

In all cases, we appreciate if you acknowledge that your VM has been adapted from the Quantum Mobile.
