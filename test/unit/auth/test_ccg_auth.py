import json
from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import Mock, MagicMock, call
from test.unit.object.conftest import mock_user  # pylint:disable=unused-import

import pytz
import pytest
from pytest_lazyfixture import lazy_fixture

from boxsdk import BoxOAuthException
from boxsdk.auth.ccg_auth import CCGAuth
from boxsdk.config import API


USER_SUBJECT_TYPE = 'user'
ENTERPRISE_SUBJECT_TYPE = 'enterprise'


@pytest.fixture(scope='function')
def successful_token_response(successful_token_json_response):
    successful_token_response_mock = MagicMock()
    response = successful_token_json_response.copy()
    del response['refresh_token']
    successful_token_response_mock.items = response
    successful_token_response_mock.json = Mock(return_value=response)
    successful_token_response_mock.access_token = response['access_token']
    successful_token_response_mock.ok = True
    successful_token_response_mock.content = json.dumps(response)
    successful_token_response_mock.status_code = 200
    return successful_token_response_mock


@pytest.fixture
def unsuccessful_ccg_response(box_datetime, status_code, error_description, include_date_header, error_code):
    headers = {'Date': box_datetime.strftime('%a, %d %b %Y %H:%M:%S %Z')} if include_date_header else {}
    unsuccessful_response = Mock(headers=headers)
    unsuccessful_response.json.return_value = {'error_description': error_description, 'error': error_code}
    unsuccessful_response.status_code = status_code
    unsuccessful_response.ok = False
    return unsuccessful_response


@pytest.fixture()
def ccg_auth(client_id, client_secret, ccg_user_id, ccg_enterprise_id) -> CCGAuth:
    auth = CCGAuth(client_id=client_id, client_secret=client_secret, user=ccg_user_id, enterprise_id=ccg_enterprise_id)
    auth._session.get_retry_after_time = MagicMock(return_value=0)  # pylint:disable=protected-access
    return auth


@pytest.fixture
def expect_auth_retry(status_code, error_description, include_date_header, error_code):
    return status_code == 400 and 'exp' in error_description and include_date_header and error_code == 'invalid_grant'


@pytest.fixture
def box_datetime():
    return datetime.now(tz=pytz.utc) - timedelta(100)


@pytest.mark.parametrize('enterprise_id', (lazy_fixture('mock_enterprise_id'), None))
@pytest.mark.parametrize('user, expected_normalized_user_id',
                         [
                             (lazy_fixture('mock_user'), lazy_fixture('mock_user_id')),
                             (lazy_fixture('mock_user_id'), lazy_fixture('mock_user_id')),
                             (None, None)
                         ])
def test_successful_create_ccg_auth_object_and_normalize_user_id(client_id, client_secret, enterprise_id, user, expected_normalized_user_id):
    auth = CCGAuth(client_id=client_id, client_secret=client_secret, enterprise_id=enterprise_id, user=user)
    assert auth._user_id == expected_normalized_user_id  # pylint:disable=protected-access


def test_throw_type_error_when_invalid_user_object_provided(client_id, client_secret, mock_enterprise_id):
    with pytest.raises(TypeError):
        CCGAuth(
            client_id=client_id,
            client_secret=client_secret,
            enterprise_id=mock_enterprise_id,
            user=123123
        )


@pytest.mark.parametrize('ccg_user_id, ccg_enterprise_id, user',
                         [
                             (lazy_fixture('mock_user_id'), None, None),
                             (None, None, lazy_fixture('mock_user_id')),
                             (None, None, lazy_fixture('mock_user'))
                         ])
def test_authenticate_user_success(ccg_auth, user, mock_user_id):
    with mock.patch.object(CCGAuth, '_fetch_access_token', return_value='new_token') as fetch_access_token_mock:
        ccg_auth.authenticate_user(user)

        fetch_access_token_mock.assert_called_once_with(mock_user_id, USER_SUBJECT_TYPE, None)
        assert ccg_auth._user_id == mock_user_id  # pylint:disable=protected-access


@pytest.mark.parametrize('ccg_user_id', (None,))
@pytest.mark.parametrize('ccg_enterprise_id', (None,))
def test_authenticate_user_throws_error_when_user_not_provided(ccg_auth):
    with pytest.raises(ValueError):
        ccg_auth.authenticate_user(None)


@pytest.mark.parametrize('ccg_user_id, ccg_enterprise_id, enterprise_id',
                         [
                             (None, lazy_fixture('mock_enterprise_id'), None),
                             (None, None, lazy_fixture('mock_enterprise_id'))
                         ])
def test_authenticate_enterprise(ccg_auth, enterprise_id, mock_enterprise_id):
    with mock.patch.object(CCGAuth, '_fetch_access_token', return_value='new_token') as fetch_access_token_mock:
        ccg_auth.authenticate_instance(enterprise_id)

        fetch_access_token_mock.assert_called_once_with(mock_enterprise_id, ENTERPRISE_SUBJECT_TYPE, None)
        assert ccg_auth._enterprise_id == mock_enterprise_id  # pylint:disable=protected-access
        assert ccg_auth._user_id is None  # pylint:disable=protected-access


@pytest.mark.parametrize('ccg_user_id, ccg_enterprise_id, enterprise_id',
                         [
                             (None, None, None),
                             (None, lazy_fixture('mock_enterprise_id'), 'other_enterprise_300')
                         ])
def test_authenticate_user_throws_error_when_enetrprise_not_provided_or_conflicts(ccg_auth, enterprise_id):
    with pytest.raises(ValueError):
        ccg_auth.authenticate_instance(enterprise_id)


@pytest.mark.parametrize('ccg_user_id', (lazy_fixture('mock_user_id'),))
@pytest.mark.parametrize('ccg_enterprise_id', (lazy_fixture('mock_enterprise_id'),))
@pytest.mark.parametrize('status_code', (400, 401))
@pytest.mark.parametrize('error_description', ('invalid box_sub_type claim', 'invalid kid', "check the 'exp' claim"))
@pytest.mark.parametrize('error_code', ('invalid_grant', 'bad_request'))
@pytest.mark.parametrize('include_date_header', (True, False))
def test_auth_retry_for_invalid_exp_claim(
        ccg_auth,
        status_code,
        expect_auth_retry,
        unsuccessful_ccg_response,
        box_datetime,
        mock_enterprise_id
):
    side_effect = [BoxOAuthException(status_code, network_response=unsuccessful_ccg_response), 'jwt_token']
    with mock.patch.object(CCGAuth, '_fetch_access_token', return_value='new_token', side_effect=side_effect) as fetch_access_token_mock:

        if not expect_auth_retry:
            with pytest.raises(BoxOAuthException):
                ccg_auth.authenticate_instance()
        else:
            ccg_auth.authenticate_instance()

        expected_calls = [call(mock_enterprise_id, 'enterprise', None)]
        if expect_auth_retry:
            expected_calls.append(call(mock_enterprise_id, 'enterprise', box_datetime.replace(microsecond=0, tzinfo=None)))
        assert len(fetch_access_token_mock.mock_calls) == len(expected_calls)
        fetch_access_token_mock.assert_has_calls(expected_calls)


@pytest.mark.parametrize('ccg_user_id', (lazy_fixture('mock_user_id'),))
@pytest.mark.parametrize('ccg_enterprise_id', (lazy_fixture('mock_enterprise_id'),))
@pytest.mark.parametrize('status_code, error_description, error_code',
                         [(429, 'Request rate limit exceeded', 'rate_limit_exceeded'),
                          (500, 'Internal Server Error', 'internal_server_error')])
@pytest.mark.parametrize('include_date_header', (False,))
def test_auth_retry_for_rate_limit_and_server_errors(
        unsuccessful_ccg_response,
        ccg_auth,
        status_code,
        mock_enterprise_id
):

    side_effect = []
    expected_calls = []
    # Retries multiple times, but less than max retries. Then succeeds when it gets a token.
    for _ in range(API.MAX_RETRY_ATTEMPTS - 2):
        side_effect.append(BoxOAuthException(status_code, network_response=unsuccessful_ccg_response))
        expected_calls.append(call(mock_enterprise_id, ENTERPRISE_SUBJECT_TYPE, None))
    side_effect.append('jwt_token')
    expected_calls.append(call(mock_enterprise_id, 'enterprise', None))
    with mock.patch.object(CCGAuth, '_fetch_access_token', return_value='new_token', side_effect=side_effect) as fetch_access_token_mock:

        ccg_auth.authenticate_instance(mock_enterprise_id)

        assert len(fetch_access_token_mock.mock_calls) == len(expected_calls)
        fetch_access_token_mock.assert_has_calls(expected_calls)


@pytest.mark.parametrize('ccg_user_id', (lazy_fixture('mock_user_id'),))
@pytest.mark.parametrize('ccg_enterprise_id', (lazy_fixture('mock_enterprise_id'),))
@pytest.mark.parametrize('status_code, error_description, error_code',
                         [(429, 'Request rate limit exceeded', 'rate_limit_exceeded'),
                          (500, 'Internal Server Error', 'internal_server_error')])
@pytest.mark.parametrize('include_date_header', (False,))
def test_auth_max_retries_for_rate_limit_and_server_errors(
        unsuccessful_ccg_response,
        ccg_auth,
        status_code,
        mock_enterprise_id
):

    side_effect = []
    expected_calls = []
    # Retries multiple times, but less than max retries. Then succeeds when it gets a token.
    for _ in range(API.MAX_RETRY_ATTEMPTS + 1):
        side_effect.append(BoxOAuthException(status_code, network_response=unsuccessful_ccg_response))
        expected_calls.append(call(mock_enterprise_id, ENTERPRISE_SUBJECT_TYPE, None))
    with mock.patch.object(CCGAuth, '_fetch_access_token', return_value='new_token', side_effect=side_effect) as fetch_access_token_mock:

        with pytest.raises(BoxOAuthException) as error:
            ccg_auth.authenticate_instance(mock_enterprise_id)

        assert error.value.status == status_code
        assert len(fetch_access_token_mock.mock_calls) == len(expected_calls)
        fetch_access_token_mock.assert_has_calls(expected_calls)


@pytest.mark.parametrize('ccg_user_id', (lazy_fixture('mock_user_id'),))
@pytest.mark.parametrize('ccg_enterprise_id', (lazy_fixture('mock_enterprise_id'),))
def test_extract_token_from_success_response(
        successful_token_response,
        successful_token_json_response,
        ccg_auth,
        mock_enterprise_id
):
    with mock.patch.object(CCGAuth, '_execute_token_request', return_value=successful_token_response):

        ccg_auth.authenticate_instance(mock_enterprise_id)

        assert ccg_auth.access_token == successful_token_json_response['access_token']


@pytest.mark.parametrize('ccg_user_id', (lazy_fixture('mock_user_id'),))
@pytest.mark.parametrize('ccg_enterprise_id', (None,))
def test_refresh_client_authentication_when_client_id_is_provided(ccg_auth):
    ccg_auth.authenticate_instance = Mock()
    ccg_auth.authenticate_user = Mock()

    ccg_auth.refresh("expired_token")

    ccg_auth.authenticate_user.assert_called_once()
    ccg_auth.authenticate_instance.assert_not_called()


@pytest.mark.parametrize('ccg_user_id', (None,))
@pytest.mark.parametrize('ccg_enterprise_id', (lazy_fixture('mock_enterprise_id'),))
def test_refresh_enterprise_authentication_when_client_id_is_not_provided(ccg_auth):
    ccg_auth.authenticate_instance = Mock()
    ccg_auth.authenticate_user = Mock()

    ccg_auth.refresh("expired_token")

    ccg_auth.authenticate_user.assert_not_called()
    ccg_auth.authenticate_instance.assert_called_once()


@pytest.mark.parametrize('ccg_user_id', (lazy_fixture('mock_user_id'),))
@pytest.mark.parametrize('ccg_enterprise_id', (lazy_fixture('mock_enterprise_id'),))
@pytest.mark.parametrize('subject_id, subject_type',
                         [
                             (lazy_fixture('mock_user_id'), USER_SUBJECT_TYPE),
                             (lazy_fixture('mock_enterprise_id'), ENTERPRISE_SUBJECT_TYPE)
                         ])
def test_send_authentication_request_with_correct_params(
        ccg_auth,
        client_id,
        client_secret,
        subject_id,
        subject_type
):
    expected_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'box_subject_id': subject_id,
        'box_subject_type': subject_type
    }
    ccg_auth.send_token_request = Mock(return_value=('new_token', None))

    # pylint:disable=protected-access
    ccg_auth._fetch_access_token(subject_id, subject_type, None)

    ccg_auth.send_token_request.assert_called_once_with(expected_data, access_token=None, expect_refresh_token=False)
