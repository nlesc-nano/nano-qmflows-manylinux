"""Python script for installing HighFive."""

from __future__ import annotations

import shutil
import os
import argparse
from pathlib import Path

from dep_builder import TimeLogger, download_and_unpack, parse_version

URL_TEMPLATE = "https://github.com/BlueBrain/HighFive/archive/refs/tags/v{version}.tar.gz"

download_highfive = TimeLogger("Download and unpack HighFive")(download_and_unpack)
parse_highfive_version = TimeLogger("Parsing HighFive version")(parse_version)


def main(version: str, prefix: str | None = None) -> None:
    """Run the script."""
    parse_highfive_version(version)
    url = URL_TEMPLATE.format(version=version)

    src_path: None | Path = None
    try:
        src_path = download_highfive(url)
        if prefix is not None:
            shutil.move(
                os.path.join(src_path, "include", "highfive"),
                os.path.join(prefix, "include", "highfive"),
            )
    finally:
        if src_path is not None:
            shutil.rmtree(src_path, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./install_highfive.py 12.1", description=__doc__)
    parser.add_argument("version", help="The library version")
    parser.add_argument(
        "--prefix", nargs=1, help="install architecture-independent files in PREFIX.",
        default=[None], dest="prefix",
    )

    args = parser.parse_args()
    main(args.version, args.prefix[0])
