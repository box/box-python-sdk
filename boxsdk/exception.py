# coding: utf-8
from typing import Optional

import attr

from .network.network_interface import NetworkResponse
from .util.log import sanitize_dictionary


class BoxException(Exception):
    """
    Base class exception for all errors raised from the SDK.
    """
    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'<{self.__class__.__name__}>'


class BoxValueError(ValueError):
    """
    Exception raise by SDK value errors
    """


class BoxNetworkException(BoxException):
    """
    Exception raised from the network layer.
    """


@attr.s(repr=True, slots=True, frozen=True)
class BoxAPIException(BoxException):
    """
    Exception raised from the box session layer.

    :param status:
        HTTP status code of the failed response
    :param code:
        The 'code' field of the failed response
    :param message:
        A message to associate with the exception, e.g. 'message' field of the json in the failed response
    :param request_id:
        The 'request_id' field of the json in the failed response
    :param headers:
        The HTTP headers in the failed response
    :param url:
        The url which raised the exception
    :param method:
        The HTTP verb used to make the request.
    :param context_info:
        The context_info returned in the failed response.
    :param network_response:
        The failed response
    """
    status: int = attr.ib()
    code: Optional[str] = attr.ib(default=None)
    message: Optional[str] = attr.ib(default=None)
    request_id: Optional[str] = attr.ib(default=None)
    headers: dict = attr.ib(default=None, hash=False)
    url: str = attr.ib(default=None)
    method: str = attr.ib(default=None)
    context_info: Optional[dict] = attr.ib(default=None)
    network_response: 'NetworkResponse' = attr.ib(default=None, repr=False)

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
    :param message:
        A message to associate with the exception, e.g. HTTP content of the auth response
    :param url:
        The url which raised the exception
    :param method:
        The HTTP verb used to make the request.
    :param network_response:
        The network response for the request.
    :param code:
        The 'code' field of the failed response
    """
    status: int = attr.ib()
    message: str = attr.ib(default=None)
    url: str = attr.ib(default=None)
    method: str = attr.ib(default=None)
    network_response: NetworkResponse = attr.ib(default=None, repr=False)
    code: Optional[str] = attr.ib(default=None)

    def __str__(self):
        # pylint:disable=no-member
        if self.network_response:
            headers = sanitize_dictionary(self.network_response.headers)
        # pylint:enable=no-member
        else:
            headers = 'N/A'
        return f'\nMessage: {self.message}\nStatus: {self.status}\nURL: {self.url}\nMethod: {self.method}' \
               f'\nHeaders: {headers}'


__all__ = list(map(str, ['BoxException', 'BoxAPIException', 'BoxOAuthException', 'BoxNetworkException']))
