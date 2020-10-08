#!/bin/bash
key=private_key
ssh-keygen -t rsa -N "" -f $key
cp $key .vagrant/machines/default/virtualbox/

echo "###################################"
echo "Use VirtualBox GUI to paste the following lines in ~vagrant/.ssh/authorized_keys"
cat ${key}.pub
rm ${key} ${key}.pub
