#!/usr/bin/env python3

import argparse
import warnings
from pathlib import Path

# The directory containing this file
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_files(path: Path = PROJECT_ROOT) -> list[Path]:
    """Files where version number must change

    Args:
        path (Path, optional): Repository root path. Defaults to PROJECT_ROOT.

    Returns:
        list[Path]: List of files with path to be changed.
    """
    return [
        PROJECT_ROOT / "pyproject.toml",
        PROJECT_ROOT / "CITATION.cff",
        PROJECT_ROOT / "setup.py",
        PROJECT_ROOT / "tufte" / "__init__.py",
        PROJECT_ROOT / "docs" / "source" / "conf.py",
    ]


def main(find_str: str, replace_str: str):
    """Find and replace instances of string

    Args:
        find_str (str): Instances of string to be found.
        replace_str (str): String to replace found instances.
    """

    files_list = get_files()

    for file in files_list:
        with open(str(file), "r") as f:
            content = f.read()
            if find_str not in content:
                warnings.warn(f"{find_str} not found in {file}")

                continue

        with open(str(file), "w") as f:
            content = content.replace(find_str, replace_str)
            f.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--find",
        default=None,
        type=str,
        help="Finds version instances of the format X.Y.Z",
    )
    parser.add_argument(
        "-r",
        "--replace",
        default=None,
        type=str,
        help="Replace found instances. Must have the format X.Y.Z",
    )

    args = parser.parse_args()

    main(args.find, args.replace)
