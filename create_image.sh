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

vm_id='$vm_name $vm_version'

echo "### Exporting '$vm_id'"
vm_release=`git describe --abbrev=0`
if [ "$vm_release" != "$vm_version" ]; then
    echo "latest git tag $vm_release and version number $vm_version do not agree"
fi

fname=quantum_mobile_${vm_release}.ova
[ -e $fname ] && rm $fname

vboxmanage export "$vm_id"  \
  -o $fname \
  --vsys 0 \
  --product "$vm_name" \
  --version "$vm_version" \
  --producturl "https://github.com/marvel-nccr/marvel-virtualmachine" \
  --vendor "$author" \
  --vendorurl "$author_url" \
  --description "$vm_description" \
  --eulafile "EULA.txt"
echo "### Find image in $fname"

echo "### Computing disk and vm size"
image_size=`du -sh $fname  | awk '{print $1}'`
vdisk_path_set=`vboxmanage showvminfo --machinereadable "$vm_id" | grep vmdk `
tmp=(${vdisk_path_set//=/ })
vdisk_path=${tmp[2]}


export fname vm_version vm_user vm_password
envsubst < INSTALL.md > INSTALL_${vm_release}.txt
echo "### Instructions in INSTALL_${vm_version}${rc}.txt"
