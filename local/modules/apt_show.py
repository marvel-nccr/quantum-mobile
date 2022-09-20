#!/usr/bin/python
# -*- coding: utf-8 -*-
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
module: apt_show
short_description: Show information about installed packages
description: Show information about installed packages
author:
  - Chris Sewell (@chrisjsewell)
options:
  name:
    description: Name of the package(s) to show
    required: true
"""

EXAMPLES = """
- name: Show information about installed packages
  apt_show:
    name: python3
  register: result
"""

RETURN = """
data:
    description: The dictionary of package information
    returned: always
    type: dict
"""


KEYS = {
    "Package": "name",
    "Version": "version",
    "Priority": "priority",
    "Section": "section",
    "Origin": "origin",
    "Maintainer": "maintainer",
    "Original-Maintainer": "maintainer_original",
    "Bugs": "bugs",
    "Installed-Size": "size_installed",
    "Depends": "depends",
    "Homepage": "homepage",
    "Supported": "supported",
    "Download-Size": "size_download",
    "APT-Manual-Installed": "installed",
    "APT-Sources": "sources",
    "Description": "description",
}


def _main():
    """Module entrypoint."""
    module = AnsibleModule(argument_spec={"name": {"required": True, "type": "str"}})
    if not module.params["name"]:
        module.fail_json(msg="Package name is empty")
    _, stdout, _ = module.run_command(["apt", "show"] + module.params["name"].split(), check_rc=True)
    data = {}
    lines = stdout.splitlines()
    index = 0
    while index < len(lines):
        if not lines[index].startswith("Package:"):
            index += 1
            continue
        package_data = {}
        while ":" in lines[index].strip():
            key, value = lines[index].split(":", 1)
            if key in KEYS:
                package_data[KEYS[key]] = value.strip()
            index += 1
        if package_data.get("installed") == "yes":
            data[package_data["name"]] = package_data

    module.exit_json(changed=False, data=data)


if __name__ == "__main__":
    _main()
