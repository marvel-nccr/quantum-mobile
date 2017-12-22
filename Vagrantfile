Vagrant.require_version ">= 1.7.0"

## Read global configuration file from YAML
require 'yaml'
current_dir    = File.dirname(File.expand_path(__FILE__))
gconfig        = YAML.load_file("#{current_dir}/globalconfig.yml")

Vagrant.configure(2) do |config|

  ## VIRTUALBOX provider
  config.vm.provider "virtualbox" do |vb|

     ## Machine name inside VirtualBox
     vb.name = gconfig['vm_name'] + ' ' + gconfig['vm_version']

     ## Resource details
     vb.memory = gconfig['vm_memory']
     vb.cpus = gconfig['vm_cpus']

     ## To allow to graphically connect to it from the VirtualBox interface
     ## (called 'show in the VirtualBox GUI')
     vb.gui = true

     # More customizations
     # See https://www.virtualbox.org/manual/ch08.html
     vb.customize ["modifyvm", :id, "--vram", gconfig['vm_vram']]
     # makes mouse/typing more responsive
     vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
     vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
     # turn off remote display (requires Virtualbox Extension pack)
     vb.customize ["modifyvm", :id, "--vrde", "off"]

     # prevent VM time slipping out of sync by more than 10s (default: 20 min)
     vb.customize [ "guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 10000 ]
   end

  # Vagrant automatically updates/upgrades the Guest Additions at every 
  # login (this requires 'vagrant plugin install vbguest')
  # Uncomment the following if you don't want to check/update the
  # Guest Additions at every reboot, but just once
  #config.vbguest.auto_update = false
   
  # Uncomment to avoid remote downloads of ISO
  #config.vbguest.no_remote = true

  config.vm.box = "bento/ubuntu-16.04"
  #config.vm.box = "ubuntu/xenial64"
  config.vm.boot_timeout = 60

  ## In case you need to specify explicitly SSH credentials...
  #config.ssh.username = "ubuntu"
  #config.ssh.password = gconfig['vm_password']
   
  # Shared folder
  # Unfortunately, VirtualBox only allows to share absolute paths, which cannot
  # work across all host OS. Until this changes, let's add the shared folder
  # https://www.virtualbox.org/ticket/15305
  #config.vm.synced_folder ".", gconfig['vm_shared_folder'], owner: gconfig['vm_user']
  
  # Disable the default shared folder of vagrant
  config.vm.synced_folder ".", "/vagrant", disabled: true

  # provisioner: python needed to have ansible work as a second provisioner
  config.vm.provision "bootstrap", type: "shell" do |s|
    s.inline = "apt-get update && apt-get install -y python2.7 python3"
  end

  # provisioner: add custom user for ansible
  user = gconfig['vm_user']
  password = gconfig['vm_password']
  commands = <<-EOF
if [ ! -d /home/#{user} ] ; then
  useradd -m -s /bin/bash --groups sudo,adm #{user} && \
  cp -pr /home/vagrant/.ssh /home/#{user}/ && \
  chown -R #{user}:#{user} /home/#{user} \
#  echo #{user}:#{password} | chpasswd 
fi
EOF
  config.vm.provision "adduser", type: "shell" do |s|
    s.inline = commands
  end

  # provisioner: set up VM via ansible. To (re-)run this step:
  #   vagrant provision --provision-with ansible
  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.extra_vars = {
       ansible_python_interpreter: "/usr/bin/python2.7",
       ansible_user: user
    }
    ansible.playbook = "playbook.yml"
  end
end
