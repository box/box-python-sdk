import warnings


def deprecated(message):
    def deprecated_decorator(func):
        def deprecated_func(*args, **kwargs):
            warnings.simplefilter('default', DeprecationWarning)
            warnings.warn(f'{func.__name__} is a deprecated function. {message}',
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)
        return deprecated_func
    return deprecated_decorator
