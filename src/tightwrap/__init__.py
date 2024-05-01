import sys

from functools import wraps as functools_wraps
from inspect import Signature, signature
from typing import Any, Callable, TypeVar

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
R = TypeVar("R")


def wraps(wrapped: Callable[P, Any]) -> Callable[[Callable[..., R]], Callable[P, R]]:
    """Apply `functools.wraps`"""

    def wrapper(fn):
        wrapper_return = signature(fn, eval_str=True).return_annotation
        res = functools_wraps(wrapped)(fn)

        orig_sig = signature(wrapped, eval_str=True)
        if orig_sig.return_annotation != wrapper_return:
            # We do a little rewriting.
            new_sig = Signature(None, return_annotation=wrapper_return)
            new_sig._parameters = orig_sig._parameters
            res.__signature__ = new_sig

        return res

    return wrapper
