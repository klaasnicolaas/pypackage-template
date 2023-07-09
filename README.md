# Python Package Template

<!-- PROJECT SHIELDS -->
[![License][license-shield]](LICENSE)
[![GitHub Release][releases-shield]][releases]

This project has been set up to quickly and easily set up a new Python package project instead of copying and modifying files from previous projects every time. For this we use [Copier][copier], which will configure your project based on a questionnaire.

## Feature Summary

* [GitHub Actions][gh-actions] for continuous integration and publishing to PyPI
* [Poetry][poetry] for dependency management and packaging
* [Thrusted publishers][thrusted] for PyPI releases
* [Dev Containers][devcontainer] for easy development in VS Code
* [Renovate Bot][renovate] for dependency updates
* [Black][black] for code formatting
* [mypy][mypy] for static type checking
* [pytest][pytest] for testing with code coverage
* [Ruff][ruff] for linting
* And much more!

## Create a new project

_Assuming you have already [correctly installed](https://copier.readthedocs.io/en/stable/#installation) Copier._

Choose where you would like to create your new project, run the following and answer the questions.

```shell
copier gh:klaasnicolaas/pypackage-template path/to/destination
```

## Publishing to PyPI

A [GitHub workflow](template/.github/workflows/release.yaml.j2) is included that will automatically publish the packaged work to [PyPI](https://pypi.org/) when a new release is created. To support this, there are some things you need to set up first.

- Create and verify an account on [PyPI](https://pypi.org/account/register/).
- Add a [Trusted Publisher](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) to your PyPI account.
- Create an Environments in the GitHub repository settings. Name it "`release`", choose **selected branches** and add a deployment branch rule for `main` and `v*`.

Now, when you [create a new release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) from your repository, a workflow will run and deploy the code to PyPI.

## Unit test coverage

With every commit push to a pull request, a [GitHub workflow](template/.github/workflows/tests.yaml) will automatically run unit tests and output code coverage into an xml file. To easily see if code coverage is changing as a result of new work, you should install the GitHub app: **Codecov**.

- Go to the Codecov app page - https://github.com/apps/codecov
- Click **Configure**
- Select your repository and follow the instructions

Future pull requests and commits will now include code coverage information.

## Renovate Bot

Renovate checks if updates are available for dependencies and will update them automatically via a pull request. If your repository is set up correctly for [auto-merging](https://docs.renovatebot.com/key-concepts/automerge/), the pull request will also be merged automatically.

- Go to the Renovate Bot app page - https://github.com/apps/renovate
- Click **Configure**
- Select your repository and follow the instructions

After this Renovate will create a GitHub issue in your repository which serves as a dashboard, you can see here which updates are pending and trigger Renovate to check again.

## Automatic Release Drafts

Automatically generate release notes with the [Release Drafter](https://github.com/release-drafter/release-drafter) workflow. This uses the labels from issues and pull requests to draft pretty and detailed release notes for your GitHub releases.

## Start developing on this template

The project uses [Poetry][poetry] for dependencies management and packaging. Make sure you have it installed in your development machine. To install the development dependencies in a virtual environment, type:

```shell
poetry install
```

This will also generate a `poetry.lock` file, you should track this file in version control. Check out the [Poetry][poetry] documentation for more information on the available commands.

## Pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) to run some checks before committing code. To install the pre-commit hooks, run the following command in the poetry environment:

```shell
pre-commit install
```

## Test changes on copier

If you would like to test locally with copier to see what the output is, you can use the command below. So that you can be sure that it takes all changes into account.

```bash
copier -r HEAD ./ path/to/destination
```

## License

Distributed under the **MIT** License. See [`LICENSE`](LICENSE) for more information.

<!-- Links -->
[black]: https://black.readthedocs.io/en/stable/
[copier]: https://copier.readthedocs.io/en/stable/
[gh-actions]: https://github.com/features/actions
[mypy]: https://mypy.readthedocs.io/en/stable/
[poetry]: https://python-poetry.org/
[pytest]: https://docs.pytest.org/en/latest/
[ruff]: https://beta.ruff.rs/docs/
[thrusted]: https://docs.pypi.org/trusted-publishers/using-a-publisher/
[renovate]: https://docs.renovatebot.com/
[devcontainer]: https://code.visualstudio.com/docs/remote/containers

<!-- Shields -->
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/pypackage-template.svg
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/pypackage-template.svg
[releases]: https://github.com/klaasnicolaas/pypackage-template/releases
