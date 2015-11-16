# coding: utf-8

from __future__ import unicode_literals, absolute_import
from functools import update_wrapper


def api_response(func):
    """
    Designates the decorated function as one that makes a Box API call.
    The decorated function can then have a translator specified that can
    take action on the reponse once it's available.

    :param func:
        The function to decorate.
    :type func:
        `callable`
    :return:
        A wrapped function that can specify a translator function.
    :rtype:
        :class:`APIResponseWrapper`
    """
    wrapper = APIResponseWrapper(func)
    update_wrapper(wrapper, func)
    return wrapper


class APIResponseWrapper(object):
    def _response_translator(self, *args):
        """
        Calls response translator.
        If a translator has not been specified, returns the last provided positional arg (which is the API response).
        """
        if self._translator_func is not None:
            return self._translator_func(*args)
        return args[-1]

    def __init__(self, func_that_returns_api_response, translator_func=None):
        super(APIResponseWrapper, self).__init__()
        self._func_that_returns_api_response = func_that_returns_api_response
        self._translator_func = translator_func

    def translator(self, translator_func):
        """
        Specifies a translator function for the API response.
        This function will be called with the API response.
        """
        self._translator_func = translator_func
        return self.__class__(self._func_that_returns_api_response, translator_func)

    def __get__(self, instance, owner):
        def call(*args, **kwargs):
            # If this is being called as an instance method, then pass the instance as the first arg (self)
            if instance is not None:
                response = self._func_that_returns_api_response(instance, *args, **kwargs)
            else:
                response = self._func_that_returns_api_response(*args, **kwargs)
            if response is not None:
                # Make the original call's args and kwargs available to the translator function
                response.args = args
                response.kwargs = kwargs
            if not isinstance(response, tuple):
                # Pass the instance as the self arg, if specified.
                response = [response]
                if instance is not None:
                    response.insert(0, instance)
                elif owner is not None and len(args) > 0 and isinstance(args[0], owner):
                    response.insert(0, args[0])
            return self._response_translator(*response)
        return call
