# Creating an ansible role

Please use the [ansible role cookiecutter](https://github.com/marvel-nccr/cookiecutter-ansible-role) to template a new role.

:::{note}
If you are developing new ansible roles for computational materials science applications and would like to make them easier to find, we'd be happy to host them under the marvel-nccr github organisation - just [drop us a line](mailto:developers@materialscloud.org).
:::

## Testing a role

### Locally

The simplest way to test a role is to:

Clone its repository into your `roles` folder, e.g.

```bash
git clone https://github.com/marvel-nccr/ansible-role-simulationbase.git roles/marvel-nccr.simulationbase
```

Add your role to the `playbook.yml` file with a *tag*:

```yaml
- role: marvel-nccr.simulationbase
  tags: [simulationbase]
  vars:
    simulationbase_vm_user: "{{ vm_user }}"
    simulationbase_vm_user_public_key: "{{ lookup('file', './keys/aiida_tutorial_aiidaaccount.pub') }}"
    simulationbase_hostname: "{{ vm_hostname }}"
    simulationbase_codes_folder: "{{ vm_codes_folder }}"
```

Run the role on your existing VM (e.g. Quantum Mobile):

```bash
ansible-playbook.yml --tags simulationbase
```

### Continuous Integration

Both [existing marvel-nccr roles on ansible galaxy](https://galaxy.ansible.com/marvel-nccr) and those templated via the cookiecutter come with a few tools to help you test the roles individually.
In the git repository of the role:

* use the pre-commit hooks to `lint` your yaml files:

  ```bash
  pip install -r requirements.txt
  pre-commit install
  ```

  From now on, lints on every commit.

* install [Docker](https://www.docker.com/products/docker-desktop) and use `molecule` for a full test of your role:

  ```bash
  pip install -r requirements.txt
  molecule tests
  ```

  This will first run the linters and then run your role on a docker container (which is thrown away after the test).
  It actually runs your role twice to make sure it's idempotent.
