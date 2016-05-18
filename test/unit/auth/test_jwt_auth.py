# coding: utf-8

from __future__ import unicode_literals

from contextlib import contextmanager
from datetime import datetime, timedelta
import json
import random
import string

from cryptography.hazmat.backends import default_backend
from mock import Mock, mock_open, patch, sentinel
import pytest

from boxsdk.auth.jwt_auth import JWTAuth
from boxsdk.config import API
from boxsdk.object.user import User
from boxsdk.util.compat import total_seconds


@pytest.fixture(params=[16, 32, 128])
def jti_length(request):
    return request.param


@pytest.fixture(params=('RS256', 'RS512'))
def jwt_algorithm(request):
    return request.param


@pytest.fixture(scope='module')
def jwt_key_id():
    return 'jwt_key_id_1'


@pytest.fixture(params=(None, b'strong_password'))
def rsa_passphrase(request):
    return request.param


@pytest.fixture(scope='module')
def successful_token_response(successful_token_mock, successful_token_json_response):
    # pylint:disable=redefined-outer-name
    response = successful_token_json_response.copy()
    del response['refresh_token']
    successful_token_mock.json = Mock(return_value=response)
    successful_token_mock.ok = True
    successful_token_mock.content = json.dumps(response)
    successful_token_mock.status_code = 200
    return successful_token_mock


@contextmanager
def jwt_auth_init_mocks(
        mock_network_layer,
        successful_token_response,
        jwt_algorithm,
        jwt_key_id,
        rsa_passphrase,
        enterprise_id=None,
):
    # pylint:disable=redefined-outer-name
    fake_client_id = 'fake_client_id'
    fake_client_secret = 'fake_client_secret'
    assertion = Mock()
    data = {
        'grant_type': JWTAuth._GRANT_TYPE,  # pylint:disable=protected-access
        'client_id': fake_client_id,
        'client_secret': fake_client_secret,
        'assertion': assertion,
        'box_device_id': '0',
        'box_device_name': 'my_awesome_device',
    }

    mock_network_layer.request.return_value = successful_token_response
    key_file_read_data = 'key_file_read_data'
    with patch('boxsdk.auth.jwt_auth.open', mock_open(read_data=key_file_read_data), create=True) as jwt_auth_open:
        with patch('cryptography.hazmat.primitives.serialization.load_pem_private_key') as load_pem_private_key:
            oauth = JWTAuth(
                client_id=fake_client_id,
                client_secret=fake_client_secret,
                enterprise_id=enterprise_id,
                rsa_private_key_file_sys_path=sentinel.rsa_path,
                rsa_private_key_passphrase=rsa_passphrase,
                network_layer=mock_network_layer,
                box_device_name='my_awesome_device',
                jwt_algorithm=jwt_algorithm,
                jwt_key_id=jwt_key_id,
            )

            jwt_auth_open.assert_called_once_with(sentinel.rsa_path)
            jwt_auth_open.return_value.read.assert_called_once_with()  # pylint:disable=no-member
            load_pem_private_key.assert_called_once_with(
                key_file_read_data,
                password=rsa_passphrase,
                backend=default_backend(),
            )

            yield oauth, assertion, fake_client_id, load_pem_private_key.return_value

    mock_network_layer.request.assert_called_once_with(
        'POST',
        '{0}/token'.format(API.OAUTH2_API_URL),
        data=data,
        headers={'content-type': 'application/x-www-form-urlencoded'},
        access_token=None,
    )
    assert oauth.access_token == successful_token_response.json()['access_token']


@contextmanager
def jwt_auth_auth_mocks(jti_length, jwt_algorithm, jwt_key_id, sub, sub_type, oauth, assertion, client_id, secret):
    # pylint:disable=redefined-outer-name
    with patch('jwt.encode') as jwt_encode:
        with patch('boxsdk.auth.jwt_auth.datetime') as mock_datetime:
            with patch('boxsdk.auth.jwt_auth.random.SystemRandom') as mock_system_random:
                jwt_encode.return_value = assertion
                mock_datetime.utcnow.return_value = datetime(2015, 7, 6, 12, 1, 2)
                mock_datetime.return_value = datetime(1970, 1, 1)
                now_plus_30 = mock_datetime.utcnow.return_value + timedelta(seconds=30)
                exp = int(total_seconds(now_plus_30 - datetime(1970, 1, 1)))
                system_random = mock_system_random.return_value
                system_random.randint.return_value = jti_length
                random_choices = [random.random() for _ in range(jti_length)]
                system_random.random.side_effect = random_choices
                ascii_alphabet = string.ascii_letters + string.digits
                ascii_len = len(ascii_alphabet)
                jti = ''.join(ascii_alphabet[int(r * ascii_len)] for r in random_choices)

                yield oauth

                system_random.randint.assert_called_once_with(16, 128)
                assert len(system_random.random.mock_calls) == jti_length
                jwt_encode.assert_called_once_with({
                    'iss': client_id,
                    'sub': sub,
                    'box_sub_type': sub_type,
                    'aud': 'https://api.box.com/oauth2/token',
                    'jti': jti,
                    'exp': exp,
                }, secret, algorithm=jwt_algorithm, headers={'kid': jwt_key_id})


def test_authenticate_app_user_sends_post_request_with_correct_params(
        mock_network_layer,
        successful_token_response,
        jti_length,
        jwt_algorithm,
        jwt_key_id,
        rsa_passphrase,
):
    # pylint:disable=redefined-outer-name
    fake_user_id = 'fake_user_id'
    with jwt_auth_init_mocks(mock_network_layer, successful_token_response, jwt_algorithm, jwt_key_id, rsa_passphrase) as params:
        with jwt_auth_auth_mocks(jti_length, jwt_algorithm, jwt_key_id, fake_user_id, 'user', *params) as oauth:
            oauth.authenticate_app_user(User(None, fake_user_id))


def test_authenticate_instance_sends_post_request_with_correct_params(
        mock_network_layer,
        successful_token_response,
        jti_length,
        jwt_algorithm,
        jwt_key_id,
        rsa_passphrase,
):
    # pylint:disable=redefined-outer-name
    enterprise_id = 'fake_enterprise_id'
    with jwt_auth_init_mocks(
        mock_network_layer,
        successful_token_response,
        jwt_algorithm,
        jwt_key_id,
        rsa_passphrase,
        enterprise_id,
    ) as params:
        with jwt_auth_auth_mocks(jti_length, jwt_algorithm, jwt_key_id, enterprise_id, 'enterprise', *params) as oauth:
            oauth.authenticate_instance()


def test_refresh_app_user_sends_post_request_with_correct_params(
        mock_network_layer,
        successful_token_response,
        jti_length,
        jwt_algorithm,
        jwt_key_id,
        rsa_passphrase,
):
    # pylint:disable=redefined-outer-name
    fake_user_id = 'fake_user_id'
    with jwt_auth_init_mocks(mock_network_layer, successful_token_response, jwt_algorithm, jwt_key_id, rsa_passphrase) as params:
        with jwt_auth_auth_mocks(jti_length, jwt_algorithm, jwt_key_id, fake_user_id, 'user', *params) as oauth:
            oauth._user_id = fake_user_id  # pylint:disable=protected-access
            oauth.refresh(None)


def test_refresh_instance_sends_post_request_with_correct_params(
        mock_network_layer,
        successful_token_response,
        jti_length,
        jwt_algorithm,
        jwt_key_id,
        rsa_passphrase,
):
    # pylint:disable=redefined-outer-name
    enterprise_id = 'fake_enterprise_id'
    with jwt_auth_init_mocks(
        mock_network_layer,
        successful_token_response,
        jwt_algorithm,
        jwt_key_id,
        rsa_passphrase,
        enterprise_id,
    ) as params:
        with jwt_auth_auth_mocks(jti_length, jwt_algorithm, jwt_key_id, enterprise_id, 'enterprise', *params) as oauth:
            oauth.refresh(None)
