# coding: utf-8

from __future__ import absolute_import, unicode_literals

from mock import DEFAULT, Mock, patch
import pytest
from requests import Response

from boxsdk.network.default_network import DefaultNetworkResponse, DefaultNetwork


@pytest.fixture
def make_network_request(make_network_request, request_response, http_verb):
    # pylint:disable=unused-argument
    # Need to list `http_verb`, even though it isn't used in this override,
    # because of <https://github.com/pytest-dev/pytest/issues/1953>.

    def _make_network_request(*args, **kwargs):
        response = make_network_request(*args, **kwargs)
        assert response.request_response is request_response
        return response

    return _make_network_request


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


def test_default_network_request(make_network_request):
    # pylint:disable=redefined-outer-name
    default_network = DefaultNetwork()
    make_network_request(default_network, custom_kwargs='test')


@pytest.mark.parametrize('delay', (0, 1))
def test_default_network_retry_after_sleeps(delay):
    default_network = DefaultNetwork()
    retry_call = Mock()
    mock_sleep = Mock()
    with patch('boxsdk.network.default_network.time.sleep', mock_sleep):
        default_network.retry_after(delay, retry_call, DEFAULT, kwarg=DEFAULT)
    mock_sleep.assert_called_once_with(delay)
    retry_call.assert_called_once_with(DEFAULT, kwarg=DEFAULT)


def test_network_response_constructor(make_network_request):
    assert DefaultNetwork().network_response_constructor is DefaultNetworkResponse

    class DefaultNetworkResponseSubclass(DefaultNetworkResponse):
        pass

    class DefaultNetworkSubclass(DefaultNetwork):
        @property
        def network_response_constructor(self):
            return DefaultNetworkResponseSubclass

    network = DefaultNetworkSubclass()
    response = make_network_request(network)
    assert isinstance(response, DefaultNetworkResponseSubclass)
