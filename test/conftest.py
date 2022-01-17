# coding: utf-8

import json
import logging
import sys

from mock import Mock
import pytest
import requests

from boxsdk.network.default_network import DefaultNetworkResponse


@pytest.fixture(autouse=True, scope='session')
def logger():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    return logging.getLogger(__name__.split('.', maxsplit=1)[0])


def _set_content_and_json_from_json(mock_response, json_value):
    mock_response.json.return_value = json_value
    mock_response.content = content = json.dumps(json_value).encode('utf-8')
    mock_response.headers['Content-Length'] = str(len(content))


def _set_content_and_json_from_content(mock_response, content):
    if not isinstance(content, bytes):
        raise TypeError(f"Expected 'content' to be byte string, got {content.__class__.__name__!r}.")
    mock_response.content = content
    mock_response.headers['Content-Length'] = str(len(content))
    try:
        mock_response.json.return_value = json.loads(content.decode('utf-8'))
    except ValueError as exc:
        mock_response.json.side_effect = exc


@pytest.fixture()
def generic_successful_request_response():
    mock_request_response = Mock(requests.Response(), headers={f'header{i}': f'value{i}' for i in range(4)})
    _set_content_and_json_from_json(mock_request_response, json_value={f'key{i}': f'value{i}' for i in range(8)})
    mock_request_response.status_code = 200
    mock_request_response.ok = True
    mock_request_response.request = Mock()
    return mock_request_response


def _network_response_mock_from_request_response(request_response):
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.request_response = request_response
    mock_network_response.json.side_effect = request_response.json
    mock_network_response.content = request_response.content
    mock_network_response.headers = request_response.headers
    mock_network_response.status_code = request_response.status_code
    mock_network_response.ok = request_response.ok
    return mock_network_response


@pytest.fixture()
def generic_successful_response(generic_successful_request_response):
    return _network_response_mock_from_request_response(generic_successful_request_response)


@pytest.fixture(scope='session')
def successful_token_json_response(access_token, refresh_token):
    # pylint:disable=redefined-outer-name
    return {
        'access_token': access_token,
        'expires_in': 3600,
        'restricted_to': [],
        'token_type': 'bearer',
        'refresh_token': refresh_token,
    }


@pytest.fixture()
def successful_token_request_response(successful_token_json_response):
    # pylint:disable=redefined-outer-name
    successful_token_mock = Mock(requests.Response(), headers={})
    _set_content_and_json_from_json(successful_token_mock, json_value=successful_token_json_response)
    successful_token_mock.ok = True
    successful_token_mock.status_code = 200
    return successful_token_mock


@pytest.fixture()
def successful_token_response(successful_token_request_response):
    return _network_response_mock_from_request_response(successful_token_request_response)


@pytest.fixture()
def successful_token_mock(successful_token_response):
    return successful_token_response


@pytest.fixture()
def unauthorized_response():
    res = Mock(DefaultNetworkResponse, headers={})
    _set_content_and_json_from_content(res, content=b'')
    res.status_code = 401
    res.ok = False
    res.request = Mock()
    return res


@pytest.fixture()
def non_json_response():
    mock_network_response = Mock(DefaultNetworkResponse, headers={})
    _set_content_and_json_from_content(mock_network_response, content=b'')
    mock_network_response.ok = True
    mock_network_response.status_code = 200
    return mock_network_response


def _retry_after_response(status_code):
    mock_network_response = Mock(DefaultNetworkResponse, headers={})
    mock_network_response.status_code = status_code
    mock_network_response.headers.update({'Retry-After': '1'})
    return mock_network_response


@pytest.fixture()
def retry_after_response_202():
    return _retry_after_response(202)


@pytest.fixture()
def retry_after_response_429():
    return _retry_after_response(429)


@pytest.fixture(params=[202, 429])
def retry_after_response(retry_after_response_202, retry_after_response_429, request):
    if request.param == 202:
        return retry_after_response_202
    if request.param == 429:
        return retry_after_response_429

    raise ValueError


def _server_error_request_response(status_code):
    mock_request_response = Mock(requests.Response(), headers={f'header{i}': f'value{i}' for i in range(4)})
    _set_content_and_json_from_json(mock_request_response, json_value={f'key{i}': f'value{i}' for i in range(8)})
    mock_request_response.status_code = status_code
    mock_request_response.ok = False
    return mock_request_response


@pytest.fixture()
def server_error_request_response_502():
    return _server_error_request_response(502)


@pytest.fixture()
def server_error_request_response_503():
    return _server_error_request_response(503)


@pytest.fixture(params=[502, 503])
def server_error_request_response(server_error_request_response_502, server_error_request_response_503, request):
    if request.param == 502:
        return server_error_request_response_502
    if request.param == 503:
        return server_error_request_response_503
    raise ValueError


@pytest.fixture
def server_error_response(server_error_request_response):
    return _network_response_mock_from_request_response(server_error_request_response)


@pytest.fixture()
def bad_network_response():
    mock_network_response = Mock(DefaultNetworkResponse, headers={})
    mock_network_response.status_code = 404
    _set_content_and_json_from_json(mock_network_response, json_value={'code': 404, 'message': 'Not Found'})
    mock_network_response.ok = False
    return mock_network_response


@pytest.fixture()
def bad_network_response_400():
    mock_network_response = Mock(DefaultNetworkResponse, headers={})
    mock_network_response.status_code = 400
    _set_content_and_json_from_json(mock_network_response, json_value={'error': 'Example Error', 'error_description': 'Example Error Description'})
    mock_network_response.ok = False
    return mock_network_response


@pytest.fixture()
def failed_non_json_response():
    mock_network_response = Mock(DefaultNetworkResponse, headers={})
    mock_network_response.status_code = 404
    _set_content_and_json_from_content(mock_network_response, content=b'')
    mock_network_response.ok = False
    return mock_network_response


@pytest.fixture(scope='session')
def access_token():
    return 'T9cE5asGnuyYCCqIZFoWjFHvNbvVqHjl'


@pytest.fixture(scope='session')
def new_access_token():
    # Must be distinct from access_token.
    return 'ZFoWjFHvNbvVqHjlT9cE5asGnuyYCCqI'


@pytest.fixture(scope='session')
def refresh_token():
    return 'J7rxTiWOHMoSC1isKZKBZWizoRXjkQzig5C6jFgCVJ9bUnsUfGMinKBDLZWP9BgRb'


@pytest.fixture(scope='session')
def test_url():
    return 'https://box.com/test/url'


@pytest.fixture(scope='session')
def client_id():
    return 'fake_client_id'


@pytest.fixture(scope='session')
def client_secret():
    return 'fake_client_secret'


@pytest.fixture(scope='session')
def auth_code():
    return 'fake_auth_code'


@pytest.fixture(params=[
    b'Hello',
    b'Goodbye',
    b'42',
])
def test_file_content(request):
    return request.param


@pytest.fixture()
def update_file_content(test_file_content):
    # pylint:disable=redefined-outer-name
    return test_file_content


@pytest.fixture()
def test_file_path():
    return 'path/to/file'


@pytest.fixture(scope='module')
def mock_object_id():
    return '42'


@pytest.fixture(scope='module')
def mock_user_id():
    return 'fake-user-100'


@pytest.fixture(scope='module')
def mock_group_id():
    return 'fake-group-99'
