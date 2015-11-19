# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .network_interface import NetworkResponse


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
