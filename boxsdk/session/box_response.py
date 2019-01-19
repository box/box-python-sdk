# coding: utf-8

from __future__ import unicode_literals, absolute_import


class BoxResponse(object):
    """Represents a response to a Box API request."""

    def __init__(self, network_response):
        self._network_response = network_response

    def json(self):
        """Return the parsed JSON response.

        :rtype:
            `dict` or `list` or `str` or `int` or `float`
        """
        return self._network_response.json()

    @property
    def content(self):
        """Return the content of the response body.

        :rtype:
            varies
        """
        return self._network_response.content

    @property
    def ok(self):
        """Return whether or not the request was successful.

        :rtype:
            `bool`
        """
        # pylint:disable=invalid-name
        return self._network_response.ok

    @property
    def status_code(self):
        """Return the HTTP status code of the response.

        :rtype:
            `int`
        """
        return self._network_response.status_code

    @property
    def headers(self):
        """
        Get the response headers.

        :rtype:
            `dict`
        """
        return self._network_response.headers

    @property
    def network_response(self):
        """Return the underlying network response.

        :rtype:
            :class:`NetworkResponse`
        """
        return self._network_response

    def __repr__(self):
        return '<Box Response[{status_code}]>'.format(status_code=self.status_code)
