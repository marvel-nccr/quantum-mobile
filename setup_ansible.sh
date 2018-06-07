#!/bin/bash
set -e

echo "### Parsing globalconfig.yml"
source other_stuff/yaml_parser.sh
eval $(parse_yaml globalconfig.yml)

# set up ssh config for ansible
vagrant ssh-config > vagrant-ssh
#sed -i"" "s/User vagrant/User ${vm_user}/g" vagrant-ssh
echo "### SSH config written to 'vagrant-ssh'"
echo "### Use e.g.: ssh -F vagrant-ssh default'"

# set up inventory file for ansible
cat > hosts <<EOF
[vms:vars]
ansible_ssh_common_args= -F vagrant-ssh
[vms]
default ansible_user=vagrant
EOF
