#!/usr/bin/env python
# This script is designed to update the tutorial database after the
# old export file tutorial_perovskites.aiida has been imported.
# IMPORTANT: This script is idempotent and has to remain idempotent
import os
import sys
from aiida.backends.djsite.db import models
from aiida.common.exceptions import NotExistent
from aiida.orm import Code, DataFactory, Group, Calculation
from aiida.orm.backend import construct_backend
from aiida.orm.data.upf import UPFGROUP_TYPE

backend = construct_backend()
user = backend.users.get_automatic_user()
changed = False

# Recreate the pseudo potential groups
for typestring in ['pbe', 'pbesol', 'lda']:

    q1 = models.DbAttribute.objects.filter(key='filename',
         tval__endswith='.UPF', tval__contains='_{}_'.format(typestring))
    q = models.DbNode.objects.filter(
        type__startswith=DataFactory('upf')._query_type_string,
        dbattributes__in=q1)

    group_name = 'GBRV_{}'.format(typestring)
    group, created = Group.get_or_create(name=group_name, type_string=UPFGROUP_TYPE, user=user) 
    node_count = len(group.nodes)
    group.add_nodes([c for c in q])

    if created or len(group.nodes) != node_count:
        changed = True

# Reset the user name and the extras for the tutorial groups
for group_name in ['tutorial_pbesol', 'tutorial_pbe', 'tutorial_lda']:
    group = Group.get(name=group_name)
    old_user = group.dbgroup.user
    group.dbgroup.user = models.DbUser.objects.get(email=user.email)
    group.dbgroup.save()

    if old_user.email != user.email:
        changed = True

    count = 0
    for n in group.nodes:
        if 'A' not in n.get_extras().keys():
            changed = True
        if 'B' not in n.get_extras().keys():
            changed = True
        A = n.inp.structure.sites[1].kind_name
        B = n.inp.structure.sites[1].kind_name
        n.set_extra('A', A)
        n.set_extra('B', B)
        count += 1

if changed:
    print "State changed"
else:
    print "Nothing changed"
