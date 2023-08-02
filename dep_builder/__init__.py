"""Utilities for the building of packages and logging thereof.

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
    __version_tuple__

API
---
.. autofunction:: download_and_unpack
.. autofunction:: configure
.. autofunction:: read_config_log
.. autofunction:: build
.. autofunction:: parse_version
.. autoclass:: BaseTimeLogger
    :members: message, logger, write, flush
.. autoclass:: TimeLogger
.. autodata:: logger
.. autodata:: __version__
.. autodata:: __version_tuple__

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._version import __version__, __version_tuple__
from ._logger import logger, TimeLogger, BaseTimeLogger
from ._core import download_and_unpack, configure, read_config_log, build, parse_version

__all__ = [
    "__version__",
    "__version_tuple__",
    "logger",
    "BaseTimeLogger",
    "TimeLogger",
    "download_and_unpack",
    "configure",
    "read_config_log",
    "build",
    "parse_version",
]

# Redeclare these objects in the scope of the main namespace so they're picked
# up by Sphinx's `autodata` directive
if not TYPE_CHECKING:
    #: The :mod:`dep_builder` version.
    __version__: str

    #: The :mod:`dep_builder` version as a tuple.
    __version_tuple__: tuple

    #: The :mod:`dep_builder` logger.
    logger: logging.Logger  # noqa: F821

del TYPE_CHECKING
