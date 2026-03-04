import sys
from functools import wraps as functools_wraps
from inspect import Signature, _empty
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from ._backported import eval_if_necessary, get_annotations

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
R = TypeVar("R")


if TYPE_CHECKING:
    from typing import Generic, overload

    class MethodWrapper(Generic[P, R]):
        """Type-only descriptor for correct method typing.

        This allows type checkers to understand that wrapped methods
        should preserve their parameter types while handling `self` correctly.
        """

        @overload
        def __get__(self, obj: None, objtype: type[T]) -> Callable[P, R]: ...

        @overload
        def __get__(self, obj: T, objtype: type[T] | None = None) -> Callable[P, R]: ...

        def __get__(
            self, obj: Any, objtype: type[Any] | None = None
        ) -> Callable[P, R]: ...

        def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...


def _get_resolved_signature(fn: Callable[..., Any]) -> Signature:
    signature = Signature.from_callable(fn)
    evaluated_annotations, fn_globals, fn_locals = get_annotations(fn)

    for name, parameter in signature.parameters.items():
        parameter._annotation = evaluated_annotations.get(name, _empty)  # type: ignore

    new_return_annotation = eval_if_necessary(
        signature.return_annotation, fn_globals, fn_locals
    )
    signature._return_annotation = new_return_annotation  # type: ignore

    return signature


if TYPE_CHECKING:

    def wraps(
        wrapped: Callable[P, Any],
    ) -> Callable[[Callable[..., R]], MethodWrapper[P, R]]:
        """Apply `functools.wraps`. Works on functions and methods."""
        ...

else:

    def wraps(wrapped):
        def wrapper(fn):
            wrapper_return = _get_resolved_signature(fn).return_annotation
            res = functools_wraps(wrapped)(fn)

            orig_sig = _get_resolved_signature(wrapped)

            if orig_sig.return_annotation != wrapper_return:
                # We do a little rewriting.
                new_sig = Signature(None, return_annotation=wrapper_return)
                new_sig._parameters = orig_sig.parameters  # type: ignore
                res.__signature__ = new_sig  # type: ignore

            return res

        return wrapper
