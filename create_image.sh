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

echo "### Halting any running machines"
vagrant halt # shut down machine

#vboxmanage list vms

echo "### Exporting '$vm_name $vm_version'"

rc=-rc0
vm_version=${vm_version}${rc}
fname=marvel_vm_${vm_version}.ova

[ -e $fname ] && rm $fname

vboxmanage export "${vm_name} ${vm_version}"  \
  -o $fname \
  --vsys 0 \
  --product "$vm_name" \
  --version "$vm_version" \
  --producturl "https://github.com/marvel-nccr/marvel-virtualmachine" \
  --vendor "$author" \
  --vendorurl "$author_url" \
  --description "$vm_description"
  --eulafile 
echo "### Find image in $fname"

export fname vm_version vm_user vm_password
envsubst < INSTALL.md > INSTALL_${vm_version}.txt
echo "### Instructions in INSTALL_${vm_version}.txt"
