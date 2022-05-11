from __future__ import annotations

import stat
import os
import subprocess
from collections.abc import Iterable

from . import logger

__all__ = ["configure", "read_config_log", "build"]


def configure(
    src_path: str | os.PathLike[str],
    build_path: str | os.PathLike[str] = "build",
    config_args: Iterable[str] = (),
) -> None:
    config_path = os.path.join(src_path, "configure")
    os.chmod(config_path, stat.S_IRUSR | stat.S_IXUSR)

    args = [config_path]
    args.extend(config_args)
    os.mkdir(build_path)
    subprocess.run(" ".join(args), shell=True, cwd=build_path, check=True)


def read_config_log(
    build_path: str | os.PathLike[str] = "build",
    log_name: str | os.PathLike[str] = "config.log",
) -> None:
    log_file = os.path.join(build_path, log_name)
    if not os.path.isfile(log_file):
        logger.debug(f"No such file: {log_file!r}")
        return

    with open(log_file, "r", encoding="utf8") as f:
        for i in f:
            logger.debug(i.strip())


def build(build_path: str | os.PathLike[str], n_proc: int = 1) -> None:
    subprocess.run(f"make -j {n_proc}", shell=True, cwd=build_path, check=True)
    subprocess.run(f"make install", shell=True, cwd=build_path, check=True)
