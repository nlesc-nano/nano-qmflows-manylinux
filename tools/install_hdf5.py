"""Python script for installing HDF5."""

from __future__ import annotations

import shutil
import os
import sys
import argparse
from pathlib import Path
from collections.abc import Iterable

from packaging.version import Version
from dep_builder import logger, TimeLogger, download_and_unpack, configure, read_config_log, build

URL_TEMPLATE = "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-{version_short}/hdf5-{version}/src/hdf5-{version}.tar.gz"

download_hdf5 = TimeLogger("Download and unpack HDF5")(download_and_unpack)
read_config_log_hdf5 = TimeLogger("Dumping HDF5 config log")(read_config_log)
build_hdf5 = TimeLogger("Build HDF5")(build)


@TimeLogger("Configure HDF5")
def configure_hdf5(
    src_path: str | os.PathLike[str],
    build_path: str | os.PathLike[str] = "build",
    config_args: Iterable[str] = (),
) -> None:
    args = ["--enable-build-mode=production"]
    args.extend(config_args)
    if sys.platform == "darwin":
        args.append("--libdir='/usr/local/lib'")
    configure(src_path, build_path, args)


@TimeLogger("Parsing HDF5 version")
def parse_version(version: str) -> tuple[str, str]:
    """Parse and validate the HDF5 version."""
    version_obj = Version(version)
    version_short = f"{version_obj.release[0]}.{version_obj.release[1]}"
    logger.info(f"Successfully parsed {version!r}")
    return version, version_short


def main(version: str, prefix: str | None = None, n_jobs: int = 1) -> None:
    """Run the script."""
    version, version_short = parse_version(version)
    url = URL_TEMPLATE.format(version=version, version_short=version_short)

    src_path: None | Path = None
    build_path = Path(os.getcwd()) / "build"

    try:
        src_path = download_hdf5(url)
        args = [f"--prefix={prefix}"] if prefix is not None else []
        try:
            configure_hdf5(src_path, build_path, config_args=args)
        finally:
            read_config_log_hdf5(build_path)
        build_hdf5(build_path, n_jobs)
    finally:
        shutil.rmtree(build_path, ignore_errors=True)
        if src_path is not None:
            shutil.rmtree(src_path, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./install_h5py.py 12.1", description=__doc__)
    parser.add_argument("version", help="The HDF5 version")
    parser.add_argument(
        "-j", "--jobs", nargs=1, help="Allow N jobs at once; 1 job with no arg.",
        default=[1], dest="n_jobs", metavar="N",
    )
    parser.add_argument(
        "--prefix", nargs=1, help="install architecture-independent files in PREFIX.",
        default=[None], dest="prefix",
    )

    args = parser.parse_args()
    main(args.version, args.prefix[0], args.n_jobs[0])
