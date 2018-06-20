# coding: utf-8

from __future__ import unicode_literals, absolute_import

import attr

from ..util.log import sanitize_dictionary


@attr.s(slots=True)
class BoxRequest(object):
    """Represents a Box API request.

    :param url:                     The URL being requested.
    :type url:                      `unicode`
    :param method:                  The HTTP method to use for the request.
    :type method:                   `unicode` or None
    :param headers:                 HTTP headers to include with the request.
    :type headers:                  `dict` or None
    :param auto_session_renewal:    Whether or not the session can be automatically renewed if the request fails.
    :type auto_session_renewal:     `bool` or None
    :param expect_json_response:    Whether or not the API response must be JSON.
    :type expect_json_response:     `bool` or None
    """
    url = attr.ib()
    method = attr.ib(default='GET')
    headers = attr.ib(default=attr.Factory(dict))
    auto_session_renewal = attr.ib(default=True)
    expect_json_response = attr.ib(default=True)

    def __repr__(self):
        return '<BoxRequest for {self.method} {self.url} with headers {headers}'.format(
            self=self,
            headers=sanitize_dictionary(self.headers),
        )
