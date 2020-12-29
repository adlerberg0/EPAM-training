"""
Write a context manager, that suppresses passed exception.
Do it both ways: as a class and as a generator.
#>>> with supressor(IndexError):
#...    [][2]
"""
from contextlib import contextmanager
from types import TracebackType
from typing import Optional, Type  # noqa


class SupressorClass:
    def __init__(self, exception_type: Type[BaseException]):
        self.exception_type = exception_type

    def __enter__(self):
        ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[Type[TracebackType]],
    ) -> bool:
        if exc_type == self.exception_type:
            return True


@contextmanager
def supressor_gen(exception_type: Optional[Type[BaseException]]) -> None:
    try:
        yield None
    except exception_type:
        return
