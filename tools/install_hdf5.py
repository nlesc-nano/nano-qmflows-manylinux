"""Python script for installing HDF5."""

from __future__ import annotations

import subprocess
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


@TimeLogger("Patch HDF5 for MacOS-ARM64 cross-compilation")
def patch_hdf5(src_path: str | os.PathLike[str]) -> None:
    """Apply a hdf5 1.21.1 cross-compilation patch for MacOS M1.

    Xref https://github.com/h5py/h5py/pull/2065.

    """
    root = Path(__file__).parent
    configure = root / "osx_cross_configure.patch"
    src_makefile = root / "osx_cross_src_makefile.patch"
    subprocess.run(f"patch -p0 < {configure}", shell=True, cwd=src_path, check=True)
    subprocess.run(f"patch -p0 < {src_makefile}", shell=True, cwd=src_path, check=True)


@TimeLogger("Re-building H5detect and H5make_libsettings for MacOS-ARM64 cross-compilation")
def build_h5detect(src_path: str | os.PathLike[str], build_path: str | os.PathLike[str]) -> None:
    src = os.path.join(build_path, "src")
    subprocess.run(
        f"CFLAGS= $CC src/H5detect.c -I {src} -o /tmp/native-build/bin/H5detect",
        shell=True, cwd=src_path, check=True,
    )
    subprocess.run(
        f"CFLAGS= $CC src/H5make_libsettings.c -I {src} -o /tmp/native-build/bin/H5make_libsettings",
        shell=True, cwd=src_path, check=True,
    )


def main(version: str, args: list[str]) -> None:
    """Run the script."""
    version_obj = parse_hdf5_version(version)
    version_short = f"{version_obj.release[0]}.{version_obj.release[1]}"
    url = URL_TEMPLATE.format(version=version, version_short=version_short)

    src_path: None | Path = None
    build_path = Path(os.getcwd()) / "build"

    try:
        src_path = download_hdf5(url)
        if os.environ.get("APPLY_HDF5_PATCH"):
            patch_hdf5(src_path)
        try:
            config_args = ["--enable-build-mode=production", "--enable-tests=no"] + args
            configure_hdf5(src_path, build_path, config_args=config_args)
        finally:
            read_config_log_hdf5(build_path)
        if os.environ.get("APPLY_HDF5_PATCH"):
            build_h5detect(src_path, build_path)
        build_hdf5(build_path)
    finally:
        shutil.rmtree(build_path, ignore_errors=True)
        if src_path is not None:
            shutil.rmtree(src_path, ignore_errors=True)
        if os.environ.get("APPLY_HDF5_PATCH"):
            shutil.rmtree("/tmp/native-build", ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./install_hdf5.py 1.12.2", description=__doc__)
    parser.add_argument("version", help="The library version")
    parser.add_argument("args", metavar="ARGS", default=[], nargs=argparse.REMAINDER,
                        help="Arguments to pass the 'configure' file")

    args = parser.parse_args()
    main(args.version, args.args)
