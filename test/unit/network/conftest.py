# coding: utf-8

from mock import Mock
import pytest
from requests import Session


@pytest.fixture(params=('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'))
def http_verb(request):
    return request.param


@pytest.fixture()
def mock_request(monkeypatch):
    mock_session_factory = Mock()
    mock_session_factory.return_value = session = Mock(Session(), request=Mock())
    monkeypatch.setattr('requests.Session', mock_session_factory)
    return session.request


@pytest.fixture(params=['generic_successful_request_response', 'server_error_request_response_502', 'server_error_request_response_503'])
def request_response(generic_successful_request_response, server_error_request_response_502, server_error_request_response_503, request):
    # pylint:disable=unused-argument
    return locals()[request.param]


@pytest.fixture
def make_request_with_request_response(mock_request, http_verb, test_url, access_token):

    def _make_request_with_request_response(network, request_response, **kwargs):
        mock_request.return_value = request_response
        response = network.request(http_verb, test_url, access_token, **kwargs)
        mock_request.assert_called_once_with(http_verb, test_url, **kwargs)
        assert response.access_token_used == access_token
        return response

    return _make_request_with_request_response


@pytest.fixture
def make_network_request(make_request_with_request_response, request_response):

    def _make_network_request(network, **kwargs):
        return make_request_with_request_response(network, request_response, **kwargs)

    return _make_network_request
