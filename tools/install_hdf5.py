"""Python script for installing HDF5."""

from __future__ import annotations

import shutil
import os
import argparse
from pathlib import Path

from dep_builder import TimeLogger, download_and_unpack, configure, read_config_log, build, parse_version

URL_TEMPLATE = "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-{version_short}/hdf5-{version}/src/hdf5-{version}.tar.gz"

download_hdf5 = TimeLogger("Download and unpack HDF5")(download_and_unpack)
read_config_log_hdf5 = TimeLogger("Dumping HDF5 config log")(read_config_log)
build_hdf5 = TimeLogger("Build HDF5")(build)
configure_hdf5 = TimeLogger("Configure HDF5")(configure)
parse_hdf5_version = TimeLogger("Parsing HDF5 version")(parse_version)


def main(version: str, args: list[str]) -> None:
    """Run the script."""
    version_obj = parse_hdf5_version(version)
    version_short = f"{version_obj.release[0]}.{version_obj.release[1]}"
    url = URL_TEMPLATE.format(version=version, version_short=version_short)

    src_path: None | Path = None
    build_path = Path(os.getcwd()) / "build"

    try:
        src_path = download_hdf5(url)
        try:
            config_args = ["--enable-build-mode=production"] + args
            configure_hdf5(src_path, build_path, config_args=config_args)
        finally:
            read_config_log_hdf5(build_path)
        build_hdf5(build_path)
    finally:
        shutil.rmtree(build_path, ignore_errors=True)
        if src_path is not None:
            shutil.rmtree(src_path, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./install_hdf5.py 12.1", description=__doc__)
    parser.add_argument("version", help="The library version")
    parser.add_argument("args", metavar="ARGS", default=[], nargs=argparse.REMAINDER,
                        help="Arguments to pass the 'configure' file")

    args = parser.parse_args()
    main(args.version, args.args)
