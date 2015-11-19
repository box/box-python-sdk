# coding: utf-8

from __future__ import unicode_literals, absolute_import
from aplus import Promise
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

    def _call_translator(self, instance, response, args, kwargs):
        """
        Call the translator function on the instance with the Box API response.
        Make the original call's args and kwargs available to the translator function as attributes of response.
        """
        response_args = [instance]
        if isinstance(response, Promise):
            def then(value):
                if value is not None:
                    value.args = args
                    value.kwargs = kwargs
                response_args.append(value)
                return self._response_translator(*response_args)
            return response.then(then)
        else:
            if response is not None:
                response.args = args
                response.kwargs = kwargs
            response_args.append(response)
            return self._response_translator(*response_args)

    def __get__(self, _instance, owner):
        def call(*args, **kwargs):
            instance = _instance
            # If this is being called as a bound method, then pass the instance as the first arg (self)
            if instance is not None:
                response = self._func_that_returns_api_response(instance, *args, **kwargs)
            else:
                response = self._func_that_returns_api_response(*args, **kwargs)
            if instance is None:
                # If called as an unbound method, then the instance is the first arg.
                if owner is not None and len(args) > 0 and isinstance(args[0], owner):
                    instance = args[0]
                else:
                    raise AttributeError
            return_value = self._call_translator(instance, response, args, kwargs)
            if isinstance(return_value, Promise) and not instance._session.is_async:  # pylint:disable=protected-access
                return_value = return_value.get()
            return return_value
        return call


def promisify(value):
    return value if isinstance(value, Promise) else Promise.fulfilled(value)
