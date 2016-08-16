# coding: utf-8

from __future__ import unicode_literals, absolute_import

from functools import update_wrapper, wraps


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
        update_wrapper(self, func_that_makes_an_api_call)

    def __get__(self, _instance, owner):
        @wraps(self._func_that_makes_an_api_call)
        def call(*args, **kwargs):
            instance = _instance
            if instance is None:
                # If this is being called as an unbound method, the instance is the first arg.
                if owner is not None and len(args) > 0 and isinstance(args[0], owner):
                    instance = args[0]
                    args = args[1:]
                else:
                    raise TypeError
            extra_network_parameters = kwargs.pop('extra_network_parameters', None)
            if extra_network_parameters:
                # If extra_network_parameters is specified, then clone the instance, and specify the parameters
                # as the defaults to be used.
                # pylint: disable=protected-access
                instance = instance.clone(instance._session.with_default_network_request_kwargs(extra_network_parameters))
                # pylint: enable=protected-access
            response = self._func_that_makes_an_api_call(instance, *args, **kwargs)
            return response
        return call
