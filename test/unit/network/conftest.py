# coding: utf-8

from __future__ import unicode_literals, absolute_import

import pytest


@pytest.fixture(params=('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'))
def http_verb(request):
    return request.param
