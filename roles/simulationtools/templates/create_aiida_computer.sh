#!/bin/bash

set -e

cat <<EOF | {{ aiida_venv }}/bin/verdi computer setup 
{{ aiida_computer_name }}
localhost

True
local
torque
{{aiida_run_folder}}
mpirun -np {tot_num_mpiprocs}
2


EOF

# I now configure the computer: it uses a local transport, no inputs asked
{{ aiida_venv }}/bin/verdi computer configure {{ aiida_computer_name }}


