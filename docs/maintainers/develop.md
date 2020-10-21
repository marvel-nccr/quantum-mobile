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

Pushing a commit to master or releasing a tag on GitHub will trigger a full build test on GH Actions.

To trigger this build test when working on a PR, you can create a tag locally (on the PR branch), then push it to GitHub:

```bash
git tag -a my-tag -m "Comment about tag"
git push --follow-tags
```
