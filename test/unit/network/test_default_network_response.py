# coding: utf-8

from __future__ import unicode_literals
from mock import Mock
from requests import Response
from boxsdk.network.default_network_response import DefaultNetworkResponse


def test_default_network_response_properties_pass_through_to_session_response_properties(access_token):
    mock_session_response = Mock(Response)
    mock_session_response.status_code = 200
    mock_session_response.headers = {}
    mock_session_response.raw = Mock()
    network_reponse = DefaultNetworkResponse(mock_session_response, access_token)
    assert network_reponse.json() == mock_session_response.json()
    assert network_reponse.content == mock_session_response.content
    assert network_reponse.ok == mock_session_response.ok
    assert network_reponse.status_code == mock_session_response.status_code
    assert network_reponse.headers == mock_session_response.headers
    assert network_reponse.response_as_stream == mock_session_response.raw
    assert network_reponse.access_token_used == access_token
