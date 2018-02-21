#!/bin/bash
set -e

echo "### WARNING - THIS HAS ONLY BEEN TESTED ONCE"

echo "### Parsing globalconfig.yml"
source other_stuff/yaml_parser.sh
eval $(parse_yaml globalconfig.yml)

vm_id="$vm_name $vm_version"

echo "### Getting size and uuid of vdisk"
vdisk_path_grep=`vboxmanage showvminfo --machinereadable "$vm_id" | grep "SATA Controller-0-0"`
[[ $vdisk_path_grep =~ ^.*=\"(.*)\"$ ]]
vdisk_path=${BASH_REMATCH[1]}

vdisk_uuid_grep=`vboxmanage showvminfo --machinereadable "$vm_id" | grep "SATA Controller-ImageUUID-0-0"`
[[ $vdisk_uuid_grep =~ ^.*=\"(.*)\"$ ]]
vdisk_uuid=${BASH_REMATCH[1]}

vm_vdisk_size=`du -sh "$vdisk_path" | awk '{print $1}' `
echo "### Initial vdisk size: $vm_vdisk_size"

#echo "### Filling free space with zeros (this can take several minutes)"
#ssh -F vagrant-ssh default "cat /dev/zero > zero.fill; sync; sleep 1; sync; rm -f zero.fill"
#
#echo "### Halting any running machines"
#vagrant halt
 
echo "### Converting vdisk to vdi format"
tmp_vdisk_vdi=tmp.vdi
rm -f $tmp_vdisk_vdi
vboxmanage clonehd "$vdisk_path" $tmp_vdisk_vdi --format vdi

echo "### Compacting vdisk"
vboxmanage modifyhd $tmp_vdisk_vdi --compact

echo "### Converting vdisk back to vmdk"
tmp_vdisk_vmdk=tmp.vmdk
rm -f $tmp_vdisk_vmdk
vboxmanage clonehd $tmp_vdisk_vdi $tmp_vdisk_vmdk --format vmdk
vboxmanage closemedium $tmp_vdisk_vdi --delete

echo "### Re-connecting vdisk to VM"
cp $tmp_vdisk_vmdk "$vdisk_path"
vboxmanage closemedium $tmp_vdisk_vmdk --delete
vboxmanage internalcommands sethduuid "$vdisk_path" $vdisk_uuid

vm_vdisk_size=`du -sh "$vdisk_path" | awk '{print $1}' `
echo "### Final vdisk size: $vm_vdisk_size"
