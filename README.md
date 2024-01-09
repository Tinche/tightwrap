# tightwrap

_tightwrap_ (pronounced _typed wrap_) is a drop-in replacement for [`functools.wraps`](https://docs.python.org/3/library/functools.html#functools.wraps) that works with static typing.
_tightwrap_ is very small, so if you don't want to add a dependency to it just [vendor this file](https://github.com/Tinche/tightwrap/blob/main/src/tightwrap/__init__.py).

`functools.wraps` is very commonly used to adapt runtime function signatures when wrapping functions, but it doesn't work well with static typing tools.
`tightwrap.wraps` has the same interface and you should use it instead:

```python
from tightwrap import wraps

def function(a: int) -> int:
    return a + 1

@wraps(function)
def wrapping(*args, **kwargs) -> int:
    return function(*args, **kwargs)

reveal_type(wrapping)  # Revealed type is "def (a: builtins.int) -> builtins.int"

wrapping("a string")  # error: Argument 1 to "wrapping" has incompatible type "str"; expected "int"
```

_tightwrap_ applies `functools.wraps` under the hood so runtime inspection continues to work.

If your wrapper has a different return type than the function you're wrapping,
`tightwrap.wraps` will use the _wrapper_ return type and make the runtime signature return type match.

For comparison, when using `functools.wraps` the current version of Mypy reports:

```python
from functools import wraps

def function(a: int) -> int:
    return a + 1

@wraps(function)
def wrapping(*args, **kwargs) -> int:
    return function(*args, **kwargs)

reveal_type(wrapping)  # Revealed type is "def (*args: Any, **kwargs: Any) -> builtins.int"

wrapping("a string")  # No type error, blows up at runtime.
```

## Changelog

### 24.1.0 (UNRELEASED)

- Initial version.