# coding: utf-8

from __future__ import unicode_literals
from six import PY2


class BoxException(Exception):
    """
    Base class exception for all errors raised from the SDK.
    """
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()


class BoxNetworkException(BoxException):
    """
    Exception raised from the network layer.
    """
    pass


class BoxAPIException(BoxException):
    """
    Exception raised from the box session layer.
    """
    def __init__(self, status, code=None, message=None, request_id=None, headers=None, url=None, method=None):
        super(BoxAPIException, self).__init__()
        self._status = status
        self._code = code
        self._message = message
        self._request_id = request_id
        self._headers = headers
        self._url = url
        self._method = method

    def __unicode__(self):
        return '\nMessage: {0}\nStatus: {1}\nCode: {2}\nRequest id: {3}\nHeaders: {4}\nURL: {5}\nMethod: {6}'.format(
            self._message,
            self._status,
            self._code,
            self._request_id,
            self._headers,
            self._url,
            self._method,
        )

    @property
    def status(self):
        """
        The status code of the network response that is responsible for the exception.
        :rtype: `int`
        """
        return self._status

    @property
    def code(self):
        """
        The explanation of the status code of the network response that is responsible for the exception.
        :rtype: `int`
        """
        return self._code

    @property
    def message(self):
        return self._message

    @property
    def request_id(self):
        """
        The id the network request that is responsible for the exception.
        :rtype: `unicode`
        """
        return self._request_id

    @property
    def url(self):
        """
        The URL of the network request that is responsible for the exception.
        :rtype: `unicode`
        """
        return self._url

    @property
    def method(self):
        """
        The HTTP verb of the request that is responsible for the exception.
        :rtype: `unicode`
        """
        return self._method


class BoxOAuthException(BoxException):
    """
    Exception raised during auth.
    """
    def __init__(self, status, message=None, url=None, method=None):
        super(BoxOAuthException, self).__init__()
        self._status = status
        self._message = message
        self._url = url
        self._method = method

    def __unicode__(self):
        return '\nMessage: {0}\nStatus: {1}\nURL: {2}\nMethod: {3}'.format(
            self._message,
            self._status,
            self._url,
            self._method,
        )
