# VirtualBox FAQ

## How do I set up a shared folder between the VM and my host?

1. Stop the VM
2. Add your folder in Machine => Settings => Shared Folders => Add Folder Icon
3. Choose "host" as the "Folder Name" (should be lowercase)
4. tick "Automount" (leave mount path free)
5. Start VM. The folder will appear in `/media/sf_<folder_name>`

**Warning:** Do not *distribute* VM images with enabled shared folders. Since VirtualBox can only share absolute paths on the host machine, users who don't have the particular path you shared will run into errors.

## How do I change the keyboard layout from the default (US English keyboard)?

 1. In the top right corner of your desktop, click on the down arrow to show the settings menu, and then click on the bottom-right icon showing a wrench and a screwdriver. This will open the Ubuntu "Settings" panel.
 2. On the left list, select "Region & Language"
 3. On the right, under "Input Sources", click on the "+" button.
 4. Click on the three vertical dots to see more choices for the keyboard layout.
 5. Start typing your language or layout name (e.g. "Spanish", "French", ...)
 6. If the keyboard layout still does not show up, click on "Other". Now you should see a full list of layouts that match what you wrote.
 7. Select the layout you want (often there are various variants depending on how you want to manage special symbols, accented letters, etc.). Then click on the green button "Add" that will appear at the top-right of the "Add an Input Source" window.
 8. Now you can choose the layout via the small menu on the top right of your desktop (it should show 'en' currently, for the default English US layout). If you prefer, you can remove any other input source from the list and only keep the one you want to use.

## How do I install a recent version of VirtualBox on Ubuntu?

Download corresponding .deb file from [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads) and do `sudo dpkg -i <deb-file>`.

:::{warning}
If you want to run VirtualBox on Ubuntu with Secure Boot enabled, you'll have to [sign the VirtualBox kernel extensions](https://askubuntu.com/questions/914997/install-virtualbox-while-keeping-secure-boot)
:::

## Icons and text are small on high-resolution screens. How do I enlarge them?

Increase the scale factor in Machine => Settings => Display => Scale Factor

## How to enable Audio?

1. Stop the VM
2. Go to Machine => Settings => Audio
3. Tick "Enable Audio" and select your desired Audio driver.
4. Start the VM.

## How do I manage VirtualBox from the command line (e.g. when running Quantum Mobile on a remote computer)?

1. Start VM: ``VBoxManage startvm "Quantum Mobile 20.03.1" --type headless``
2. Enter VM: ``ssh -p 2222 max@127.0.0.1``  
 Note: 2222 is the standard port. Use ``VBoxManage showvminfo "Quantum Mobile 20.03.1" | grep 'Rule'`` to check the port for your VM.
3. Stop VM: ``VBoxManage controlvm "Quantum Mobile 20.03.1" acpipowerbutton``
