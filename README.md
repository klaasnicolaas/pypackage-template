# Python Package Template

<!-- PROJECT SHIELDS -->
[![License][license-shield]](LICENSE)
[![GitHub Release][releases-shield]][releases]

This project has been set up to quickly and easily set up a new Python package project instead of copying and modifying files from previous projects every time. For this we use [Copier][copier], which will configure your project based on a questionnaire.

## Feature Summary

* ♻️ [GitHub Actions][gh-actions] for continuous integration and publishing to PyPI
* 📦 [Poetry][poetry] for dependency management and packaging
* 🛡️ [Thrusted publishers][thrusted] for PyPI releases
* 🦋 Optional Bluesky posts for new releases
* 🐳 [Dev Containers][devcontainer] for easy development in VS Code
* ⬆️ [Renovate Bot][renovate] for dependency updates
* ✅ [ty][ty] for static type checking
* 🧪 [Pytest][pytest] for testing and code coverage
* ✍️ [Ruff][ruff] for linting and code formatting
* And much more!

## Create a new project

Ensure you have copier installed via [`pipx`](https://github.com/pypa/pipx):

```shell
pipx install copier
```

Decide where you want to create a new project, run the following command and answer all the questions:

```shell
copier copy --trust --data-file versions.json gh:klaasnicolaas/pypackage-template ~/path/to/destination
```

Or if you want to use the latest version from the main branch:

```shell
copier copy --trust --vcs-ref=HEAD --data-file versions.json gh:klaasnicolaas/pypackage-template ~/path/to/destination
```

Or clone the repository and run Copier directly:

```shell
uv sync
uv run copier copy --trust --vcs-ref=HEAD --data-file versions.json . ~/path/to/destination
```

## Publishing to PyPI

A [GitHub workflow](template/.github/workflows/release.yaml.j2) is included that will automatically publish the packaged work to [PyPI](https://pypi.org/) when a new release is created. To support this, there are some things you need to set up first.

- Create and verify an account on [PyPI](https://pypi.org/account/register/).
- Add a [Trusted Publisher](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) to your PyPI account.
- Create an Environment in the GitHub repository settings and name it "`release`".

When Bluesky release posting is enabled (the default), also add these secrets to the `release` environment:

- `BLUESKY_IDENTIFIER`: the Bluesky account identifier used for release posts.
- `BLUESKY_PASSWORD`: an app password for that Bluesky account.

Now, when you [create a new release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) from your repository, a workflow will publish the package to PyPI and, when enabled, post the release to Bluesky.

## Unit test coverage

With every commit push to a pull request, a [GitHub workflow](template/.github/workflows/tests.yaml) will automatically run unit tests and output code coverage into an xml file. To easily see if code coverage is changing as a result of new work, you should install the GitHub app: **Codecov**.

- Go to the Codecov app page - https://github.com/apps/codecov
- Click **Configure**
- Select your repository and follow the instructions
- Add the `CODECOV_TOKEN` secret to your repository secrets, you can find the token on the Codecov app page (required since v4.x).

Future pull requests and commits will now include code coverage information.

## Renovate Bot

Renovate checks if updates are available for dependencies and will update them automatically via a pull request. If your repository is set up correctly for [auto-merging](https://docs.renovatebot.com/key-concepts/automerge/), the pull request will also be merged automatically.

- Go to the Renovate Bot app page - https://github.com/apps/renovate
- Click **Configure**
- Select your repository and follow the instructions

After this Renovate will create a GitHub issue in your repository which serves as a dashboard, you can see here which updates are pending and trigger Renovate to check again.

## Automatic Release Drafts

Automatically generate release notes with the [Release Drafter](https://github.com/release-drafter/release-drafter) workflow. This uses the labels from issues and pull requests to draft pretty and detailed release notes for your GitHub releases.

## Shared GitHub configuration

Release Drafter uses the repository owner's `.github` defaults when no local release configuration exists. For `klaasnicolaas`, this is [klaasnicolaas/.github](https://github.com/klaasnicolaas/.github). The release workflow remains in the generated package.

Labels are synchronized centrally: add each newly generated repository to the target list in `.github` and grant the central label token access. Packages no longer contain a local label blueprint or sync workflow.

Renovate uses the shared Python preset through its local `extends` reference. For another owner, configure that owner's Release Drafter defaults and label synchronization, and review the Renovate preset reference. See the [central configuration guide](https://github.com/klaasnicolaas/.github#readme).

## Updating

Future boilerplate updates can be as simple as:

```bash
copier update --trust --skip-answered
```

In case you want to update your answers to the questions as well as update:

```bash
copier update --trust
```

## Start developing on this template

This Python template project relies on [uv] as its dependency manager,
providing comprehensive management and control over project dependencies.

You need at least:

- [Python] 3.12+ - The programming language
- [uv] - A python virtual environment/package manager

Install all packages, including all development requirements:

```shell
uv sync --dev
```

### Prek hooks

This project uses [prek](https://github.com/j178/prek) to run some checks before committing code. To install the prek hooks, run the following command:

```shell
uv run prek install
```

To run all hooks manually without linting the `template/` workspace, run:

```shell
uv run prek run --all-files
```

### Keep template dependencies up to date

The [pyproject.toml](./template/pyproject.toml.j2) file of the template has a jinja2 extension and is therefore not seen by Renovate bot to update automatically. That's why I keep track of the dependencies separately in a [Gist](https://gist.github.com/klaasnicolaas/323975ac4f173087a979209cd1c8f202) and a [workflow](./.github/workflows/sync-dependencies.yaml) will check every week if anything needs to be adjusted.

## License

Distributed under the **MIT** License. See [`LICENSE`](LICENSE) for more information.

<!-- Links -->
[copier]: https://copier.readthedocs.io/en/stable/
[gh-actions]: https://github.com/features/actions
[ty]: https://docs.astral.sh/ty/
[poetry]: https://python-poetry.org/
[pytest]: https://docs.pytest.org/en/latest/
[ruff]: https://beta.ruff.rs/docs/
[thrusted]: https://docs.pypi.org/trusted-publishers/using-a-publisher/
[renovate]: https://docs.renovatebot.com/
[devcontainer]: https://code.visualstudio.com/docs/remote/containers

[uv]: https://docs.astral.sh/uv/
[Python]: https://www.python.org/

<!-- Shields -->
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/pypackage-template.svg
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/pypackage-template.svg
[releases]: https://github.com/klaasnicolaas/pypackage-template/releases
