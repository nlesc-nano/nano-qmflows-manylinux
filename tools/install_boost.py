"""Python script for installing Boost."""

from __future__ import annotations

import shutil
import os
import argparse
from pathlib import Path

from dep_builder import TimeLogger, download_and_unpack, parse_version

URL_TEMPLATE = "https://boostorg.jfrog.io/artifactory/main/release/{version}/source/boost_{version_underscore}.tar.gz"

download_boost = TimeLogger("Download and unpack Boost")(download_and_unpack)
parse_boost_version = TimeLogger("Parsing Boost version")(parse_version)


def main(version: str, prefix: str | None = None) -> None:
    """Run the script."""
    parse_boost_version(version)
    version_underscore = version.replace(".", "_")
    url = URL_TEMPLATE.format(version=version, version_underscore=version_underscore)

    src_path: None | Path = None
    try:
        src_path = download_boost(url)
        if prefix is not None:
            shutil.move(
                os.path.join(src_path, "boost"),
                os.path.join(prefix, "include", "boost"),
            )
    finally:
        if src_path is not None:
            shutil.rmtree(src_path, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./install_boost.py 12.1", description=__doc__)
    parser.add_argument("version", help="The library version")
    parser.add_argument(
        "--prefix", nargs=1, help="install architecture-independent files in PREFIX.",
        default=[None], dest="prefix",
    )

    args = parser.parse_args()
    main(args.version, args.prefix[0])
