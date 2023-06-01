# Python Package Template

<!-- PROJECT SHIELDS -->
[![License][license-shield]](LICENSE)
[![GitHub Release][releases-shield]][releases]

Project template for a Python Package using [Copier][copier].

## Feature Summary

* [GitHub Actions][gh-actions] for continuous integration and publishing to PyPI
* [Poetry][poetry] for dependency management and packaging
* [Thrusted publishers][thrusted] for PyPI releases
* [Black][black] for code formatting
* [mypy][mypy] for static type checking
* [pytest][pytest] for testing with code coverage
* [Ruff][ruff] for linting
* And much more!

### PEP 621 Ready

This template supports [PEP 621](https://peps.python.org/pep-0621), which allows for the placement of project metadata in pyproject.toml.

### GitHub Issue Labelling

Series of helpful labels that you can use to categorise issues and pull requests. These come in especially handy when combined with the Release Drafter workflow!

### Automatic Release Drafts

Automatically generate release notes with the [Release Drafter] workflow. This uses the labels from issues and pull requests to draft pretty and detailed release notes for your GitHub releases.

## Usage

Ensure you have copier installed:

```shell
pipx install copier
```

After installing [copier][copier], run the following and answer the questions.

```shell
copier gh:klaasnicolaas/pypackage-template path/to/destination
```

### Start developing

The project uses [Poetry][poetry] for dependencies management and packaging. Make sure you have it installed in your development machine. To install the development dependencies in a virtual environment, type:

```shell
poetry install
```

This will also generate a `poetry.lock` file, you should track this file in version control. Check out the [Poetry][poetry] documentation for more information on the available commands.


<!-- Links -->
[black]: https://black.readthedocs.io/en/stable/
[copier]: https://copier.readthedocs.io/en/stable/
[gh-actions]: https://github.com/features/actions
[mypy]: https://mypy.readthedocs.io/en/stable/
[poetry]: https://python-poetry.org/
[pytest]: https://docs.pytest.org/en/latest/
[ruff]: https://beta.ruff.rs/docs/
[thrusted]: https://docs.pypi.org/trusted-publishers/using-a-publisher/

<!-- Shields -->
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/pypackage-template.svg
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/pypackage-template.svg
[releases]: https://github.com/klaasnicolaas/pypackage-template/releases