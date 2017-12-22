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

vm_id="$vm_name $vm_version"

echo "### Exporting '$vm_id'"
git_tag=`git describe --abbrev=0`
if [ "$git_tag" != "$vm_version" ]; then
    echo "latest git tag $git_tag and version number $vm_version do not agree"
    exit
fi

fname=quantum_mobile_${vm_version}.ova
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

echo "### Computing size of vm image and vm disk"
vm_image_size=`du -sh $fname  | awk '{print $1}'`
vdisk_path_grep=`vboxmanage showvminfo --machinereadable "$vm_id" | grep vmdk `
[[ $vdisk_path_grep =~ ^.*=\"(.*)\"$ ]]
vdisk_path=${BASH_REMATCH[1]}
vm_vdisk_size=`du -sh "$vdisk_path" | awk '{print $1}' `

export fname vm_version vm_user vm_password 
export vm_image_size vm_vdisk_size
envsubst < INSTALL.md > INSTALL_${vm_version}.txt
echo "### Instructions in INSTALL_${vm_version}${rc}.txt"
