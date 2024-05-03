import sys
from functools import wraps as functools_wraps
from inspect import Signature
from typing import Any, Callable, TypeVar, cast

from ._backported import eval_if_necessary, get_annotations

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
R = TypeVar("R")


def _get_resolved_signature(fn: Callable[..., Any]) -> Signature:
    signature = Signature.from_callable(fn)
    evaluated_annotations, fn_globals, fn_locals = get_annotations(fn)

    for name, parameter in signature.parameters.items():
        setattr(parameter, "_annotation", evaluated_annotations[name])

    new_return_annotation = eval_if_necessary(
        signature.return_annotation, fn_globals, fn_locals
    )
    setattr(signature, "_return_annotation", new_return_annotation)

    return signature


def wraps(wrapped: Callable[P, Any]) -> Callable[[Callable[..., R]], Callable[P, R]]:
    """Apply `functools.wraps`"""

    def wrapper(fn: Callable[..., R]) -> Callable[P, R]:
        wrapper_return = _get_resolved_signature(fn).return_annotation
        res = functools_wraps(wrapped)(fn)

        orig_sig = _get_resolved_signature(wrapped)

        if orig_sig.return_annotation != wrapper_return:
            # We do a little rewriting.
            new_sig = Signature(None, return_annotation=wrapper_return)
            setattr(new_sig, "_parameters", orig_sig.parameters)
            setattr(res, "__signature__", new_sig)

        return cast(Callable[P, R], res)

    return wrapper
