#!/usr/bin/python
# -*- coding: utf-8 -*-
DOCUMENTATION = """
module: verdi_code
short_description: Add a code to AiiDA
description: Add a code to AiiDA
author:
  - Chris Sewell (@chrisjsewell)
options:
    verdi:
        description: The verdi command
        required: true
    profile:
        description: The AiiDA profile
        required: true
    label:
        description: The label of the computer
        required: true
    work_dir:
        description: The working directory for the computer
        required: true
        type: path
    transport:
        description: The transport plugin name
        required: true
    scheduler:
        description: The scheduler plugin name
        required: true
    hostname:
        description: The fully qualified hostname of the computer
        required: false
    description:
        description: The description
        required: false
    mpirun_command:
        description: The mpirun command
        required: false
    mpiprocs_per_machine:
        description: The default number of MPI processes that should be executed per machine (node)
        required: false
    configure:
        description: The list of configuration options
        required: false
        type: list
        elements: str
"""

EXAMPLES = """
- name: Show information about installed packages
  verdi_code:
    verdi: /path/to/verdi
    profile: default
    label: computer_name
    work_dir: /path/to/workdir
    transport: local
    scheduler: direct
    hostname: localhost
    mpirun_command: mpirun
    mpiprocs_per_machine: 1
    configure:
    - --safe-interval=5
"""

from ansible.module_utils.basic import AnsibleModule


def _main():
    """Module entrypoint."""
    module = AnsibleModule(
        argument_spec={
            "verdi": {"required": True, "type": "str"},
            "profile": {"required": True, "type": "str"},
            "label": {"required": True, "type": "str"},
            "work_dir": {"required": True, "type": "path"},
            "transport": {"required": True, "type": "str"},
            "scheduler": {"required": True, "type": "str"},
            "hostname": {"required": True, "type": "str"},
            "description": {"required": False, "type": "str"},
            "mpirun_command": {"required": False, "type": "str"},
            "mpiprocs_per_machine": {"required": False, "type": "int"},
            "configure": {"required": False, "type": "list", "elements": "str"},
        },
    )
    verdi = module.params["verdi"].split() + ["--profile", module.params["profile"]]
    # test if computer is already there
    label = module.params["label"]
    rc, _, _ = module.run_command(verdi + ["computer", "show", label])
    if rc == 0:
        # TODO ensure computers are configured
        module.exit_json(changed=False)

    # otherwise create
    command = verdi + ["computer", "setup", "--non-interactive"]

    for option, key in [
        ("--label", "label"),
        ("--work-dir", "work_dir"),
        ("--transport", "transport"),
        ("--scheduler", "scheduler"),
        ("--hostname", "hostname"),
        ("--mpirun-command", "mpirun_command"),
        ("--mpiprocs-per-machine", "mpiprocs_per_machine"),
    ]:
        if key in module.params and module.params[key]:
            command.extend([option, str(module.params[key])])

    _, setup_stdout, _ = module.run_command(command, check_rc=True)

    # configure
    command = (
        verdi
        + [
            "computer",
            "configure",
            module.params["transport"],
            "--non-interactive",
            label,
        ]
        + (module.params["configure"] or [])
    )
    _, config_stdout, _ = module.run_command(command, check_rc=True)

    module.exit_json(changed=True, setup=setup_stdout, config=config_stdout)


if __name__ == "__main__":
    _main()
