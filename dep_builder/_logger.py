from __future__ import annotations

import logging
import contextlib
import sys
import time
import types
from typing import ClassVar, TypeVar

_Self = TypeVar("_Self", bound="TimeLogger")

__all__ = ["logger", "stdout_handler", "TimeLogger"]

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(logging.Formatter(
    fmt="%(message)s",
))
logger.addHandler(stdout_handler)


class TimeLogger(contextlib.ContextDecorator):
    __slots__ = ("message", "_start")

    GREEN: ClassVar = "\033[32m"
    RED: ClassVar = "\033[31m"
    logger: ClassVar = logger

    def __init__(self, message: None | str = None) -> None:
        self.message = message

    def __enter__(self) -> None:
        self._start = time.time()
        if self.message is not None:
            self.logger.info(f"::group::{self.message}")
        else:
            self.logger.info("::group::")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: types.TracebackType | None
    ) -> None:
        duration = time.time() - self._start
        sys.stdout.flush()
        self.logger.info("\n::endgroup::")
        if exc_type is None:
            self.logger.info(f"{self.GREEN}✓ {duration:.2f}s".rjust(78))
        else:
            self.logger.info(f"{self.RED}✕ {duration:.2f}s".rjust(78))

    def __repr__(self) -> str:
        cls = type(self)
        return f"{cls.__name__}(message={self.message!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TimeLogger):
            return NotImplemented
        return self.logger == other.logger and self.message == other.message

    def __reduce__(self: _Self) -> tuple[type[_Self], tuple[str | None]]:
        cls = type(self)
        return cls, (self.message,)
