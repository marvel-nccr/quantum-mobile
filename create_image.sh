#!/bin/bash
set -e

( echo "" | envsubst ) || (echo "envsubst not found, install e.g. via 'brew install gettext' + read information in output to finalize installation" ; exit 1)

echo "### Parsing globalconfig.yml"
source other_stuff/yaml_parser.sh
eval $(parse_yaml globalconfig.yml)

echo "### Halting any running machines"
vagrant halt # shut down machine
#vboxmanage list vms

vm_id="$vm_name $vm_version"

echo "### Exporting '$vm_id'"
git_tag=`git describe --abbrev=0 --tags`
if [ "$git_tag" != "$vm_version" ]; then
    echo "latest git tag $git_tag and version number $vm_version do not agree"
#    exit
fi

fname=quantum_mobile_${vm_version}.ova
[ -e $fname ] && rm $fname

vboxmanage export "$vm_id"  \
  -o $fname \
  --vsys 0 \
  --product "$vm_name" \
  --version "$vm_version" \
  --producturl "https://github.com/marvel-nccr/marvel-virtualmachine" \
  --vendor "$vm_author" \
  --vendorurl "$vm_author_url" \
  --description "$vm_description" \
  --eulafile "EULA.txt"
echo "### Find image in $fname"

echo "### Computing size of vm image and vm disk"
vm_image_size=`du -sh $fname  | awk '{print $1}'`
vm_image_md5=`md5 $fname  | awk '{print $4}'`
vdisk_path_grep=`vboxmanage showvminfo --machinereadable "$vm_id" | grep vmdk `
[[ $vdisk_path_grep =~ ^.*=\"(.*)\"$ ]]
vdisk_path=${BASH_REMATCH[1]}
vm_vdisk_size=`du -sh "$vdisk_path" | awk '{print $1}' `
echo "### vdisk size: $vm_vdisk_size"
echo "### image size: $vm_image_size"

export fname vm_version vm_user vm_password 
export vm_image_size vm_image_md5 vm_vdisk_size
envsubst < INSTALL.md > INSTALL_${vm_version}.txt
echo "### Instructions in INSTALL_${vm_version}${rc}.txt"
