"""Python script for installing Eigen."""

from __future__ import annotations

import shutil
import os
import argparse
from pathlib import Path

from packaging.version import Version
from dep_builder import logger, TimeLogger, download_and_unpack

URL_TEMPLATE = "https://gitlab.com/libeigen/eigen/-/archive/{version}/eigen-{version}.tar.gz"

download_eigen = TimeLogger("Download and unpack Eigen")(download_and_unpack)


@TimeLogger("Parsing Eigen version")
def parse_version(version: str) -> None:
    Version(version)
    logger.info(f"Successfully parsed {version!r}")


def main(version: str, prefix: str | None = None) -> None:
    """Run the script."""
    parse_version(version)
    url = URL_TEMPLATE.format(version=version)

    src_path: None | Path = None
    try:
        src_path = download_eigen(url)
        if prefix is not None:
            shutil.move(
                os.path.join(src_path, "Eigen"),
                os.path.join(prefix, "include", "Eigen"),
            )
    finally:
        if src_path is not None:
            shutil.rmtree(src_path, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./install_eigen.py 12.1", description=__doc__)
    parser.add_argument("version", help="The library version")
    parser.add_argument(
        "--prefix", nargs=1, help="install architecture-independent files in PREFIX.",
        default=[None], dest="prefix",
    )

    args = parser.parse_args()
    main(args.version, args.prefix[0])
