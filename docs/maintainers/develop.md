# Developing Quantum Mobile

## Code style

Code style is tested using pre-commit:

```bash
pip install pre-commit
pre-commit run --all
```

## Updating the documentation

```bash
pip install tox
# to build from scratch
tox -e docs-clean
# to update the build (faster, doesn't remove existing build)
tox -e docs-update
# to start a live server (reloads automatically on changes to documentation)
tox -e docs-live
```

## Testing a build on GH Actions

Pushing a commit to main or a PR on GitHub will trigger a pre-commit test and a Docker-based build test on GitHub Actions.
The build test runs Ansible provisioning in Docker containers on both ARM64 (`ubuntu-24.04-arm`) and AMD64 (`ubuntu-latest`) architectures.

You can also trigger a full build test of either the vagrant or docker builds, by pushing a git tag prefixed `vagrant-` or `docker-`.

To trigger this build test when working on a PR, you can create a tag locally (on the PR branch), then push it to GitHub:

```bash
git tag -a vagrant-test1 -m "Test the full vagrant build"
git tag -a docker-test1 -m "Test the full Docker build"
git push --follow-tags
```

The docker build will also push the final image to <https://hub.docker.com/r/marvelnccr/quantum-mobile>, under the tag `develop`.
