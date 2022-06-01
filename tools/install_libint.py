"""Python script for installing Libint."""

from __future__ import annotations

import subprocess
import shutil
import os
import stat
import argparse
from pathlib import Path

from dep_builder import TimeLogger, download_and_unpack, configure, read_config_log, build, parse_version

URL_TEMPLATE = "https://github.com/evaleev/libint/archive/refs/tags/v{version}.tar.gz"

download_libint = TimeLogger("Download and unpack Libint")(download_and_unpack)
read_config_log_libint = TimeLogger("Dumping Libint config log")(read_config_log)
build_libint = TimeLogger("Build Libint")(build)
configure_libint = TimeLogger("Configure Libint")(configure)
parse_libint_version = TimeLogger("Parsing Libint version")(parse_version)


@TimeLogger("Run Libint autogen")
def run_autogen(src_path: str | os.PathLike[str]) -> None:
    os.chmod(os.path.join(src_path, "autogen.sh"), stat.S_IRUSR | stat.S_IXUSR)
    subprocess.run("bash autogen.sh", shell=True, cwd=src_path, check=True)


def main(version: str, args: list[str]) -> None:
    """Run the script."""
    parse_libint_version(version)
    url = URL_TEMPLATE.format(version=version)

    src_path: None | Path = None
    build_path = Path(os.getcwd()) / "build"

    try:
        src_path = download_libint(url)
        run_autogen(src_path)
        try:
            config_args = ["--enable-shared=yes"] + args
            configure_libint(src_path, build_path, config_args=config_args)
        finally:
            read_config_log_libint(build_path)
        build_libint(build_path)
    finally:
        shutil.rmtree(build_path, ignore_errors=True)
        if src_path is not None:
            shutil.rmtree(src_path, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./install_libint.py 2.7.1", description=__doc__)
    parser.add_argument("version", help="The library version")
    parser.add_argument("args", metavar="ARGS", default=[], nargs=argparse.REMAINDER,
                        help="Arguments to pass the 'configure' file")

    args = parser.parse_args()
    main(args.version, args.args)
