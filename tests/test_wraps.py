from __future__ import annotations

from inspect import signature
from typing import Any, Callable

from tightwrap import wraps


def test_wraps() -> None:
    """Wraps works."""

    def wrapped(a: int) -> int:
        return a + 1

    @wraps(wrapped)
    def wrapper(a: int) -> int:
        return wrapped(a)

    assert wrapper(3) == 4
    assert signature(wrapped) == signature(wrapper)

    _: Callable[[int], int] = wrapper


def test_wraps_different_return() -> None:
    def wrapped(a: int) -> int:
        return a + 1

    @wraps(wrapped)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        return str(wrapped(*args, **kwargs))

    assert wrapper(3) == "4"
    assert signature(wrapped, eval_str=True).parameters == signature(wrapper).parameters
    assert signature(wrapper).return_annotation is str
    assert signature(wrapped, eval_str=True).return_annotation is int

    _: Callable[[int], str] = wrapper
