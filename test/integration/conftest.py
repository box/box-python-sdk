# coding: utf-8

from __future__ import absolute_import, unicode_literals

from mock import Mock
import pytest
from requests import Response

from boxsdk import Client
from boxsdk.auth.oauth2 import OAuth2
from test.integration.mock_network import MockNetwork


@pytest.fixture()
def box_client(box_oauth, mock_box_network):
    # pylint:disable=redefined-outer-name
    return Client(box_oauth, network_layer=mock_box_network)


@pytest.fixture()
def box_oauth(mock_box_network, client_id, client_secret, access_token, refresh_token):
    # pylint:disable=redefined-outer-name
    return OAuth2(
        client_id,
        client_secret,
        network_layer=mock_box_network,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@pytest.fixture()
def mock_box_network():
    return MockNetwork()


@pytest.fixture
def generic_successful_response(generic_successful_request_response):
    return generic_successful_request_response


@pytest.fixture
def successful_token_mock(successful_token_request_response):
    return successful_token_request_response


@pytest.fixture(scope='session')
def unauthorized_response():
    res = Mock(Response)
    res.content = b''
    res.status_code = 401
    res.ok = False
    return res
