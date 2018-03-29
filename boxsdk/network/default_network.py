# coding: utf-8

from __future__ import unicode_literals

import time

import requests

from .network_interface import Network, NetworkResponse


class DefaultNetwork(Network):
    """Implementation of the network interface using the requests library."""

    def __init__(self):
        super(DefaultNetwork, self).__init__()
        self._session = requests.Session()

    def request(self, method, url, access_token, **kwargs):
        """Base class override.
        Make a network request using a requests.Session.
        """
        # pylint:disable=abstract-class-instantiated
        return self.network_response_constructor(
            request_response=self._session.request(method, url, **kwargs),
            access_token_used=access_token,
        )

    def retry_after(self, delay, request_method, *args, **kwargs):
        """Base class override.
        Retry after sleeping for delay seconds.
        """
        time.sleep(delay)
        return request_method(*args, **kwargs)

    @property
    def network_response_constructor(self):
        """Baseclass override.

        A callable that accepts `request_response` and `access_token_used`
        keyword arguments for the :class:`DefaultNetworkResponse` constructor,
        and returns an instance of :class:`DefaultNetworkResponse`.
        """
        return DefaultNetworkResponse


class DefaultNetworkResponse(NetworkResponse):
    """Implementation of the network interface using the requests library."""

    def __init__(self, request_response, access_token_used):
        self._request_response = request_response
        self._access_token_used = access_token_used

    def json(self):
        """Base class override."""
        return self._request_response.json()

    @property
    def content(self):
        """Base class override."""
        return self._request_response.content

    @property
    def status_code(self):
        """Base class override."""
        return self._request_response.status_code

    @property
    def ok(self):
        """Base class override."""
        # pylint:disable=invalid-name
        return self._request_response.ok

    @property
    def headers(self):
        """Base class override."""
        return self._request_response.headers

    @property
    def response_as_stream(self):
        """Base class override."""
        return self._request_response.raw

    @property
    def access_token_used(self):
        """Base class override."""
        return self._access_token_used

    @property
    def request_response(self):
        """
        The response returned from the Requests library.

        :rtype: `Response`
        """
        return self._request_response
