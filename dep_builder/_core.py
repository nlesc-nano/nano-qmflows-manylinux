"""The core functions for compiling packages."""

from __future__ import annotations

import operator
import tarfile
import stat
import os
import subprocess
from collections.abc import Iterable
from pathlib import Path

import requests
from packaging.version import Version

from . import logger

__all__ = ["download_and_unpack", "configure", "read_config_log", "build", "parse_version"]


def parse_version(version: str) -> Version:
    """Check that a PEP 440-compliant version is provided.

    Parameters
    ----------
    version : str
        The to-be validated version.

    Returns
    -------
    packaging.version.Version
        The fully parsed version object.

    """
    ret = Version(version)
    logger.info(f"Successfully parsed {version!r}")
    return ret


def download_and_unpack(
    url: str,
    archive_path: str | os.PathLike[str] = "tmp.tar.gz",
    delete_archive: bool = True,
) -> Path:
    """Download and unpack the archive from the provided URL.

    Parameters
    ----------
    url : str
        The URL to the to-be downloaded tar archive.
    archive_path : str | os.PathLike[str]
        The (absolute) path to the to-be downloaded archive.
    delete_archive : bool
        Whether the archive should be deleted after the download is complete.

    Returns
    -------
    pathlib.Path
        The absolute path to the downloaded and extracted archive.

    """
    archive_path = os.fsdecode(archive_path)
    logger.info(f"Download {url!r}")
    try:
        with open(archive_path, "wb") as f1, requests.get(url, allow_redirects=True) as r:
            r.raise_for_status()
            f1.write(r.content)

        with tarfile.open(archive_path, "r") as f2:
            root = {i.split(os.sep)[0 if not i.startswith(".") else 1] for i in f2.getnames()}
            if len(root) != 1:
                raise ValueError(
                    f"Expected a single top-directory in {archive_path!r}, observed {len(root)}"
                )
            output_dir = root.pop()
            logger.info(f"Unpack archive {archive_path!r} to {output_dir!r}")
            f2.extractall()
    finally:
        if delete_archive and os.path.isfile(archive_path):
            os.remove(archive_path)

    return Path(os.getcwd()) / output_dir


def configure(
    src_path: str | os.PathLike[str],
    build_path: str | os.PathLike[str] = "build",
    config_args: Iterable[str] = (),
) -> None:
    """Run the ``configure`` executable from the passed source path.

    Parameters
    ----------
    src_path : str | os.PathLike[str]
        The path to the source directory.
    build_path : str | os.PathLike[str]
        The path to the to-be created build directory.
    config_args : Iterable[str]
        Arguments for the ``configure`` executable in ``src_path``.

    """
    config_path = os.path.join(src_path, "configure")
    os.chmod(config_path, stat.S_IRUSR | stat.S_IXUSR)

    cmd = " ".join([config_path, *config_args])
    logger.info(cmd)

    os.mkdir(build_path)
    subprocess.run(cmd, shell=True, cwd=build_path, check=True)


def read_config_log(
    build_path: str | os.PathLike[str] = "build",
    log_name: str | os.PathLike[str] = "config.log",
) -> None:
    """Write the ``./configure`` output to the logger.

    Parameters
    ----------
    build_path : str | os.PathLike[str]
        The path to the build directory.
    log_name : str | os.PathLike[str]
        The name of the logfile inside ``build_path``.

    """
    log_file = os.path.join(build_path, log_name)
    if not os.path.isfile(log_file):
        logger.debug(f"No such file: {log_file!r}")
        return

    with open(log_file, "r", encoding="utf8") as f:
        for i in f:
            logger.debug(i.strip())


def build(build_path: str | os.PathLike[str], cpu_count: int | None = None) -> None:
    """Build and install a package via GNU make.

    Parameters
    ----------
    build_path : str | os.PathLike[str]
        The path to the build directory.
    cpu_count : int | None
        The number of CPU cores to use for the build process.
        Using :data:`None` defaults to the output of :func:`os.cpu_count`.

    """
    if cpu_count is None:
        cpu_count = os.cpu_count()
    else:
        cpu_count = operator.index(cpu_count)

    logger.info(f"Running 'make -j {cpu_count} && make install'")
    subprocess.run(f"make -j {cpu_count}", shell=True, cwd=build_path, check=True)
    subprocess.run("make install", shell=True, cwd=build_path, check=True)
