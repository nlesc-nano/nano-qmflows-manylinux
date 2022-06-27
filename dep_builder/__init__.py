"""Utilities for building (and logging) packages.

Index
-----
.. currentmodule:: dep_builder
.. autosummary::
    download_and_unpack
    configure
    read_config_log
    build
    parse_version
    BaseTimeLogger
    TimeLogger
    logger
    __version__

API
---
.. autofunction:: download_and_unpack
.. autofunction:: configure
.. autofunction:: read_config_log
.. autofunction:: build
.. autofunction:: parse_version
.. autoclass:: BaseTimeLogger
.. autoclass:: TimeLogger
.. autodata:: logger
.. autodata:: __version__

"""

from ._version import __version__
from ._logger import logger, TimeLogger, BaseTimeLogger
from ._core import download_and_unpack, configure, read_config_log, build, parse_version

__all__ = [
    "__version__",
    "logger",
    "BaseTimeLogger",
    "TimeLogger",
    "download_and_unpack",
    "configure",
    "read_config_log",
    "build",
    "parse_version",
]
