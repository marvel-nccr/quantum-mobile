Vagrant.require_version ">= 1.7.0"

## Read global configuration file from YAML
require 'yaml'
current_dir    = File.dirname(File.expand_path(__FILE__))
configs        = YAML.load_file("#{current_dir}/globalconfig.yml")
version = configs['vm_version']
name = configs['vm_name']

Vagrant.configure(2) do |config|

  ## VIRTUALBOX provider
  config.vm.provider "virtualbox" do |vb|

     ## Machine name inside VirtualBox
     vb.name = "#{name} #{version}"

     ## Resource details
     vb.memory = 1024
     vb.cpus = 2

     ## To allow to graphically connect to it from the VirtualBox interface
     ## (called 'show in the VirtualBox GUI')
     vb.gui = true
   end

  ## To automatically update/upgrade the Guest Additions at every 
  ## login. Note this requires 'vagrant plugin install vbguest'
  ##
  ## Uncomment the following if you don't want to check/update the
  ## Guest Additions at every reboot, but just once
  #config.vbguest.auto_update = false
  ## Uncomment to avoid remote downloads of ISO
  #config.vbguest.no_remote = true

  ## Starting Box
  config.vm.box = "ubuntu/xenial64"

  ## In case you need to specify explicitly SSH credentials...
  #config.ssh.username = "ubuntu"
  #config.ssh.password = "xyz"

  ## First provisioner: python needed to have ansible work
  ## as a second provisioner
  config.vm.provision "bootstrap", type: "shell" do |s|
    s.inline = "apt-get update && apt-get install -y python2.7 python3"
  end

  ## Second provisioner: ansible script that actually sets up
  ## the hole machine. To (re)run only this, run
  ##   vagrant provision --provision-with ansible
  ##
  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.extra_vars = {
       ansible_python_interpreter: "/usr/bin/python2.7"
    }
    ansible.playbook = "playbook.yml"
  end
end
