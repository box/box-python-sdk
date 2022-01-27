import warnings
from typing import Callable, Any


def deprecated(message: str):
    def deprecated_decorator(func: Callable) -> Any:
        def deprecated_func(*args, **kwargs):
            warnings.simplefilter('default', DeprecationWarning)
            warnings.warn(f'{func.__name__} is a deprecated function. {message}',
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)
        return deprecated_func
    return deprecated_decorator


def deprecated_param(*, name: str, position: int, message: str):
    def deprecated_decorator(func: Callable) -> Any:
        def deprecated_func(*args, **kwargs):
            if len(args) >= position + 1 or name in kwargs:
                warnings.simplefilter('default', DeprecationWarning)
                warnings.warn(
                    f'{func.__name__} function parameter `{name}` at position {position} is deprecated. {message}',
                    category=DeprecationWarning,
                    stacklevel=2
                )
            return func(*args, **kwargs)
        return deprecated_func
    return deprecated_decorator
