# coding: utf-8

from __future__ import unicode_literals, absolute_import

from functools import update_wrapper, wraps

from ..object.cloneable import Cloneable


def api_call(method):
    """
    Designates the decorated method as one that makes a Box API call.
    The decorated method can then accept a new keyword argument `extra_network_parameters`,
    a dictionary of key-value pairs to be passed to the network layer for API
    calls made by the method.

    The decorated method must belong to a subclass of `Cloneable` as using this
    decorator and then passing a `extra_network_parameters` parameter to the method will cause
    the object's clone method to be called.

    :param method:
        The method to decorate.
    :type method:
        `callable`
    :return:
        A wrapped method that can pass extra request data to the network layer.
    :rtype:
        :class:`APICallWrapper`
    """
    return APICallWrapper(method)


class APICallWrapper(object):

    def __init__(self, func_that_makes_an_api_call):
        super(APICallWrapper, self).__init__()
        self._func_that_makes_an_api_call = func_that_makes_an_api_call
        self.__name__ = func_that_makes_an_api_call.__name__
        update_wrapper(self, func_that_makes_an_api_call)

    def __call__(self, cloneable_instance, *args, **kwargs):
        return self.__get__(cloneable_instance, type(cloneable_instance))(*args, **kwargs)

    def __get__(self, _instance, owner):
        # `APICallWrapper` is imitating a function. For native functions,
        # ```func.__get__(None, cls)``` always returns `func`.
        if _instance is None:
            return self

        if isinstance(owner, type) and not issubclass(owner, Cloneable):
            raise TypeError(
                "descriptor {name!r} must be owned by a 'Cloneable' subclass, not {owner.__name__}"
                .format(name=self.__name__, owner=owner)
            )
        expected_type = owner or Cloneable
        if not isinstance(_instance, expected_type):
            raise TypeError(
                "descriptor {name!r} for {expected_type.__name__!r} objects doesn't apply to {instance.__class__.__name__!r} object"
                .format(name=self.__name__, expected_type=expected_type, instance=_instance)
            )

        @wraps(self._func_that_makes_an_api_call)
        def call(instance, *args, **kwargs):
            extra_network_parameters = kwargs.pop('extra_network_parameters', None)
            if extra_network_parameters:
                # If extra_network_parameters is specified, then clone the instance, and specify the parameters
                # as the defaults to be used.
                instance = instance.clone(instance.session.with_default_network_request_kwargs(extra_network_parameters))

            method = self._func_that_makes_an_api_call.__get__(instance, owner)
            return method(*args, **kwargs)

        # Since the caller passed a non-`None` instance to `__get__()`, they
        # want a bound method back, not an unbound function. Thus, we must bind
        # `call()` to `_instance` and then return that bound method.
        return call.__get__(_instance, owner)
