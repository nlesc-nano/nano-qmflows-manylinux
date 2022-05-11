"""Python script for installing Libint."""

from __future__ import annotations

import subprocess
import shutil
import os
import sys
import stat
import argparse
from pathlib import Path
from collections.abc import Iterable

from packaging.version import Version
from dep_builder import logger, TimeLogger, download_and_unpack, configure, read_config_log, build

URL_TEMPLATE = "https://github.com/evaleev/libint/archive/refs/tags/v{version}.tar.gz"

download_libint = TimeLogger("Download and unpack Libint")(download_and_unpack)
read_config_log_libint = TimeLogger("Dumping Libint config log")(read_config_log)
build_libint = TimeLogger("Build Libint")(build)


@TimeLogger("Parsing Libint version")
def parse_version(version: str) -> None:
    Version(version)
    logger.info(f"Successfully parsed {version!r}")


@TimeLogger("Configure Libint")
def configure_libint(
    src_path: str | os.PathLike[str],
    build_path: str | os.PathLike[str] = "build",
    config_args: Iterable[str] = (),
) -> None:
    args = ["--enable-shared=yes"]
    if sys.platform == "darwin":
        args.append("--libdir='/usr/local/lib'")
    configure(src_path, build_path, args)


@TimeLogger("Run Libint autogen")
def run_autogen(src_path: str | os.PathLike[str]) -> None:
    os.chmod(os.path.join(src_path, "autogen.sh"), stat.S_IRUSR | stat.S_IXUSR)
    subprocess.run("bash autogen.sh", shell=True, cwd=src_path, check=True)


def main(version: str, prefix: str | None = None, n_jobs: int = 1) -> None:
    """Run the script."""
    parse_version(version)
    url = URL_TEMPLATE.format(version=version)

    src_path: None | Path = None
    build_path = Path(os.getcwd()) / "build"

    try:
        src_path = download_libint(url)
        run_autogen(src_path)
        try:
            args = [f"--prefix={prefix}"] if prefix is not None else []
            configure_libint(src_path, build_path, config_args=args)
        finally:
            read_config_log_libint(build_path)
        build_libint(build_path, n_jobs)
    finally:
        shutil.rmtree(build_path, ignore_errors=True)
        if src_path is not None:
            shutil.rmtree(src_path, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./install_libint.py 12.1", description=__doc__)
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
