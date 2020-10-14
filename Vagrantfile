Vagrant.require_version ">= 2.0.0"

## Read global configuration file from YAML
require 'yaml'
current_dir    = File.dirname(File.expand_path(__FILE__))
inventory      = YAML.load_file("#{current_dir}/inventory.yml")
# host specific variables take priority over global ones
gconfig        = inventory['all']['vars'].merge(inventory['all']['hosts']['vagrant-provision'])
launch_gui     = ENV.has_key?('VAGRANT_NO_GUI') ? false : true

# Currently on GitHub Actions it fails if more than 1 CPU or accelerate3d activated
on_ci          = ENV.has_key?('VAGRANT_ON_GH') ? true : false

Vagrant.configure(2) do |config|

  ## VIRTUALBOX provider
  config.vm.provider "virtualbox" do |vb|

     ## Machine name inside VirtualBox
     vb.name = gconfig['vm_name'] + ' ' + gconfig['vm_version']

     ## Resource details
     vb.memory = gconfig['vm_memory']
     if on_ci
      vb.cpus = gconfig['vm_cpus']
     else
      vb.cpus = 1
     end

     ## To allow to graphically connect to it from the VirtualBox interface
     ## (called 'show in the VirtualBox GUI')
     vb.gui = launch_gui

     # More customizations
     # See https://www.virtualbox.org/manual/ch08.html
     vb.customize ["modifyvm", :id, "--vram", gconfig['vm_vram']]
     # makes mouse/typing more responsive
     if !(on_ci)
      vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
     end
     # see https://github.com/marvel-nccr/quantum-mobile/issues/99
     vb.customize ["modifyvm", :id, "--graphicscontroller", "vmsvga"]
     vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
     vb.customize ["modifyvm", :id, "--draganddrop", "bidirectional"]
     # turn off remote display (requires Virtualbox Extension pack)
     vb.customize ["modifyvm", :id, "--vrde", "off"]

     # enable audio (default changed to off in virtualbox 6)
     # vb.customize ["modifyvm", :id, "--audio", "coreaudio"]
     vb.customize ["modifyvm", :id, "--audioout", "on"]

     # prevent VM time slipping out of sync by more than 10s (default: 20 min)
     vb.customize [ "guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 10000 ]
   end

  # Vagrant automatically updates the Guest Additions on 'vagrant up'
  # (this requires 'vagrant plugin install vbguest')
  # To disable this, uncomment the following
  #config.vbguest.auto_update = false 
  #config.vbguest.no_install = true
   
  # Uncomment to avoid remote downloads of ISO
  #config.vbguest.no_remote = true

  config.vm.box = gconfig["vm_base_image"]
  config.vm.boot_timeout = 120

  ## In case you need to specify explicitly SSH credentials...
  #config.ssh.username = "ubuntu"
  #config.ssh.password = gconfig['vm_password']
   
  # Shared folder
  # Unfortunately, VirtualBox only allows to share absolute paths, which cannot
  # work across all host OS.
  # https://www.virtualbox.org/ticket/15305
  # config.vm.synced_folder ".", gconfig['vm_shared_folder'], owner: gconfig['vm_user']
  
  # Disable the default shared folder of vagrant
  config.vm.synced_folder ".", "/vagrant", disabled: true

  # provisioner: set up VM via ansible. To (re-)run this step:
  #   vagrant provision --provision-with ansible
  # Note we use a static inventory, see: https://www.vagrantup.com/docs/provisioning/ansible_intro#static-inventory
  config.vm.network :private_network, ip: gconfig["ansible_host"]
  config.vm.provision "ansible" do |ansible|
    ansible.inventory_path = "inventory.yml"
    ansible.limit = "vagrant-provision"
    ansible.playbook = "playbook-build.yml"
    # ansible.verbose = "v"
    ansible.extra_vars = {
      build_hosts: "vagrant-provision",
    }
    ansible.raw_arguments = Shellwords.shellsplit(ENV['ANSIBLE_ARGS']) if ENV['ANSIBLE_ARGS']
    # Ensure that public key auth is not disabled by the user's config
    ansible.raw_ssh_args = ['-o PubKeyAuthentication=yes -o DSAAuthentication=yes']
  end
end
