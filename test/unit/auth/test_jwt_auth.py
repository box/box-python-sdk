# coding: utf-8

from contextlib import contextmanager
from datetime import datetime, timedelta
import io
from itertools import cycle, product
import json
import random
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, generate_private_key as generate_rsa_private_key
from cryptography.hazmat.primitives import serialization
from mock import Mock, mock_open, patch, sentinel, call
import pytest
import pytz
import requests

from boxsdk.auth.jwt_auth import JWTAuth
from boxsdk.exception import BoxOAuthException
from boxsdk.config import API
from boxsdk.object.user import User


@pytest.fixture(params=[16, 32, 128])
def jti_length(request):
    return request.param


@pytest.fixture(params=('RS256', 'RS512'))
def jwt_algorithm(request):
    return request.param


@pytest.fixture(scope='module')
def jwt_key_id():
    return 'jwt_key_id_1'


@pytest.fixture(scope='module')
def rsa_private_key_object():
    return generate_rsa_private_key(public_exponent=65537, key_size=4096, backend=default_backend())


@pytest.fixture(params=(None, b'strong_password'))
def rsa_passphrase(request):
    return request.param


@pytest.fixture
def rsa_private_key_bytes(rsa_private_key_object, rsa_passphrase):
    encryption = serialization.BestAvailableEncryption(rsa_passphrase) if rsa_passphrase else serialization.NoEncryption()
    return rsa_private_key_object.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption,
    )


@pytest.fixture(scope='function')
def successful_token_response(successful_token_mock, successful_token_json_response):
    # pylint:disable=redefined-outer-name
    response = successful_token_json_response.copy()
    del response['refresh_token']
    successful_token_mock.json = Mock(return_value=response)
    successful_token_mock.ok = True
    successful_token_mock.content = json.dumps(response)
    successful_token_mock.status_code = 200
    return successful_token_mock


@pytest.mark.parametrize(('key_file', 'key_data'), [(None, None), ('fake sys path', 'fake key data')])
@pytest.mark.parametrize('rsa_passphrase', [None])
def test_jwt_auth_init_raises_type_error_unless_exactly_one_of_rsa_private_key_file_or_data_is_given(key_file, key_data, rsa_private_key_bytes):
    kwargs = dict(
        rsa_private_key_data=rsa_private_key_bytes,
        client_id=None,
        client_secret=None,
        jwt_key_id=None,
        enterprise_id=None,
    )
    JWTAuth(**kwargs)
    kwargs.update(rsa_private_key_file_sys_path=key_file, rsa_private_key_data=key_data)
    with pytest.raises(TypeError):
        JWTAuth(**kwargs)


@pytest.mark.parametrize('key_data', [object(), u'ƒøø'])
@pytest.mark.parametrize('rsa_passphrase', [None])
def test_jwt_auth_init_raises_type_error_if_rsa_private_key_data_has_unexpected_type(key_data, rsa_private_key_bytes):
    kwargs = dict(
        rsa_private_key_data=rsa_private_key_bytes,
        client_id=None,
        client_secret=None,
        jwt_key_id=None,
        enterprise_id=None,
    )
    JWTAuth(**kwargs)
    kwargs.update(rsa_private_key_data=key_data)
    with pytest.raises(TypeError):
        JWTAuth(**kwargs)


@pytest.mark.parametrize('rsa_private_key_data_type', [io.BytesIO, str, bytes, RSAPrivateKey])
def test_jwt_auth_init_accepts_rsa_private_key_data(rsa_private_key_bytes, rsa_passphrase, rsa_private_key_data_type):
    if rsa_private_key_data_type is str:
        rsa_private_key_data = str(rsa_private_key_bytes.decode('ascii'))
    elif rsa_private_key_data_type is RSAPrivateKey:
        rsa_private_key_data = serialization.load_pem_private_key(
            rsa_private_key_bytes,
            password=rsa_passphrase,
            backend=default_backend(),
        )
    else:
        rsa_private_key_data = rsa_private_key_data_type(rsa_private_key_bytes)
    JWTAuth(
        rsa_private_key_data=rsa_private_key_data,
        rsa_private_key_passphrase=rsa_passphrase,
        client_id=None,
        client_secret=None,
        jwt_key_id=None,
        enterprise_id=None,
    )


@pytest.fixture(params=[False, True])
def pass_private_key_by_path(request):
    """For jwt_auth_init_mocks, whether to pass the private key via sys_path (True) or pass the data directly (False)."""
    return request.param


@pytest.fixture
def jwt_auth_init_mocks(
        mock_box_session,
        successful_token_response,
        jwt_algorithm,
        jwt_key_id,
        rsa_passphrase,
        rsa_private_key_bytes,
        pass_private_key_by_path,
):
    # pylint:disable=redefined-outer-name

    @contextmanager
    def _jwt_auth_init_mocks(**kwargs):
        assert_authed = kwargs.pop('assert_authed', True)
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
        mock_box_session.request.return_value = successful_token_response
        with patch('boxsdk.auth.jwt_auth.open', mock_open(read_data=rsa_private_key_bytes), create=True) as jwt_auth_open:
            with patch('cryptography.hazmat.primitives.serialization.load_pem_private_key') as load_pem_private_key:
                oauth = JWTAuth(
                    client_id=fake_client_id,
                    client_secret=fake_client_secret,
                    rsa_private_key_file_sys_path=(sentinel.rsa_path if pass_private_key_by_path else None),
                    rsa_private_key_data=(None if pass_private_key_by_path else rsa_private_key_bytes),
                    rsa_private_key_passphrase=rsa_passphrase,
                    session=mock_box_session,
                    box_device_name='my_awesome_device',
                    jwt_algorithm=jwt_algorithm,
                    jwt_key_id=jwt_key_id,
                    enterprise_id=kwargs.pop('enterprise_id', None),
                    **kwargs
                )
                if pass_private_key_by_path:
                    jwt_auth_open.assert_called_once_with(sentinel.rsa_path, 'rb')
                    jwt_auth_open.return_value.read.assert_called_once_with()  # pylint:disable=no-member
                else:
                    jwt_auth_open.assert_not_called()
                load_pem_private_key.assert_called_once_with(
                    rsa_private_key_bytes,
                    password=rsa_passphrase,
                    backend=default_backend(),
                )

                yield oauth, assertion, fake_client_id, load_pem_private_key.return_value

        if assert_authed:
            mock_box_session.request.assert_called_once_with(
                'POST',
                f'{API.OAUTH2_API_URL}/token',
                data=data,
                headers={'content-type': 'application/x-www-form-urlencoded'},
                access_token=None,
            )
            assert oauth.access_token == successful_token_response.json()['access_token']

    return _jwt_auth_init_mocks


def test_refresh_authenticates_with_user_if_enterprise_id_and_user_both_passed_to_constructor(jwt_auth_init_and_auth_mocks):
    user = 'fake_user_id'
    with jwt_auth_init_and_auth_mocks(sub=user, sub_type='user', enterprise_id='fake_enterprise_id', user=user) as oauth:
        oauth.refresh(None)


@pytest.mark.parametrize('jwt_auth_method_name', ['authenticate_user', 'authenticate_instance'])
def test_authenticate_raises_value_error_if_sub_was_never_given(jwt_auth_init_mocks, jwt_auth_method_name):
    with jwt_auth_init_mocks(assert_authed=False) as params:
        auth = params[0]
        authenticate_method = getattr(auth, jwt_auth_method_name)
        with pytest.raises(ValueError):
            authenticate_method()


def test_jwt_auth_constructor_raises_type_error_if_user_is_unsupported_type(jwt_auth_init_mocks):
    with pytest.raises(TypeError):
        with jwt_auth_init_mocks(user=object()):
            assert False


def test_authenticate_user_raises_type_error_if_user_is_unsupported_type(jwt_auth_init_mocks):
    with jwt_auth_init_mocks(assert_authed=False) as params:
        auth = params[0]
        with pytest.raises(TypeError):
            auth.authenticate_user(object())


@pytest.mark.parametrize('user_id_for_init', [None, 'fake_user_id_1'])
def test_authenticate_user_saves_user_id_for_future_calls(jwt_auth_init_and_auth_mocks, user_id_for_init, jwt_encode):

    def assert_jwt_encode_call_args(user_id):
        assert jwt_encode.call_args[0][0]['sub'] == user_id
        assert jwt_encode.call_args[0][0]['box_sub_type'] == 'user'
        jwt_encode.call_args = None

    with jwt_auth_init_and_auth_mocks(sub=None, sub_type=None, assert_authed=False, user=user_id_for_init) as auth:
        for new_user_id in ['fake_user_id_2', 'fake_user_id_3']:
            auth.authenticate_user(new_user_id)
            assert_jwt_encode_call_args(new_user_id)
            auth.authenticate_user()
            assert_jwt_encode_call_args(new_user_id)


def test_authenticate_instance_raises_value_error_if_different_enterprise_id_is_given(jwt_auth_init_mocks):
    with jwt_auth_init_mocks(enterprise_id='fake_enterprise_id_1', assert_authed=False) as params:
        auth = params[0]
        with pytest.raises(ValueError):
            auth.authenticate_instance('fake_enterprise_id_2')


def test_authenticate_instance_saves_enterprise_id_for_future_calls(jwt_auth_init_and_auth_mocks):
    enterprise_id = 'fake_enterprise_id'
    with jwt_auth_init_and_auth_mocks(sub=enterprise_id, sub_type='enterprise', assert_authed=False) as auth:
        auth.authenticate_instance(enterprise_id)
        auth.authenticate_instance()
        auth.authenticate_instance(enterprise_id)
        with pytest.raises(ValueError):
            auth.authenticate_instance('fake_enterprise_id_2')


@pytest.yield_fixture
def jwt_encode():
    with patch('jwt.encode') as patched_jwt_encode:
        yield patched_jwt_encode


@pytest.fixture
def jwt_auth_auth_mocks(jti_length, jwt_algorithm, jwt_key_id, jwt_encode):

    @contextmanager
    def _jwt_auth_auth_mocks(sub, sub_type, oauth, assertion, client_id, secret, assert_authed=True):
        # pylint:disable=redefined-outer-name
        with patch('boxsdk.auth.jwt_auth.datetime') as mock_datetime:
            with patch('boxsdk.auth.jwt_auth.random.SystemRandom') as mock_system_random:
                jwt_encode.return_value = assertion
                mock_datetime.utcnow.return_value = datetime(2015, 7, 6, 12, 1, 2)
                mock_datetime.return_value = datetime(1970, 1, 1)
                now_plus_30 = mock_datetime.utcnow.return_value + timedelta(seconds=30)
                exp = int((now_plus_30 - datetime(1970, 1, 1)).total_seconds())
                system_random = mock_system_random.return_value
                system_random.randint.return_value = jti_length
                random_choices = [random.random() for _ in range(jti_length)]

                # Use cycle so that we can do auth more than once inside the context manager.
                system_random.random.side_effect = cycle(random_choices)

                ascii_alphabet = string.ascii_letters + string.digits
                ascii_len = len(ascii_alphabet)
                jti = ''.join(ascii_alphabet[int(r * ascii_len)] for r in random_choices)

                yield oauth

                if assert_authed:
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

    return _jwt_auth_auth_mocks


@pytest.fixture
def jwt_auth_init_and_auth_mocks(jwt_auth_init_mocks, jwt_auth_auth_mocks):

    @contextmanager
    def _jwt_auth_init_and_auth_mocks(sub, sub_type, *jwt_auth_init_mocks_args, **jwt_auth_init_mocks_kwargs):
        assert_authed = jwt_auth_init_mocks_kwargs.pop('assert_authed', True)
        with jwt_auth_init_mocks(*jwt_auth_init_mocks_args, assert_authed=assert_authed, **jwt_auth_init_mocks_kwargs) as params:
            with jwt_auth_auth_mocks(sub, sub_type, *params, assert_authed=assert_authed) as oauth:
                yield oauth

    return _jwt_auth_init_and_auth_mocks


@pytest.mark.parametrize(
    ('user', 'pass_in_init'),
    list(product([str('fake_user_id'), User(None, 'fake_user_id')], [False, True])),
)
def test_authenticate_user_sends_post_request_with_correct_params(jwt_auth_init_and_auth_mocks, user, pass_in_init):
    # pylint:disable=redefined-outer-name
    if isinstance(user, User):
        user_id = user.object_id
    elif isinstance(user, str):
        user_id = user
    else:
        raise NotImplementedError
    init_kwargs = {}
    authenticate_params = []
    if pass_in_init:
        init_kwargs['user'] = user
    else:
        authenticate_params.append(user)
    with jwt_auth_init_and_auth_mocks(user_id, 'user', **init_kwargs) as oauth:
        oauth.authenticate_user(*authenticate_params)


@pytest.mark.parametrize(('pass_in_init', 'pass_in_auth'), [(True, False), (False, True), (True, True)])
def test_authenticate_instance_sends_post_request_with_correct_params(jwt_auth_init_and_auth_mocks, pass_in_init, pass_in_auth):
    # pylint:disable=redefined-outer-name
    enterprise_id = 'fake_enterprise_id'
    init_kwargs = {}
    auth_params = []
    if pass_in_init:
        init_kwargs['enterprise_id'] = enterprise_id
    if pass_in_auth:
        auth_params.append(enterprise_id)
    with jwt_auth_init_and_auth_mocks(enterprise_id, 'enterprise', **init_kwargs) as oauth:
        oauth.authenticate_instance(*auth_params)


def test_refresh_app_user_sends_post_request_with_correct_params(jwt_auth_init_and_auth_mocks):
    # pylint:disable=redefined-outer-name
    fake_user_id = 'fake_user_id'
    with jwt_auth_init_and_auth_mocks(fake_user_id, 'user', user=fake_user_id) as oauth:
        oauth.refresh(None)


def test_refresh_instance_sends_post_request_with_correct_params(jwt_auth_init_and_auth_mocks):
    # pylint:disable=redefined-outer-name
    enterprise_id = 'fake_enterprise_id'
    with jwt_auth_init_and_auth_mocks(enterprise_id, 'enterprise', enterprise_id=enterprise_id) as oauth:
        oauth.refresh(None)


@pytest.fixture()
def jwt_subclass_that_just_stores_params():
    class StoreParamJWTAuth(JWTAuth):
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            super().__init__(**kwargs)

    return StoreParamJWTAuth


@pytest.fixture
def fake_client_id():
    return 'fake_client_id'


@pytest.fixture
def fake_client_secret():
    return 'fake_client_secret'


@pytest.fixture
def fake_enterprise_id():
    return 'fake_enterprise_id'


@pytest.fixture
def app_config_json_content(
        fake_client_id,
        fake_client_secret,
        fake_enterprise_id,
        jwt_key_id,
        rsa_private_key_bytes,
        rsa_passphrase,
):
    template = r"""
{{
  "boxAppSettings": {{
    "clientID": "{client_id}",
    "clientSecret": "{client_secret}",
    "appAuth": {{
      "publicKeyID": "{jwt_key_id}",
      "privateKey": "{private_key}",
      "passphrase": {passphrase}
    }}
  }},
  "enterpriseID": {enterprise_id}
}}"""
    return template.format(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
        jwt_key_id=jwt_key_id,
        private_key=rsa_private_key_bytes.replace(b"\n", b"\\n").decode(),
        passphrase=json.dumps(rsa_passphrase and rsa_passphrase.decode()),
        enterprise_id=json.dumps(fake_enterprise_id),
    )


@pytest.fixture()
def assert_jwt_kwargs_expected(
        fake_client_id,
        fake_client_secret,
        fake_enterprise_id,
        jwt_key_id,
        rsa_private_key_bytes,
        rsa_passphrase,
):
    def _assert_jwt_kwargs_expected(jwt_auth):
        assert jwt_auth.kwargs['client_id'] == fake_client_id
        assert jwt_auth.kwargs['client_secret'] == fake_client_secret
        assert jwt_auth.kwargs['enterprise_id'] == fake_enterprise_id
        assert jwt_auth.kwargs['jwt_key_id'] == jwt_key_id
        assert jwt_auth.kwargs['rsa_private_key_data'] == rsa_private_key_bytes.decode()
        assert jwt_auth.kwargs['rsa_private_key_passphrase'] == (rsa_passphrase and rsa_passphrase.decode())

    return _assert_jwt_kwargs_expected


def test_from_config_file(
        jwt_subclass_that_just_stores_params,
        app_config_json_content,
        assert_jwt_kwargs_expected,
):
    # pylint:disable=redefined-outer-name
    with patch('boxsdk.auth.jwt_auth.open', mock_open(read_data=app_config_json_content), create=True):
        jwt_auth_from_config_file = jwt_subclass_that_just_stores_params.from_settings_file('fake_config_file_sys_path')
        assert_jwt_kwargs_expected(jwt_auth_from_config_file)


def test_from_settings_dictionary(
        jwt_subclass_that_just_stores_params,
        app_config_json_content,
        assert_jwt_kwargs_expected,
):
    jwt_auth_from_dictionary = jwt_subclass_that_just_stores_params.from_settings_dictionary(json.loads(app_config_json_content))
    assert_jwt_kwargs_expected(jwt_auth_from_dictionary)


@pytest.fixture
def expect_auth_retry(status_code, error_description, include_date_header, error_code):
    return status_code == 400 and 'exp' in error_description and include_date_header and error_code == 'invalid_grant'


@pytest.fixture
def box_datetime():
    return datetime.now(tz=pytz.utc) - timedelta(100)


@pytest.fixture
def unsuccessful_jwt_response(box_datetime, status_code, error_description, include_date_header, error_code):
    headers = {'Date': box_datetime.strftime('%a, %d %b %Y %H:%M:%S %Z')} if include_date_header else {}
    unsuccessful_response = Mock(requests.Response(), headers=headers)
    unsuccessful_response.json.return_value = {'error_description': error_description, 'error': error_code}
    unsuccessful_response.status_code = status_code
    unsuccessful_response.ok = False
    return unsuccessful_response


@pytest.mark.parametrize('jwt_algorithm', ('RS512',))
@pytest.mark.parametrize('rsa_passphrase', (None,))
@pytest.mark.parametrize('pass_private_key_by_path', (False,))
@pytest.mark.parametrize('status_code', (400, 401))
@pytest.mark.parametrize('error_description', ('invalid box_sub_type claim', 'invalid kid', "check the 'exp' claim"))
@pytest.mark.parametrize('error_code', ('invalid_grant', 'bad_request'))
@pytest.mark.parametrize('include_date_header', (True, False))
def test_auth_retry_for_invalid_exp_claim(
        jwt_auth_init_mocks,
        expect_auth_retry,
        unsuccessful_jwt_response,
        box_datetime,
):
    # pylint:disable=redefined-outer-name
    enterprise_id = 'fake_enterprise_id'
    with jwt_auth_init_mocks(assert_authed=False) as params:
        auth = params[0]
        with patch.object(auth, '_construct_and_send_jwt_auth') as mock_send_jwt:
            mock_send_jwt.side_effect = [BoxOAuthException(400, network_response=unsuccessful_jwt_response), 'jwt_token']
            if not expect_auth_retry:
                with pytest.raises(BoxOAuthException):
                    auth.authenticate_instance(enterprise_id)
            else:
                auth.authenticate_instance(enterprise_id)
            expected_calls = [call(enterprise_id, 'enterprise', None)]
            if expect_auth_retry:
                expected_calls.append(call(enterprise_id, 'enterprise', box_datetime.replace(microsecond=0, tzinfo=None)))
            assert len(mock_send_jwt.mock_calls) == len(expected_calls)
            mock_send_jwt.assert_has_calls(expected_calls)


@pytest.mark.parametrize('jwt_algorithm', ('RS512',))
@pytest.mark.parametrize('rsa_passphrase', (None,))
@pytest.mark.parametrize('pass_private_key_by_path', (False,))
@pytest.mark.parametrize('status_code', (429,))
@pytest.mark.parametrize('error_description', ('Request rate limit exceeded',))
@pytest.mark.parametrize('error_code', ('rate_limit_exceeded',))
@pytest.mark.parametrize('include_date_header', (False,))
def test_auth_retry_for_rate_limit_error(
        jwt_auth_init_mocks,
        unsuccessful_jwt_response,
):
    # pylint:disable=redefined-outer-name
    enterprise_id = 'fake_enterprise_id'
    with jwt_auth_init_mocks(assert_authed=False) as params:
        auth = params[0]
        with patch.object(auth, '_construct_and_send_jwt_auth') as mock_send_jwt:
            side_effect = []
            expected_calls = []
            # Retries multiple times, but less than max retries. Then succeeds when it gets a token.
            for _ in range(API.MAX_RETRY_ATTEMPTS - 2):
                side_effect.append(BoxOAuthException(429, network_response=unsuccessful_jwt_response))
                expected_calls.append(call(enterprise_id, 'enterprise', None))
            side_effect.append('jwt_token')
            expected_calls.append(call(enterprise_id, 'enterprise', None))
            mock_send_jwt.side_effect = side_effect

            auth.authenticate_instance(enterprise_id)
            assert len(mock_send_jwt.mock_calls) == len(expected_calls)
            mock_send_jwt.assert_has_calls(expected_calls)


@pytest.mark.parametrize('jwt_algorithm', ('RS512',))
@pytest.mark.parametrize('rsa_passphrase', (None,))
@pytest.mark.parametrize('pass_private_key_by_path', (False,))
@pytest.mark.parametrize('status_code', (429,))
@pytest.mark.parametrize('error_description', ('Request rate limit exceeded',))
@pytest.mark.parametrize('error_code', ('rate_limit_exceeded',))
@pytest.mark.parametrize('include_date_header', (False,))
def test_auth_max_retries_for_rate_limit_error(
        jwt_auth_init_mocks,
        unsuccessful_jwt_response,
):
    # pylint:disable=redefined-outer-name
    enterprise_id = 'fake_enterprise_id'
    with jwt_auth_init_mocks(assert_authed=False) as params:
        auth = params[0]
        with patch.object(auth, '_construct_and_send_jwt_auth') as mock_send_jwt:
            side_effect = []
            expected_calls = []
            # Retries max number of times, then throws the error
            for _ in range(API.MAX_RETRY_ATTEMPTS + 1):
                side_effect.append(BoxOAuthException(429, network_response=unsuccessful_jwt_response))
                expected_calls.append(call(enterprise_id, 'enterprise', None))
            mock_send_jwt.side_effect = side_effect

            with pytest.raises(BoxOAuthException) as error:
                auth.authenticate_instance(enterprise_id)
            assert error.value.status == 429
            assert len(mock_send_jwt.mock_calls) == len(expected_calls)
            mock_send_jwt.assert_has_calls(expected_calls)


@pytest.mark.parametrize('jwt_algorithm', ('RS512',))
@pytest.mark.parametrize('rsa_passphrase', (None,))
@pytest.mark.parametrize('pass_private_key_by_path', (False,))
@pytest.mark.parametrize('status_code', (500,))
@pytest.mark.parametrize('error_description', ('Internal Server Error',))
@pytest.mark.parametrize('error_code', ('internal_server_error',))
@pytest.mark.parametrize('include_date_header', (False,))
def test_auth_retry_for_internal_server_error(
        jwt_auth_init_mocks,
        unsuccessful_jwt_response,
):
    # pylint:disable=redefined-outer-name
    enterprise_id = 'fake_enterprise_id'
    with jwt_auth_init_mocks(assert_authed=False) as params:
        auth = params[0]
        with patch.object(auth, '_construct_and_send_jwt_auth') as mock_send_jwt:
            side_effect = []
            expected_calls = []
            # Retries multiple times, but less than max retries. Then succeeds when it gets a token.
            for _ in range(API.MAX_RETRY_ATTEMPTS - 2):
                side_effect.append(BoxOAuthException(500, network_response=unsuccessful_jwt_response))
                expected_calls.append(call(enterprise_id, 'enterprise', None))
            side_effect.append('jwt_token')
            expected_calls.append(call(enterprise_id, 'enterprise', None))
            mock_send_jwt.side_effect = side_effect

            auth.authenticate_instance(enterprise_id)
            assert len(mock_send_jwt.mock_calls) == len(expected_calls)
            mock_send_jwt.assert_has_calls(expected_calls)


@pytest.mark.parametrize('jwt_algorithm', ('RS512',))
@pytest.mark.parametrize('rsa_passphrase', (None,))
@pytest.mark.parametrize('pass_private_key_by_path', (False,))
@pytest.mark.parametrize('status_code', (500,))
@pytest.mark.parametrize('error_description', ('Internal Server Error',))
@pytest.mark.parametrize('error_code', ('internal_server_error',))
@pytest.mark.parametrize('include_date_header', (False,))
def test_auth_max_retries_for_internal_server_error(
        jwt_auth_init_mocks,
        unsuccessful_jwt_response,
):
    # pylint:disable=redefined-outer-name
    enterprise_id = 'fake_enterprise_id'
    with jwt_auth_init_mocks(assert_authed=False) as params:
        auth = params[0]
        with patch.object(auth, '_construct_and_send_jwt_auth') as mock_send_jwt:
            side_effect = []
            expected_calls = []
            # Retries max number of times, then throws the error
            for _ in range(API.MAX_RETRY_ATTEMPTS + 1):
                side_effect.append(BoxOAuthException(500, network_response=unsuccessful_jwt_response))
                expected_calls.append(call(enterprise_id, 'enterprise', None))
            mock_send_jwt.side_effect = side_effect

            with pytest.raises(BoxOAuthException) as error:
                auth.authenticate_instance(enterprise_id)
            assert error.value.status == 500
            assert len(mock_send_jwt.mock_calls) == len(expected_calls)
            mock_send_jwt.assert_has_calls(expected_calls)
