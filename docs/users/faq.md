# VirtualBox FAQ

:::{warning}
These notes are added over time, and some may be outdated.
If you notice anything incorrect, please open [an issue](https://github.com/marvel-nccr/quantum-mobile/issues/new?template=BLANK_ISSUE).
:::

:::{admonition} More questions?
If the following sections to not answer your question,
please direct further inquiries to the [Quantum Mobile support channel](https://aiida.discourse.group/c/quantum-mobile/) in the AiiDA Discourse.
:::

## How do I set up a shared folder between the VM and my host?

1. Stop the VM
2. Add your folder in Machine => Settings => Shared Folders => Add Folder Icon
3. Choose "host" as the "Folder Name" (should be lowercase)
4. tick "Automount" (leave mount path free)
5. Start VM. The folder will appear in `/media/sf_<folder_name>`

**Warning:** Do not *distribute* VM images with enabled shared folders. Since VirtualBox can only share absolute paths on the host machine, users who don't have the particular path you shared will run into errors.

## How do I change the keyboard layout from the default (US English keyboard)?

1. open the ubuntu settings within the VM (click on the ubuntu logo in the lower left corner, search for ``Settings``, and then click on it to launch)
2. go to ``Keyboard`` ➔ ``Input sources`` ➔ ``Add Input Source``
3. click on the ``⋮`` and add the desired language
4. Once added there you should be able to select the desired keyboard profile in a drop-down menu on the upper right corner of the screen.

## How do I install a recent version of VirtualBox on Ubuntu?

Download corresponding .deb file from [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads) and do `sudo dpkg -i <deb-file>`.

:::{warning}
VirtualBox might fail to start on Secure Boot-enabled Linux system, you can either 1) disable Secure Boot, please consult the user manual of the hardware manufacturer for the specific configuration in the BIOS/UEFI, or 2) [sign the VirtualBox kernel extensions](https://askubuntu.com/questions/914997/install-virtualbox-while-keeping-secure-boot), note you might need to re-sign the kernel module for each kernel update.
:::

## Icons and text are small on high-resolution screens. How do I enlarge them?

Increase the scale factor in Machine => Settings => Display => Scale

## How to enable Audio?

1. Stop the VM
2. Go to Machine => Settings => Audio
3. Tick "Enable Audio" and select your desired Audio driver.
4. Start the VM.
