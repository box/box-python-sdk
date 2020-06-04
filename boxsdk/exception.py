# coding: utf-8

from __future__ import unicode_literals

import attr

from .network.network_interface import NetworkResponse
from .util.log import sanitize_dictionary


class BoxException(Exception):
    """
    Base class exception for all errors raised from the SDK.
    """
    def __str__(self):
        return '{}'.format(self.__class__.__name__)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


class BoxValueError(ValueError):
    """
    Exception raise by SDK value errors
    """


class BoxNetworkException(BoxException):
    """
    Exception raised from the network layer.
    """
    pass


@attr.s(repr=True, slots=True, frozen=True)
class BoxAPIException(BoxException):
    """
    Exception raised from the box session layer.

    :param status:
        HTTP status code of the failed response
    :type status:
        `int`
    :param code:
        The 'code' field of the failed response
    :type code:
        `unicode` or None
    :param message:
        A message to associate with the exception, e.g. 'message' field of the json in the failed response
    :type message:
        `unicode` or None
    :param request_id:
        The 'request_id' field of the json in the failed response
    :type request_id:
        `unicode` or None
    :param headers:
        The HTTP headers in the failed response
    :type headers:
        `dict`
    :param url:
        The url which raised the exception
    :type url:
        `unicode`
    :param method:
        The HTTP verb used to make the request.
    :type method:
        `unicode`
    :param context_info:
        The context_info returned in the failed response.
    :type context_info:
        `dict` or None
    :param network_response:
        The failed response
    :type network_response:
        Requests `Response`
    """
    status = attr.ib()
    code = attr.ib(default=None)
    message = attr.ib(default=None)
    request_id = attr.ib(default=None)
    headers = attr.ib(default=None, hash=False)
    url = attr.ib(default=None)
    method = attr.ib(default=None)
    context_info = attr.ib(default=None)
    network_response = attr.ib(default=None, repr=False)

    def __str__(self):
        return '\n'.join((
            'Message: {self.message}',
            'Status: {self.status}',
            'Code: {self.code}',
            'Request ID: {self.request_id}',
            'Headers: {headers}',
            'URL: {self.url}',
            'Method: {self.method}',
            'Context Info: {self.context_info}',
        )).format(self=self, headers=sanitize_dictionary(self.headers))


@attr.s(repr=True, slots=True, frozen=True)
class BoxOAuthException(BoxException):
    """
    Exception raised during auth.

    :param status:
        HTTP status code of the auth response
    :type status:
        `int`
    :param message:
        A message to associate with the exception, e.g. HTTP content of the auth response
    :type message:
        `unicode`
    :param url:
        The url which raised the exception
    :type url:
        `unicode`
    :param method:
        The HTTP verb used to make the request.
    :type method:
        `unicode`
    :param network_response:
        The network response for the request.
    :type network_response:
        :class:`NetworkResponse`
    :param code:
        The 'code' field of the failed response
    :type code:
        `unicode` or None
    """
    status = attr.ib()
    message = attr.ib(default=None)
    url = attr.ib(default=None)
    method = attr.ib(default=None)
    network_response = attr.ib(default=None, repr=False, type=NetworkResponse)
    code = attr.ib(default=None)

    def __str__(self):
        # pylint:disable=no-member
        if self.network_response:
            headers = sanitize_dictionary(self.network_response.headers)
        # pylint:enable=no-member
        else:
            headers = 'N/A'
        return '\nMessage: {0}\nStatus: {1}\nURL: {2}\nMethod: {3}\nHeaders: {4}'.format(
            self.message,
            self.status,
            self.url,
            self.method,
            headers,
        )


__all__ = list(map(str, ['BoxException', 'BoxAPIException', 'BoxOAuthException', 'BoxNetworkException']))
