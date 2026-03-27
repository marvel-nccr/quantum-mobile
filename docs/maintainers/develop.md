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

## Supported codes

Below is a list of codes we aim to support in Quantum Mobile, with some useful links/details.
Architecture support refers to `linux-aarch64` (ARM64) availability on conda-forge (as of March 2026).

| Code | Releases | Conda-forge | aarch64 |
|------|----------|-------------|---------|
| [ABINIT](https://www.abinit.org/) | [GitHub](https://github.com/abinit/abinit/releases) | [abinit](https://anaconda.org/conda-forge/abinit) / [feedstock](https://github.com/conda-forge/abinit-feedstock) | ❌ |
| [BigDFT](https://bigdft.org/) | [GitLab](https://gitlab.com/l_sim/bigdft-suite/-/releases) | [bigdft-suite](https://anaconda.org/conda-forge/bigdft-suite) / [feedstock](https://github.com/conda-forge/bigdft-suite-feedstock) | ❌ |
| [CP2K](https://www.cp2k.org/) | [GitHub](https://github.com/cp2k/cp2k/releases) | [cp2k](https://anaconda.org/conda-forge/cp2k) / [feedstock](https://github.com/conda-forge/cp2k-feedstock) | ❌ |
| [Fleur](https://www.flapw.de/) | [GitHub](https://github.com/judftteam/fleur/releases) | [fleur](https://anaconda.org/conda-forge/fleur) / [feedstock](https://github.com/conda-forge/fleur-feedstock) | ❌ |
| [NWChem](https://nwchemgit.github.io/) | [GitHub](https://github.com/nwchemgit/nwchem/releases) | [nwchem](https://anaconda.org/conda-forge/nwchem) / [feedstock](https://github.com/conda-forge/nwchem-feedstock) | ✅ |
| [Quantum ESPRESSO](https://www.quantum-espresso.org/) | [GitLab](https://gitlab.com/QEF/q-e/-/releases) | [qe](https://anaconda.org/conda-forge/qe) / [feedstock](https://github.com/conda-forge/qe-feedstock) | ✅ |
| [Siesta](https://siesta-project.org/) | [GitLab](https://gitlab.com/siesta-project/siesta/-/releases) | [siesta](https://anaconda.org/conda-forge/siesta) / [feedstock](https://github.com/conda-forge/siesta-feedstock) | ✅ |
| [Wannier90](http://www.wannier.org/) | [GitHub](https://github.com/wannier-developers/wannier90/releases) | [wannier90](https://anaconda.org/conda-forge/wannier90) / [feedstock](https://github.com/conda-forge/wannier90-feedstock) | ✅ |
| [Yambo](http://www.yambo-code.eu/) | [GitHub](https://github.com/yambo-code/yambo/releases) | [yambo](https://anaconda.org/conda-forge/yambo) / [feedstock](https://github.com/conda-forge/yambo-feedstock) | ✅ |
