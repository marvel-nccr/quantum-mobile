## To start the machine:
# vagrant up
## To stop the machine:
# vagrant halt
## To destroy everything:
# vagrant destroy
## To provision again
# vagrant provision
## or
# vagrant provision --provision-with ansible
## To run only the ansible part

## NOTE!
## You need to have ansible (and vagrant) installed in your host; 
## remember to enter the virtualenv if you installed ansible inside it

## Note: you might also need to install a vagrant plugin, see below


# This guide is optimized for Vagrant 1.7 and above.
# Although versions 1.6.x should behave very similarly, it is recommended
# to upgrade instead of disabling the requirement below.
Vagrant.require_version ">= 1.7.0"

# From https://stackoverflow.com/questions/16708917/how-do-i-include-variables-in-my-vagrantfile
# to read variables from externale file
require 'yaml'
current_dir    = File.dirname(File.expand_path(__FILE__))
configs        = YAML.load_file("#{current_dir}/globalconfig.yml")
version = configs['vm_version']

Vagrant.configure(2) do |config|

  config.vm.provider "virtualbox" do |vb|

     vb.name = "MARVEL Virtual Machine #{version}"

     vb.memory = 1024
     vb.cpus = 2

     # To allow to graphically connect to it from the VirtualBox interface
     # (called 'show')
     vb.gui = true
   end

  # THE FOLLOWING NEEDS THE vbguest PLUGIN, that can be installed
  # AS 
  # vagrant plugin install vagrant-vbguest
  # we will try to autodetect this path. 
  # However, if we cannot or you have a special one you may pass it like:
  # config.vbguest.iso_path = "#{ENV['HOME']}/Downloads/VBoxGuestAdditions.iso"
  # or an URL:
  # config.vbguest.iso_path = "http://company.server/VirtualBox/%{version}/VBoxGuestAdditions.iso"
  # or relative to the Vagrantfile:
  # config.vbguest.iso_path = File.expand_path("../relative/path/to/VBoxGuestAdditions.iso", __FILE__)
  
  # set auto_update to false, if you do NOT want to check the correct 
  # additions version when booting this machine
  ## GP: I instead comment to check at every boot!
  # config.vbguest.auto_update = false
  
  # do NOT download the iso file from a webserver
  #config.vbguest.no_remote = true



  # 16.04
  config.vm.box = "ubuntu/xenial64"
  # Vagrant suggests to use bento
  #config.vm.box = "bento/ubuntu-16.04"

  # Disable the new default behavior introduced in Vagrant 1.7, to
  # ensure that all Vagrant machines will use the same SSH key pair.
  # See https://github.com/mitchellh/vagrant/issues/5005
  #config.ssh.insert_key = false

  #config.vm.base_mac = "022999D56C03"
  #config.ssh.username = "ubuntu"
  ## If needed, you can find the password inside the Vagrantfile
  ## inside your ~/.vagrant.d/boxes/ubuntu-VAGRANTSLASH-xenial64/20171006.0.0/virtualbox/Vagrantfile
  # or equivalent file
  #config.ssh.password = "38c8abcb7ae7bceda9947a5f"
  #                       509bd213fdcc4473a2db00e6

  config.vm.provision "bootstrap", type: "shell" do |s|
    s.inline = "apt-get update && apt-get install -y python2.7 python3"
  end

  # To run only this, run
  # vagrant provision --provision-with ansible
  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.extra_vars = {
       ansible_python_interpreter: "/usr/bin/python2.7"
    }
# Not sure this works...
#    ansible.tags = "wallpaper"
    ansible.playbook = "playbook.yml"
  end
end
