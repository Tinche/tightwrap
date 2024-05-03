from __future__ import annotations

from typing import Any, Callable

from tightwrap import _get_resolved_signature  # pyright: ignore[reportPrivateUsage]
from tightwrap import wraps


def test_wraps() -> None:
    """Wraps works."""

    def wrapped(a: int) -> int:
        return a + 1

    @wraps(wrapped)
    def wrapper(a: int) -> int:
        return wrapped(a)

    assert wrapper(3) == 4
    assert _get_resolved_signature(wrapped) == _get_resolved_signature(wrapper)

    _: Callable[[int], int] = wrapper


def test_wraps_different_return() -> None:
    def wrapped(a: int) -> int:
        return a + 1

    @wraps(wrapped)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        return str(wrapped(*args, **kwargs))

    wrapped_signature = _get_resolved_signature(wrapped)
    wrapper_signature = _get_resolved_signature(wrapper)

    assert wrapper(3) == "4"
    assert wrapped_signature.parameters == wrapper_signature.parameters
    assert wrapper_signature.return_annotation is str
    assert wrapped_signature.return_annotation is int

    _: Callable[[int], str] = wrapper
