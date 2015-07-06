# coding: utf-8

from __future__ import unicode_literals
import pytest
from boxsdk.util.shared_link import get_shared_link_header


@pytest.fixture(params=('mock_shared_link', 'https://app.box.com/s/q2i1024dvguiads6mzj2avsq9hmz43du'))
def shared_link(request):
    return request.param


@pytest.fixture(params=(None, 'shared_link_password'))
def password(request):
    return request.param


def test_get_shared_link_header(shared_link, password):
    # pylint:disable=redefined-outer-name
    header = get_shared_link_header(shared_link, password)
    assert 'BoxApi' in header
    assert shared_link in header['BoxApi']
    if password is not None:
        assert password in header['BoxApi']
