"""Logging-related utilities."""

from __future__ import annotations

import logging
import contextlib
import sys
import time
import types
from typing import TYPE_CHECKING, ClassVar, TypeVar, Generic
from collections.abc import Iterable

if TYPE_CHECKING:
    from typing_extensions import Protocol

    class _HandlerProtocol(Protocol):
        def flush(self) -> object: ...

    class _LoggingProtocol(Protocol):
        @property
        def handlers(self) -> Iterable[_HandlerProtocol]: ...
        def info(self, __message: str) -> object: ...

_Self = TypeVar("_Self", bound="BaseTimeLogger")
_LoggerType = TypeVar("_LoggerType", bound="_LoggingProtocol")

__all__ = ["logger", "stdout_handler", "TimeLogger", "BaseTimeLogger"]

#: The default logger.
logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)

#: The default stdout handler.
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(logging.Formatter(
    fmt="%(message)s",
))
logger.addHandler(stdout_handler)


class BaseTimeLogger(contextlib.ContextDecorator, Generic[_LoggerType]):
    """A context decorator for logging github-style ``:group:`` blocks before/after function calls.

    Examples
    --------
    .. code-block:: python

        >>> import sys
        >>> import logging
        >>> from dep_builder import BaseTimeLogger

        >>> logger = logging.getLogger()
        >>> logger.setLevel(logging.INFO)
        >>> logger.addHandler(logging.StreamHandler(stream=sys.stdout))

        >>> @BaseTimeLogger(logger, "message block")
        ... def func() -> None:
        ...     print("1 2 3 4")

        >>> func()
        ::group::message block
        1 2 3 4

        ::endgroup::
                                                                        ✓ 0.00s

    Parameters
    ----------
    logger : logging.Logger
        The to-be wrapped :class:`~logging.Logger`.
    message : None | str
        The group-message to-be displayed upon entering the context manager.

    """
    __slots__ = ("_message", "_start", "_logger", "_hash")

    GREEN: ClassVar[str] = "\033[32m"
    RED: ClassVar[str] = "\033[31m"

    @property
    def message(self) -> None | str:
        """The group-message to-be displayed upon entering the context manager."""
        return self._message

    @property
    def logger(self) -> _LoggerType:
        """The wrapped :class:`~logging.Logger`."""
        return self._logger

    def __init__(self, logger: _LoggerType, message: None | str = None) -> None:
        """Initialize the instance."""
        self._logger = logger
        self._message = message

    def __enter__(self) -> None:
        """Enter the context manager."""
        self._start = time.time()
        self.flush()
        if self.message is not None:
            self.write(f"::group::{self.message}")
        else:
            self.write("::group::")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: types.TracebackType | None
    ) -> None:
        """Exit the context manager."""
        duration = time.time() - self._start
        self.flush()
        self.write("\n::endgroup::")
        if exc_type is None:
            self.write(f"{self.GREEN}✓ {duration:.2f}s".rjust(78))
        else:
            self.write(f"{self.RED}✕ {duration:.2f}s".rjust(78))

    def __repr__(self) -> str:
        """Implement :func:`repr(self) <repr>`."""
        cls = type(self)
        return f"{cls.__name__}(logger={self.logger!r}, message={self.message!r})"

    def __eq__(self, other: object) -> bool:
        """Implement :meth:`self == other <object.__eq__>`."""
        if not isinstance(other, BaseTimeLogger):
            return NotImplemented
        return self.logger == other.logger and self.message == other.message

    def __copy__(self: _Self) -> _Self:
        """Implement :func:`copy.copy(self) <copy.copy>`."""
        return self

    def __deepcopy__(self: _Self, memo: object = None) -> _Self:
        """Implement :func:`copy.deepcopy(self) <copy.deepcopy>`."""
        return self

    def __hash__(self) -> int:
        """Implement :func:`hash(self) <hash>`."""
        try:
            return self._hash
        except AttributeError:
            pass
        self._hash: int = hash(self.logger) ^ hash(self.message)
        return self._hash

    def __reduce__(self: _Self) -> tuple[type[_Self], tuple[_LoggerType, str | None]]:
        """Helper for :mod:`pickle`."""
        cls = type(self)
        return cls, (self.logger, self.message)

    def flush(self) -> None:
        """Flush all logging handlers."""
        for handler in self.logger.handlers:
            handler.flush()

    def write(self, message: str) -> None:
        """Write to the logger at the ``INFO`` level."""
        self.logger.info(message)


class TimeLogger(BaseTimeLogger[logging.Logger]):
    """A :class:`BaseTimeLogger` subclass with a fixed :class:`~logging.Logger` instance.

    Parameters
    ----------
    message : None | str
        The group-message to-be displayed upon entering the context manager.

    """

    __slots__ = ()

    _logger = logger

    def __init__(self, message: None | str = None) -> None:
        """Initialize the instance."""
        self._message = message

    def __repr__(self) -> str:
        """Implement :func:`repr(self) <repr>`."""
        cls = type(self)
        return f"{cls.__name__}(message={self.message!r})"

    def __reduce__(self: _Self) -> tuple[type[_Self], tuple[str | None]]:  # type: ignore[override]
        """Helper for :mod:`pickle`."""
        cls = type(self)
        return cls, (self.message,)
