#!/bin/bash
cat <<EOF | {{ aiida_venv}}/bin/verdi code setup 
{{ aiida_qe_code_name}}
pw.x from Quantum ESPRESSO compiled (version {{ aiida_qe_code_name }})
False
quantumespresso.pw
{{ aiida_computer_name }}
{{ qe_topdir }}/bin/pw.x


EOF


