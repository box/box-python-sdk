# coding: utf-8

from __future__ import unicode_literals, absolute_import

from functools import update_wrapper


def api_call(func):
    """
    Designates the decorated method as one that makes a Box API call.
    The decorated method can then accept a new keyword argument `request_data`,
    a dictionary of key-value pairs to be passed to the network layer for API
    calls made by the method.

    :param func:
        The method to decorate.
    :type func:
        `callable`
    :return:
        A wrapped method that can pass extra request data to the network layer.
    :rtype:
        :class:`APICallWrapper`
    """
    wrapper = APICallWrapper(func)
    update_wrapper(wrapper, func)
    return wrapper


class APICallWrapper(object):

    def __init__(self, func_that_makes_an_api_call):
        super(APICallWrapper, self).__init__()
        self._func_that_makes_an_api_call = func_that_makes_an_api_call

    def __get__(self, _instance, owner):
        def call(*args, **kwargs):
            instance = _instance
            if instance is None:
                # If this is being called as an unbound method, the instance is the first arg.
                if owner is not None and len(args) > 0 and isinstance(args[0], owner):
                    instance = args[0]
                    args = args[1:]
                else:
                    raise AttributeError
            request_data = kwargs.pop('request_data', {})
            if request_data:
                # If request_data is specified, then clone the instance, and specify it as the default network args.
                # pylint: disable=protected-access
                instance = instance.clone(instance._session.with_default_network_request_kwargs(**request_data))
                # pylint: enable=protected-access
            response = self._func_that_makes_an_api_call(instance, *args, **kwargs)
            return response
        return call
