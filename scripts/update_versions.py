"""Updates the versions.json file with the latest package versions from PyPI."""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

import requests

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
    match = re.match(r"^([<>=!~^]{1,2})(.+)$", spec)
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
    except requests.exceptions.ConnectionError as err:
        msg = f"Failed to connect to PyPI for package '{package}'. Please check your network connection."  # noqa: E501

        raise RuntimeError(msg) from err
    except requests.exceptions.Timeout as err:
        msg = f"Request to PyPI for package '{package}' timed out. Please try again later."  # noqa: E501
        raise RuntimeError(msg) from err
    except requests.exceptions.HTTPError as err:
        msg = f"HTTP error occurred while fetching package '{package}' from PyPI: {err}"
        raise RuntimeError(msg) from err
    except requests.exceptions.RequestException as err:
        msg = f"An error occurred while fetching package '{package}' from PyPI: {err}"
        raise RuntimeError(msg) from err


def update_spec(
    name: str,
    spec: str | dict[str, str],
) -> tuple[str | dict[str, str], bool, str, str]:
    """Update a version specifier to the latest PyPI version."""
    if isinstance(spec, str):
        operator, current = split_operator_version(spec)
        latest = fetch_latest_pypi_version(name)
        new_spec = f"{operator}{latest}" if operator else latest
        return new_spec, current != latest, f"{operator}{current}", new_spec

    if isinstance(spec, dict) and "version" in spec:
        operator, current = split_operator_version(spec["version"])
        latest = fetch_latest_pypi_version(name)
        updated_version = f"{operator}{latest}" if operator else latest
        new_spec = {**spec, "version": updated_version}
        return new_spec, current != latest, f"{operator}{current}", updated_version

    return spec, False, "", ""


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
        updated[group] = {}
        for name, spec in deps.items():
            try:
                new_spec, changed, before, after = update_spec(name, spec)
                updated[group][name] = new_spec

                if changed:
                    has_updates = True
                    LOGGER.info(
                        "✅ [UPDATE]   %-20s (%s) %s → %s",
                        name,
                        group,
                        before,
                        after,
                    )
                else:
                    LOGGER.info(
                        "➖ [UNCHANGED] %-20s (%s) %s",  # noqa: RUF001
                        name,
                        group,
                        before or spec,
                    )

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
