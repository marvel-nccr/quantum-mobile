#!/bin/bash
set -e

( echo "" | envsubst ) || (echo "envsubst not found, install it first - it is part of gettext, so you can e.g. du 'brew install gettext' and read information in the output to finalize the installation" ; exit 1)

echo "### Parsing globalconfig.yml"
source other_stuff/yaml_parser.sh
eval $(parse_yaml globalconfig.yml)

echo "### Halting any running machines"
vagrant halt # shut down machine
#vboxmanage list vms

vm_id="$vm_name $vm_version"
new_vm_id="Quantum Mobile AiiDA tutorial May 2018"
vboxmanage modifyvm "$vm_id" --name "$new_vm_id"

echo "### Exporting '$new_vm_id'"

fname=quantum_mobile_aiida_tutorial_May_2018.ova
[ -e $fname ] && rm $fname

vboxmanage export "$new_vm_id"  \
  -o $fname \
  --vsys 0 \
  --product "Quantum Mobile AiiDA tutorial" \
  --version "May 2018" \
  --producturl "https://github.com/marvel-nccr/quantum-mobile" \
  --vendor "$vm_author" \
  --vendorurl "$vm_author_url" \
  --description "$vm_description" \
  --eulafile "EULA.txt"
echo "### Find image in $fname"

echo "### Computing size of vm image and vm disk"
vm_image_size=`du -sh $fname  | awk '{print $1}'`
vm_image_md5=`md5 $fname  | awk '{print $4}'`
vdisk_path_grep=`vboxmanage showvminfo --machinereadable "$new_vm_id" | grep vmdk `
[[ $vdisk_path_grep =~ ^.*=\"(.*)\"$ ]]
vdisk_path=${BASH_REMATCH[1]}
vm_vdisk_size=`du -sh "$vdisk_path" | awk '{print $1}' `

export fname vm_version vm_user vm_password 
export vm_image_size vm_image_md5 vm_vdisk_size
envsubst < INSTALL.md > INSTALL_${vm_version}.txt
echo "### Instructions in INSTALL_${vm_version}${rc}.txt"
