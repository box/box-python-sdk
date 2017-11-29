# coding: utf-8

from __future__ import unicode_literals, absolute_import

import attr


@attr.s(slots=True)
class BoxRequest(object):
    """Represents a Box API request"""
    url = attr.ib()
    method = attr.ib(default='GET')
    headers = attr.ib(default=attr.Factory(dict))
    auto_session_renewal = attr.ib(default=True)
    expect_json_response = attr.ib(default=True)
