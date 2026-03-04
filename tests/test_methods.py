from __future__ import annotations

from tightwrap import (
    _get_resolved_signature,
    wraps,
)


def test_method_wraps_basic() -> None:
    """Basic method wrapping works at runtime."""

    class MyClass:
        @staticmethod
        def _inner(a: int, b: str) -> str:
            return f"{a}: {b}"

        @wraps(_inner)
        def outer(self, a: int, b: str) -> str:
            return self._inner(a, b)

    obj = MyClass()
    assert obj.outer(42, "hello") == "42: hello"

    # Verify functools.wraps metadata is preserved
    assert MyClass.outer.__name__ == "_inner"
    assert hasattr(MyClass.outer, "__wrapped__")


def test_method_wraps_different_return() -> None:
    """Method wrapping with different return type."""

    class MyClass:
        @staticmethod
        def _inner(a: int) -> int:
            return a + 1

        @wraps(_inner)
        def outer(self, a: int) -> str:
            return str(self._inner(a))

    obj = MyClass()
    assert obj.outer(3) == "4"


def test_method_signature() -> None:
    """Method signature is correctly resolved (without self)."""

    class MyClass:
        @staticmethod
        def _inner(a: int, b: str) -> str:
            return f"{a}: {b}"

        @wraps(_inner)
        def outer(self, a: int, b: str) -> str:
            return self._inner(a, b)

    # The resolved signature should match the inner function
    inner_sig = _get_resolved_signature(MyClass._inner)
    outer_sig = _get_resolved_signature(MyClass.outer)

    assert inner_sig.parameters == outer_sig.parameters
