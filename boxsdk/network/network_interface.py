# coding: utf-8

from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod, abstractproperty
from six import add_metaclass


@add_metaclass(ABCMeta)
class Network(object):
    """
    Abstract base class specifying the interface of the network layer.
    """

    @abstractmethod
    def request(self, method, url, access_token, **kwargs):
        """
        Make a network request to the given url with the given method.

        :param method:
            The HTTP verb that should be used to make the request.
        :type method:
            `unicode`
        :param url:
            The URL for the request.
        :type url:
            `unicode`
        :param access_token:
            The OAuth2 access token used to authorize the request.
        :type access_token:
            `unicode`
        :rtype:   :class:`NetworkResponse`
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def retry_after(self, delay, request_method, *args, **kwargs):
        """
        Make a network request after a given delay.

        :param delay:
            How long until the request should be executed.
        :type delay:
            `float`
        :param request_method:
            A callable that will execute the request.
        :type request_method:
            `callable`
        :rtype:   :class:`NetworkResponse`
        """
        raise NotImplementedError  # pragma: no cover

    @property
    def network_response_constructor(self):
        """The constructor to use for creating NetworkResponse instances.

        This is not implemented by default, and is not a required part of the
        interface.

        It is recommended that implementations of `request()` call this to
        construct their responses, rather than hard-coding the construction.
        That way, subclasses of the implementation can easily extend the
        construction of :class:`NetworkResponse` instances, by overriding this
        property, instead of needing to override `request()`.

        :return:
            A callable that returns an instance of :class:`NetworkResponse`.
            Most commonly, this will be a subclass of :class:`NetworkResponse`.
        :rtype:   `type` or `callable`
        """
        return NetworkResponse


@add_metaclass(ABCMeta)
class NetworkResponse(object):
    """Abstract base class specifying the interface for a network response."""

    @abstractmethod
    def json(self):
        """Return the parsed JSON response.

        :rtype:
            `dict` or `list` or `str` or `int` or `float`
        """
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def content(self):
        """Return the content of the response body.

        :rtype:
            varies
        """
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def status_code(self):
        """Return the HTTP status code of the response.

        :rtype:
            `int`
        """
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def ok(self):
        """Return whether or not the request was successful.

        :rtype:
            `bool`
        """
        # pylint:disable=invalid-name
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def headers(self):
        """Return the response headers.

        :rtype:
            `dict`
        """
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def response_as_stream(self):
        """Return a stream containing the raw network response.

        :rtype:
            `stream`
        """
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def access_token_used(self):
        """Return the access token used to make the request.

        :rtype:
            `unicode`
        """
        raise NotImplementedError  # pragma: no cover
