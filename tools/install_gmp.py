"""Python script for installing GMP."""

from __future__ import annotations

import shutil
import os
import argparse
from pathlib import Path

from dep_builder import TimeLogger, download_and_unpack, configure, read_config_log, build, parse_version

URL_TEMPLATE = "https://gmplib.org/download/gmp/gmp-{version}.tar.xz"

download_gmp = TimeLogger("Download and unpack GMP")(download_and_unpack)
read_config_log_gmp = TimeLogger("Dumping GMP config log")(read_config_log)
build_gmp = TimeLogger("Build GMP")(build)
configure_gmp = TimeLogger("Configure GMP")(configure)
parse_gmp_version = TimeLogger("Parsing GMP version")(parse_version)


def main(version: str, args: list[str]) -> None:
    """Run the script."""
    parse_gmp_version(version)
    url = URL_TEMPLATE.format(version=version)

    src_path: None | Path = None
    build_path = Path(os.getcwd()) / "build"

    try:
        src_path = download_gmp(url)
        try:
            config_args = ["--enable-cxx"] + args
            configure_gmp(src_path, build_path, config_args=config_args)
        finally:
            read_config_log_gmp(build_path)
        build_gmp(build_path)
    finally:
        shutil.rmtree(build_path, ignore_errors=True)
        if src_path is not None:
            shutil.rmtree(src_path, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./install_gmp.py 6.2.1", description=__doc__)
    parser.add_argument("version", help="The library version")
    parser.add_argument("args", metavar="ARGS", default=[], nargs=argparse.REMAINDER,
                        help="Arguments to pass the 'configure' file")

    args = parser.parse_args()
    main(args.version, args.args)
