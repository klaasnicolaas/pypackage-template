"""Updates the versions.json file with the latest package versions from PyPI."""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

import requests
from packaging.version import InvalidVersion, Version

VERSIONS_PATH = Path("versions.json")

# Logging setup
logging.addLevelName(logging.INFO, "")
logging.addLevelName(logging.ERROR, "::error::")
logging.addLevelName(logging.WARNING, "::warning::")
logging.basicConfig(
    level=logging.INFO,
    format=" %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
LOGGER = logging.getLogger(__name__)


def split_operator_version(spec: str) -> tuple[str, str]:
    """Split a version specifier into operator and version.

    Args:
        spec (str): The version specifier string.

    Returns:
        tuple[str, str]: A tuple containing the operator and version.

    """
    match = re.match(r"^([<>=!~^]{1,2})?(.+)$", spec)
    if not match:
        return "", spec
    return match.group(1), match.group(2)


def fetch_latest_pypi_version(package: str) -> str:
    """Fetch the latest version of a package from PyPI.

    Args:
        package (str): The name of the package to check.

    Returns:
        str: The latest version of the package.

    Raises:
        RuntimeError: If there is an issue connecting to PyPI or fetching the version.

    """
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()["info"]["version"]
    except requests.exceptions.RequestException as err:
        raise RuntimeError(f"Failed to fetch {package} from PyPI: {err}") from err  # noqa: EM102


def get_minor_range(version: str) -> str:
    """Get the minor version range for a given version string.

    Args:
        version (str): The version string to process.

    Returns:
        str: A string representing the minor version range, e.g., ">=1.2.0".

    Raises:
        ValueError: If the version string is invalid.

    """
    try:
        v = Version(version)
    except InvalidVersion as err:
        raise ValueError(f"Invalid version string: {version}") from err  # noqa: EM102
    else:
        return f">={v.major}.{v.minor}.0"


def format_version(
    version: str,
    operator: str,
    patch_only: bool,  # noqa: FBT001
) -> str:
    """Format a version string with an operator.

    Args:
        version (str): The version string to format.
        operator (str): The operator to prepend to the version.
        patch_only (bool): If True, return a minor version range.

    Returns:
        str: The formatted version string.

    """
    return (
        get_minor_range(version)
        if patch_only
        else f"{operator}{version}"
        if operator
        else version
    )


def update_spec(
    name: str,
    spec: str | dict[str, str],
    patch_only: bool = False,  # noqa: FBT001, FBT002
) -> tuple[str | dict[str, str], bool, str, str]:
    """Update a version specifier to the latest PyPI version."""
    original = spec["version"] if isinstance(spec, dict) else spec
    operator, _ = split_operator_version(original)

    latest = fetch_latest_pypi_version(name)
    new_version = format_version(latest, operator, patch_only)

    changed = original != new_version
    before = original
    after = new_version

    if isinstance(spec, dict):
        return {**spec, "version": new_version}, changed, before, after
    return new_version, changed, before, after


def main() -> None:
    """Update versions.json with the latest package versions from PyPI."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without writing changes to versions.json",
    )
    args = parser.parse_args()

    raw = json.loads(VERSIONS_PATH.read_text())
    versions = raw.get("versions", raw)

    updated = {}
    has_updates = False

    LOGGER.info("📦 Checking for updated versions...")

    for group, deps in versions.items():
        patch_only = group == "main"
        updated[group] = {}

        for name, spec in deps.items():
            try:
                new_spec, changed, before, after = update_spec(
                    name, spec, patch_only=patch_only
                )
                updated[group][name] = new_spec

                if changed:
                    has_updates = True
                    LOGGER.info(
                        "✅ [UPDATE]   %-20s (%s) %s → %s", name, group, before, after
                    )
                else:
                    LOGGER.info("➖ [UNCHANGED] %-20s (%s) %s", name, group, before)  # noqa: RUF001
            except Exception:
                LOGGER.exception("❌ [ERROR]     %-20s (%s)", name, group)
                updated[group][name] = spec

    if args.dry_run:
        LOGGER.info("💡 Dry-run mode: versions.json not written.")
    else:
        VERSIONS_PATH.write_text(json.dumps({"versions": updated}, indent=2) + "\n")
        LOGGER.info("✅ versions.json updated successfully.")

    if not has_updates:
        LOGGER.info("👍 Everything is already up-to-date.")


if __name__ == "__main__":
    main()
