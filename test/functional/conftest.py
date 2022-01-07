# coding: utf-8
from urllib import parse
from test.functional.mock_box.box import Box
from test.util.streamable_mock_open import streamable_mock_open

import re
import pytest
import requests

from mock import patch
from boxsdk.auth.oauth2 import OAuth2
from boxsdk.client import LoggingClient
from boxsdk.config import API
from boxsdk.network.default_network import DefaultNetwork
from boxsdk.session.session import Session, AuthorizedSession


@pytest.fixture(scope='session')
def network_layer():
    return DefaultNetwork()


@pytest.fixture()
def box_client(box_oauth, box_session):
    # pylint:disable=redefined-outer-name
    return LoggingClient(box_oauth, session=box_session)


@pytest.fixture
def unauthorized_session(network_layer):
    return Session(network_layer=network_layer)


@pytest.fixture
def box_session(box_oauth, network_layer):
    # pylint:disable=redefined-outer-name
    return AuthorizedSession(oauth=box_oauth, network_layer=network_layer)


@pytest.fixture()
def box_oauth(client_id, client_secret, user_login, unauthorized_session):
    # pylint:disable=redefined-outer-name
    oauth2 = OAuth2(client_id, client_secret, box_device_name='mock_box functional test', session=unauthorized_session)
    url, _ = oauth2.get_authorization_url('http://localhost')
    form = requests.get(url + '&box_login=' + user_login).content.decode('utf-8')
    form_action = re.search('action="([^"]*)"', form).group(1)
    auth_response = requests.post(form_action, allow_redirects=False, data={
        'login': user_login,
        'client_id': client_id,
        'client_secret': client_secret,
    })
    redirect_url = auth_response.headers['Location']
    query_string = parse.urlparse(redirect_url).query
    parsed_query_string_dict = parse.parse_qs(query_string)

    # Get the OAuth2 authorization code from `parsed_query_string_dict`
    # (NOTE: the values in the dictionary are lists of strings),
    # and if necessary decode it from a utf-8 encoded byte string to
    # a unicode string.
    auth_code = parsed_query_string_dict['code'][0]
    if isinstance(auth_code, bytes):
        auth_code = auth_code.decode('utf-8')

    oauth2.authenticate(auth_code)
    return oauth2


@pytest.fixture(scope='session')
def mock_box_server(request):
    box = Box()
    request.addfinalizer(box.shutdown)
    return box


@pytest.fixture(autouse=True)
def mock_box(mock_box_server, monkeypatch, client_id, client_secret, user_name, user_login):
    # pylint:disable=redefined-outer-name
    mock_box_server.reset_filesystem([(user_name, user_login)], [(client_id, client_secret, 0)])
    monkeypatch.setattr(API, 'BASE_API_URL', f'http://localhost:{Box.API_PORT}')
    monkeypatch.setattr(API, 'UPLOAD_URL', f'http://localhost:{Box.UPLOAD_PORT}')
    monkeypatch.setattr(API, 'OAUTH2_API_URL', f'http://localhost:{Box.OAUTH_API_PORT}')
    monkeypatch.setattr(API, 'OAUTH2_AUTHORIZE_URL', f'http://localhost:{Box.OAUTH_AUTHORIZE_PORT}')
    return mock_box_server


@pytest.fixture(params=[
    'foo.txt',
    'bar.docx',
    'foo.txt',
])
def file_name(request):
    return request.param


@pytest.fixture(params=[
    'some_folder',
    'Ѵȁćȁƭȉőń Ρȉćƭȕŕȅŝ',
])
def folder_name(request):
    return request.param


@pytest.fixture(scope='session')
def user_name():
    return 'User 1'


@pytest.fixture(scope='session')
def user_login():
    return 'user.1@example.com'


@pytest.fixture()
def uploaded_file(box_client, test_file_path, test_file_content, file_name):
    # pylint:disable=redefined-outer-name
    with patch('boxsdk.object.folder.open', streamable_mock_open(read_data=test_file_content), create=True):
        return box_client.folder('0').upload(test_file_path, file_name)


@pytest.fixture()
def created_subfolder(box_client, folder_name):
    # pylint:disable=redefined-outer-name
    return box_client.folder('0').create_subfolder(folder_name)
