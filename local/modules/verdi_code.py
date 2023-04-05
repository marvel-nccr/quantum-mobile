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
        description: The label of the code
        required: true
    computer:
        description: The computer name
        required: true
    remote_abs_path:
        description: The absolute path to the executable
        required: true
    input_plugin:
        description: The input plugin
        required: true
    description:
        description: The description
        required: false
    prepend_text:
        description: The prepend text
        required: false
    append_text:
        description: The append text
        required: false
    run_test:
        description: Whether to run verdi code test after creating the code (default: true)
        required: false
"""

EXAMPLES = """
- name: Show information about installed packages
  verdi_code:
    verdi: /path/to/verdi
    profile: default
    label: code_name
    computer: localhost
    remote_abs_path: /path/to/code
    input_plugin: quantum_espresso.pw
    description: "Code description"
    prepend_text: 'commands'
    append_text: 'commands'
"""

from ansible.module_utils.basic import AnsibleModule


def _main():
    """Module entrypoint."""
    module = AnsibleModule(
        argument_spec={
            "verdi": {"required": True, "type": "str"},
            "profile": {"required": True, "type": "str"},
            "label": {"required": True, "type": "str"},
            "computer": {"required": True, "type": "str"},
            "remote_abs_path": {"required": True, "type": "path"},
            "input_plugin": {"required": True, "type": "str"},
            "description": {"required": False, "type": "str"},
            "prepend_text": {"required": False, "type": "str"},
            "append_text": {"required": False, "type": "str"},
            "run_test": {"required": False, "type": "bool", "default": True},
        },
    )
    verdi = module.params["verdi"].split() + ["--profile", module.params["profile"]]
    # test if code is already there
    label = module.params["label"]
    computer = module.params["computer"]
    rc, _, _ = module.run_command(verdi + ["code", "show", f"{label}@{computer}"])
    if rc == 0:
        module.exit_json(changed=False)

    # otherwise create
    command = verdi + ["code", "setup", "--non-interactive"]

    for option, key in [
        ("--label", "label"),
        ("--computer", "computer"),
        ("--remote-abs-path", "remote_abs_path"),
        ("--input-plugin", "input_plugin"),
        ("--description", "description"),
        ("--prepend-text", "prepend_text"),
        ("--append-text", "append_text"),
    ]:
        if key in module.params and module.params[key]:
            command.extend([option, module.params[key]])

    _, stdout, _ = module.run_command(command, check_rc=True)

    if "run_test" in module.params and not module.params["run_test"]:
        # if not running test, then just exit
        module.exit_json(changed=True, stdout=stdout)

    # test the code actually works, e.g. that the executable exists
    # otherwise delete
    test_rc, test_stdout, test_stderr = module.run_command(
        verdi + ["code", "test", module.params["label"]]
    )
    if test_rc != 0:
        module.run_command(
            verdi + ["code", "delete", "--force", module.params["label"]]
        )
        module.fail_json(
            msg="verdi code test failed",
            rc=test_rc,
            stdout=test_stdout,
            stderr=test_stderr,
        )

    module.exit_json(changed=True, stdout=stdout)


if __name__ == "__main__":
    _main()
