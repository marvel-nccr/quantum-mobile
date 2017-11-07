#!/bin/bash

# Credits for yaml parser: 
# https://stackoverflow.com/a/21189044
function parse_yaml {
   local prefix=$2
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
   sed -ne "s|^\($s\):|\1|" \
        -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  $1 |
   awk -F$fs '{
      indent = length($1)/2;
      vname[indent] = $2;
      for (i in vname) {if (i > indent) {delete vname[i]}}
      if (length($3) > 0) {
         vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
         printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
      }
   }'
}

echo "### Parsing globalconfig.yml"
eval $(parse_yaml globalconfig.yml)

# set up ssh config for ansible
vagrant ssh-config > vagrant-ssh
sed -i "" "s/User vagrant/User ${vm_user}/g" vagrant-ssh

# set up inventory file for ansible
cat > hosts <<EOF
[vms]
default ansible_user=${vm_user}
EOF
