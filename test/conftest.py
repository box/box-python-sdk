# coding: utf-8

from __future__ import unicode_literals
import json
from mock import Mock
import pytest
from boxsdk.network.default_network import DefaultNetworkResponse


@pytest.fixture(scope='session')
def generic_successful_response():
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.content = b'{"message": "success"}'
    mock_network_response.status_code = 200
    mock_network_response.ok = True
    mock_network_response.raw = Mock()
    return mock_network_response


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


@pytest.fixture(scope='session')
def successful_token_response(successful_token_mock, successful_token_json_response):
    # pylint:disable=redefined-outer-name
    successful_token_mock.json = Mock(return_value=successful_token_json_response)
    successful_token_mock.ok = True
    successful_token_mock.content = json.dumps(successful_token_json_response)
    successful_token_mock.status_code = 200
    return successful_token_mock


@pytest.fixture(scope='session')
def successful_token_mock():
    return Mock(DefaultNetworkResponse)


@pytest.fixture(scope='session')
def unauthorized_response():
    res = Mock(DefaultNetworkResponse)
    res.content = b''
    res.status_code = 401
    res.ok = False
    return res


@pytest.fixture(scope='session')
def non_json_response():
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.content = b''
    mock_network_response.ok = True
    mock_network_response.status_code = 200
    mock_network_response.json.side_effect = ValueError('No JSON object could be decoded')
    return mock_network_response


@pytest.fixture(scope='session', params=[202, 429])
def retry_after_response(request):
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.status_code = int(request.param)
    mock_network_response.headers = {'Retry-After': '1'}
    return mock_network_response


@pytest.fixture(scope='session', params=[502, 503])
def server_error_response(request):
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.status_code = int(request.param)
    mock_network_response.ok = False
    return mock_network_response


@pytest.fixture(scope='session')
def bad_network_response():
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.status_code = 404
    mock_network_response.json.return_value = {'code': 404, 'message': 'Not Found'}
    mock_network_response.ok = False
    return mock_network_response


@pytest.fixture(scope='session')
def failed_non_json_response():
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.status_code = 404
    mock_network_response.json.side_effect = ValueError('No JSON object could be decoded')
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
