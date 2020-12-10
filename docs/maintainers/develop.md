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
# to start a live server (reloads automatically on changes to documentation)
tox -e docs-live
```

## Testing a build on GH Actions

Pushing a commit to master or a PR on GitHub will trigger a pre-commit and initial build (only for `init` tagged tasks) tests on GH Actions.

You can also trigger a full build test of either the vagrant or docker builds, by pushing a git tag prefixed `vagrant-` or `docker-`.

To trigger this build test when working on a PR, you can create a tag locally (on the PR branch), then push it to GitHub:

```bash
git tag -a vagrant-test1 -m "Test the full vagrant build"
git tag -a docker-test1 -m "Test the full Docker build"
git push --follow-tags
```

The docker build will also push the final image to <https://hub.docker.com/r/marvelnccr/quantum-mobile>, under the tag `develop`.
