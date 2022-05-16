"""Script for generating readme files for auto-generated MacOS C++ dependencies."""

import os
import argparse
import datetime


def _parse_env_vars() -> "dict[str, str]":
    names = [
        "HIGHFIVE_VERSION",
        "BOOST_VERSION",
        "EIGEN_VERSION",
        "HDF5_VERSION",
        "LIBINT_VERSION",
    ]
    i = len("_VERSION")
    try:
        return {k[:-i]: os.environ[k] for k in names}
    except KeyError as ex:
        raise ValueError(f"Missing environment variable: {ex}") from None


VERSION_DICT = _parse_env_vars()


def main(output: "str | os.PathLike[str]") -> None:
    with open(output, "w", encoding="utf8") as f:
        f.write(f"Auto-generated MacOS C++ build dependencies ({datetime.datetime.now()})\n\n")
        f.write("Packages\n--------\n")
        for k, v in VERSION_DICT.items():
            f.write(f"- {k}: {v}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="python construct_readme.py README.rst", description=__doc__
    )
    parser.add_argument("path", help="The path to the to-be created README file")
    args = parser.parse_args()
    main(args.path)
