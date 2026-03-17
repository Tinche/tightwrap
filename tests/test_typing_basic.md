# wraps

## Preserves wrapped argument types

```python
from tightwrap import wraps


def inner(a: int) -> int:
    return a + 1


@wraps(inner)
def wrapped(*args, **kwargs) -> int:
    return inner(*args, **kwargs)


wrapped(1)
wrapped("a string")  # ty-error: [invalid-argument-type]  # mypy-error: [arg-type]
```

## Preserves wrapped method argument types

```python
from tightwrap import wraps


class MyClass:
    @staticmethod
    def _inner(a: int, b: str) -> str:
        return f"{a}: {b}"

    @wraps(_inner)
    def outer(self, *args, **kwargs) -> str:
        return self._inner(*args, **kwargs)


obj = MyClass()
obj.outer(42, "hello")
obj.outer("not an int", "hello")  # ty-error: [invalid-argument-type]  # mypy-error: [arg-type]
```

## Preserves method types when wrapping a function

```python
from tightwrap import wraps


def inner(a: int, b: str) -> str:
    return f"{a}: {b}"


class MyClass:
    @wraps(inner)
    def outer(self, *args, **kwargs) -> str:
        return inner(*args, **kwargs)


obj = MyClass()
obj.outer(42, "hello")
obj.outer("not an int", "hello")  # ty-error: [invalid-argument-type]  # mypy-error: [arg-type]
```
