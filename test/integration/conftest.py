# coding: utf-8

from __future__ import unicode_literals
import json
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


@pytest.fixture(scope='session')
def generic_successful_response():
    mock_network_response = Mock(Response)
    content = '{"message": "success"}'
    mock_network_response.content = content.encode('utf-8')
    mock_network_response.status_code = 200
    mock_network_response.ok = True
    mock_network_response.raw = Mock()
    mock_network_response.json.return_value = json.loads(content)
    return mock_network_response


@pytest.fixture(scope='session')
def successful_token_mock():
    return Mock(Response)


@pytest.fixture(scope='session')
def unauthorized_response():
    res = Mock(Response)
    res.content = b''
    res.status_code = 401
    res.ok = False
    return res
