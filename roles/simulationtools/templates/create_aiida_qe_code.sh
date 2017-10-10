#!/bin/bash
cat <<EOF | {{ aiida_venv }}/bin/verdi code setup 
{{ aiida_qe_code_name }}
{{ qe_exec_name }}.x from Quantum ESPRESSO {{ qe_version }} compiled
False
quantumespresso.{{ qe_exec_name }}
{{ aiida_computer_name }}
{{ qe_topdir }}/bin/{{ qe_exec_name }}.x


EOF


