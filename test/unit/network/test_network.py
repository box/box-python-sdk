# coding: utf-8

from __future__ import unicode_literals
from mock import DEFAULT, Mock, patch
import pytest
from requests import Response, Session
from boxsdk.network.default_network import DefaultNetworkResponse, DefaultNetwork


@pytest.fixture()
def mock_request(monkeypatch):
    mock_session_factory = Mock()
    mock_session_factory.return_value = session = Mock(Session, request=Mock())
    monkeypatch.setattr('requests.Session', mock_session_factory)
    return session.request


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


def test_default_network_request(mock_request, http_verb, test_url, access_token, generic_successful_response):
    # pylint:disable=redefined-outer-name
    default_network = DefaultNetwork()
    mock_request.return_value = generic_successful_response
    response = default_network.request(http_verb, test_url, access_token, custom_kwarg='test')
    mock_request.assert_called_once_with(http_verb, test_url, custom_kwarg='test')
    assert response.response_as_stream == generic_successful_response.raw
    assert response.access_token_used == access_token


@pytest.mark.parametrize('delay', (0, 1))
def test_default_network_retry_after_sleeps(delay):
    default_network = DefaultNetwork()
    retry_call = Mock()
    mock_sleep = Mock()
    with patch('boxsdk.network.default_network.time.sleep', mock_sleep):
        default_network.retry_after(delay, retry_call, DEFAULT, kwarg=DEFAULT)
    mock_sleep.assert_called_once_with(delay)
    retry_call.assert_called_once_with(DEFAULT, kwarg=DEFAULT)
