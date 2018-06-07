Ansible Role: Default Web Browser
=================================

[![Build Status](https://travis-ci.org/gantsign/ansible-role-default-web-browser.svg?branch=master)](https://travis-ci.org/gantsign/ansible-role-default-web-browser)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.default--web--browser-blue.svg)](https://galaxy.ansible.com/gantsign/default-web-browser)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-default-web-browser/master/LICENSE)

This role sets the default web browser for Ubuntu Unity and Xfce4.

Requirements
------------

* Ansible

    * Minimum 2.3

* Ubuntu

    * Xenial (16.04)

* Supported desktop

    * Ubuntu Unity (i.e. the default desktop on Ubuntu)

        Note: other Gnome based desktops may work but have not been tested.

    * Xfce4 (i.e. the desktop on XUbuntu)

* Installed web browser

    * This role doesn't install the web browser; you need to have already
      installed your chosen web browser before using this role.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# The web browser to make the default (i.e. the name of the .desktop file without the extension)
default_web_browser: google-chrome
```

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
    - role: gantsign.default-web-browser
      default_web_browser: google-chrome
```

More Roles From GantSign
------------------------

You can find more roles from GantSign on
[Ansible Galaxy](https://galaxy.ansible.com/gantsign).

Development & Testing
---------------------

This project uses [Molecule](http://molecule.readthedocs.io/) to aid in the
development and testing; the role is unit tested using
[Testinfra](http://testinfra.readthedocs.io/) and
[pytest](http://docs.pytest.org/).

To develop or test you'll need to have installed the following:

* Linux (e.g. [Ubuntu](http://www.ubuntu.com/))
* [Docker](https://www.docker.com/)
* [Python](https://www.python.org/) (including python-pip)
* [Ansible](https://www.ansible.com/)
* [Molecule](http://molecule.readthedocs.io/)

To run the role (i.e. the `tests/test.yml` playbook), and test the results
(`tests/test_role.py`), execute the following command from the project root
(i.e. the directory with `molecule.yml` in it):

```bash
molecule test
```

License
-------

MIT

Author Information
------------------

John Freeman

GantSign Ltd.
Company No. 06109112 (registered in England)
