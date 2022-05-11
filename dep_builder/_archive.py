from __future__ import annotations

import tarfile
import os
from pathlib import Path

import requests

from . import logger

__all__ = ["download_and_unpack"]


def download_and_unpack(
    url: str,
    archive_path: str | os.PathLike[str] = "tmp.tar.gz",
    delete_archive: bool = True,
) -> Path:
    """Download and unpack the archive from the provided url."""
    logger.info(f"Download {url!r}")
    try:
        with open(archive_path, "wb") as f1, requests.get(url, allow_redirects=True) as r:
            r.raise_for_status()
            f1.write(r.content)

        logger.info(f"Unpack archive {os.fspath(archive_path)!r}")
        with tarfile.open(archive_path, "r") as f2:
            root = {i.split(os.sep)[0] for i in f2.getnames()}
            if len(root) != 1:
                raise ValueError(
                    f"Expected a single top-directory in {os.fspath(archive_path)!r}, "
                    f"observed {len(root)}"
                )
            f2.extractall()
    finally:
        if delete_archive:
            os.remove(archive_path)

    return Path(os.getcwd()) / root.pop()
