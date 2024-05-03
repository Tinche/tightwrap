import functools
import sys
from types import GetSetDescriptorType, ModuleType
from typing import Any, Callable, Dict, Tuple, cast


Annotations = Dict[str, Any]
Globals = Dict[str, Any]
Locals = Dict[str, Any]
GetAnnotationsResults = Tuple[Annotations, Globals, Locals]


def eval_if_necessary(source: Any, globals: Globals, locals: Locals) -> Any:
    if not isinstance(source, str):
        return source

    return eval(source, globals, locals)


def get_annotations(obj: Callable[..., Any]) -> GetAnnotationsResults:
    # Copied from https://github.com/python/cpython/blob/3.12/Lib/inspect.py#L176-L288

    obj_globals: Any
    obj_locals: Any
    unwrap: Any

    if isinstance(obj, type):
        obj_dict = getattr(obj, "__dict__", None)

        if obj_dict and hasattr(obj_dict, "get"):
            ann = obj_dict.get("__annotations__", None)
            if isinstance(ann, GetSetDescriptorType):
                ann = None
        else:
            ann = None

        obj_globals = None
        module_name = getattr(obj, "__module__", None)

        if module_name:
            module = sys.modules.get(module_name, None)

            if module:
                obj_globals = getattr(module, "__dict__", None)

        obj_locals = dict(vars(obj))
        unwrap = obj

    elif isinstance(obj, ModuleType):
        ann = getattr(obj, "__annotations__", None)
        obj_globals = getattr(obj, "__dict__")
        obj_locals = None
        unwrap = None

    elif callable(obj):
        ann = getattr(obj, "__annotations__", None)
        obj_globals = getattr(obj, "__globals__", None)
        obj_locals = None
        unwrap = obj

    else:
        raise TypeError(f"{obj!r} is not a module, class, or callable.")

    if ann is None:
        return cast(GetAnnotationsResults, ({}, obj_globals, obj_locals))

    if not isinstance(ann, dict):
        raise ValueError(f"{obj!r}.__annotations__ is neither a dict nor None")

    if not ann:
        return cast(GetAnnotationsResults, ({}, obj_globals, obj_locals))

    if unwrap is not None:
        while True:
            if hasattr(unwrap, "__wrapped__"):
                unwrap = unwrap.__wrapped__
                continue
            if isinstance(unwrap, functools.partial):
                unwrap = unwrap.func
                continue
            break
        if hasattr(unwrap, "__globals__"):
            obj_globals = unwrap.__globals__

    return_value = {
        key: eval_if_necessary(value, obj_globals, obj_locals)
        for key, value in cast(Dict[str, Any], ann).items()
    }

    return cast(GetAnnotationsResults, (return_value, obj_globals, obj_locals))
