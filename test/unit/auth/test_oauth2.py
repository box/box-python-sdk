# coding: utf-8

from functools import partial
import re
from threading import Thread
import uuid
from urllib import parse

from mock import Mock, patch
import pytest

from boxsdk.exception import BoxOAuthException
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.auth.oauth2 import OAuth2
from boxsdk.config import API


class MyError(Exception):
    pass


class MyBaseException(BaseException):
    pass


@pytest.fixture(params=('https://url.com/foo?bar=baz', 'https://ȕŕľ.com/ƒőő?Ƅȁŕ=Ƅȁż', None))
def redirect_url(request):
    """A value for the `redirect_uri` query string parameter for OAuth2."""
    return request.param


def test_get_correct_authorization_url(redirect_url):
    # pylint:disable=redefined-outer-name
    fake_client_id = 'fake_client_id'
    fake_client_secret = 'fake_client_secret'
    oauth2 = OAuth2(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
    )
    auth_url, csrf_token = oauth2.get_authorization_url(redirect_url=redirect_url)
    expected_auth_url_format = '{0}?state={1}&response_type=code&client_id={2}'
    if redirect_url:
        expected_auth_url_format += '&redirect_uri={3}'
    assert auth_url == expected_auth_url_format.format(
        API.OAUTH2_AUTHORIZE_URL,
        csrf_token,
        fake_client_id,
        parse.quote_plus((redirect_url or '').encode('utf-8')),
    )
    assert re.match('^box_csrf_token_[A-Za-z0-9]{16}$', csrf_token)


def test_authenticate_send_post_request_with_correct_params(mock_box_session, successful_token_response):
    fake_client_id = 'fake_client_id'
    fake_client_secret = 'fake_client_secret'
    fake_auth_code = 'fake_auth_code'
    data = {
        'grant_type': 'authorization_code',
        'code': fake_auth_code,
        'client_id': fake_client_id,
        'client_secret': fake_client_secret,
        'box_device_id': '0',
        'box_device_name': 'my_awesome_device',
    }
    mock_box_session.request.return_value = successful_token_response
    oauth = OAuth2(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
        session=mock_box_session,
        box_device_name='my_awesome_device',
    )

    oauth.authenticate(fake_auth_code)

    mock_box_session.request.assert_called_once_with(
        'POST',
        f'{API.OAUTH2_API_URL}/token',
        data=data,
        headers={'content-type': 'application/x-www-form-urlencoded'},
        access_token=None,
    )

    assert oauth.access_token == successful_token_response.json()['access_token']


@pytest.mark.parametrize('_', range(10))
def test_refresh_send_post_request_with_correct_params_and_handles_multiple_requests(
        mock_box_session,
        successful_token_response,
        _,
):
    fake_client_id = 'fake_client_id'
    fake_client_secret = 'fake_client_secret'
    fake_refresh_token = 'fake_refresh_token'
    fake_access_token = 'fake_access_token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': fake_refresh_token,
        'client_id': fake_client_id,
        'client_secret': fake_client_secret,
        'box_device_id': '0',
        'box_device_name': 'my_awesome_device',
    }
    mock_box_session.request.return_value = successful_token_response
    oauth = OAuth2(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
        access_token=fake_access_token,
        refresh_token=fake_refresh_token,
        session=mock_box_session,
        box_device_name='my_awesome_device',
    )

    # Create four threads to call refresh on oauth at the same time.
    threads = []
    for _ in range(4):
        threads.append(Thread(target=oauth.refresh, args=(fake_access_token,)))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Assert that even four threads were trying to refresh the tokens at the same time, only one token request was made,
    # and it was made with the correct params.
    mock_box_session.request.assert_called_once_with(
        'POST',
        f'{API.OAUTH2_API_URL}/token',
        data=data,
        headers={'content-type': 'application/x-www-form-urlencoded'},
        access_token=fake_access_token,
    )


def test_authenticate_stores_tokens_correctly(mock_box_session, successful_token_response):
    fake_client_id = 'fake_client_id'
    fake_client_secret = 'fake_client_secret'
    fake_auth_code = 'fake_auth_code'

    mock_box_session.request.return_value = successful_token_response
    mock_token_callback = Mock()
    oauth = OAuth2(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
        session=mock_box_session,
        store_tokens=mock_token_callback,
    )

    access_token, refresh_token = oauth.authenticate(fake_auth_code)
    mock_token_callback.assert_called_once_with(access_token, refresh_token)

    assert access_token == successful_token_response.json()['access_token']
    assert refresh_token == successful_token_response.json()['refresh_token']


@pytest.mark.parametrize('_', range(10))
def test_refresh_gives_back_the_correct_response_and_handles_multiple_requests(
        mock_box_session,
        successful_token_response,
        network_response_with_missing_tokens,
        _,
):
    # pylint:disable=redefined-outer-name
    fake_client_id = 'fake_client_id'
    fake_client_secret = 'fake_client_secret'
    fake_refresh_token = 'fake_refresh_token'
    fake_access_token = 'fake_access_token'

    # Setup the network layer so that if oauth makes more than one request, it will get a malformed response and failed
    # the test.
    mock_box_session.request.side_effect = [successful_token_response, network_response_with_missing_tokens]
    oauth = OAuth2(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
        access_token=fake_access_token,
        refresh_token=fake_refresh_token,
        session=mock_box_session,
    )

    def refresh_tokens_and_verify_the_response():
        access_token, refresh_token = oauth.refresh(fake_access_token)
        assert access_token == successful_token_response.json()['access_token']
        assert refresh_token == successful_token_response.json()['refresh_token']

    # Creates four threads and do token refresh at the same time. Assert they all get the same new access token and
    # refresh token.
    threads = []
    for _ in range(4):
        threads.append(Thread(target=refresh_tokens_and_verify_the_response))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


@pytest.fixture()
def token_method(request):
    """ Fixture that returns a partial method based on the method provided in request.param"""
    if request.param == OAuth2.refresh:
        return partial(OAuth2.refresh, access_token_to_refresh='fake_access_token')
    if request.param == OAuth2.authenticate:
        return partial(OAuth2.authenticate, auth_code='fake_code')
    return None


@pytest.mark.parametrize(
    'token_method',
    [OAuth2.refresh, OAuth2.authenticate],
    indirect=True,
)
def test_token_request_raises_box_oauth_exception_when_getting_bad_network_response(
        token_method,
        mock_box_session,
        bad_network_response,
):
    with pytest.raises(BoxOAuthException):
        mock_box_session.request.return_value = bad_network_response
        oauth = OAuth2(
            client_id='',
            client_secret='',
            access_token='fake_access_token',
            session=mock_box_session,
        )
        token_method(oauth)


@pytest.mark.parametrize(
    'token_method',
    [OAuth2.refresh, OAuth2.authenticate],
    indirect=True,
)
def test_token_request_raises_box_oauth_exception_when_no_json_object_can_be_decoded(
        token_method,
        mock_box_session,
        non_json_response,
):
    mock_box_session.request.return_value = non_json_response
    oauth = OAuth2(
        client_id='',
        client_secret='',
        access_token='fake_access_token',
        session=mock_box_session,
    )
    with pytest.raises(BoxOAuthException):
        token_method(oauth)


@pytest.fixture(params=[
    ['access_token'],
    ['refresh_token'],
    [],
])
def network_response_with_missing_tokens(request):
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    json_dict = {}
    for key in request.param:
        json_dict[key] = 'fake_token'
    mock_network_response.json.return_value = json_dict
    return mock_network_response


@pytest.mark.parametrize('test_method', [
    partial(OAuth2.refresh, access_token_to_refresh='fake_access_token'),
    partial(OAuth2.authenticate, auth_code='fake_code')
])
def test_token_request_raises_box_oauth_exception_when_tokens_are_not_in_the_response(
        test_method,
        mock_box_session,
        network_response_with_missing_tokens,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.request.return_value = network_response_with_missing_tokens
    oauth = OAuth2(
        client_id='',
        client_secret='',
        access_token='fake_access_token',
        session=mock_box_session,
    )
    with pytest.raises(BoxOAuthException):
        test_method(oauth)


def test_oauth_exception_error_and_error_description(mock_box_session, bad_network_response_400):
    mock_box_session.request.return_value = bad_network_response_400
    oauth = OAuth2(
        client_id='',
        client_secret='',
        access_token='fake_access_token',
        session=mock_box_session,
    )
    try:
        oauth.authenticate('fake_auth_code')
        pytest.fail('Should throw exception because of bad network response')
    except BoxOAuthException as exception:
        assert exception.code == 'Example Error'
        assert exception.message == 'Example Error Description'


def test_token_request_allows_missing_refresh_token(mock_box_session):
    mock_network_response = Mock()
    mock_network_response.ok = True
    mock_network_response.json.return_value = {'access_token': 'fake_token'}
    mock_box_session.request.return_value = mock_network_response
    oauth = OAuth2(
        client_id='',
        client_secret='',
        access_token='fake_access_token',
        session=mock_box_session,
    )
    oauth.send_token_request({}, access_token=None, expect_refresh_token=False)


@pytest.fixture()
def oauth(client_id, client_secret, access_token, refresh_token, mock_box_session):
    return OAuth2(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
        session=mock_box_session,
    )


@pytest.mark.parametrize(
    'access_token,refresh_token,expected_token_to_revoke',
    (
        ('fake_access_token', 'fake_refresh_token', 'fake_access_token'),
        (None, 'fake_refresh_token', 'fake_refresh_token')
    )
)
def test_revoke_sends_revoke_request(
        client_id,
        client_secret,
        mock_box_session,
        access_token,
        oauth,
        expected_token_to_revoke,
):
    mock_network_response = Mock()
    mock_network_response.ok = True
    mock_box_session.request.return_value = mock_network_response
    oauth.revoke()
    mock_box_session.request.assert_called_once_with(
        'POST',
        f'{API.OAUTH2_API_URL}/revoke',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'token': expected_token_to_revoke,
        },
        access_token=access_token,
    )
    assert oauth.access_token is None


def test_tokens_get_updated_after_noop_refresh(client_id, client_secret, access_token, new_access_token, refresh_token, mock_box_session):
    """`OAuth2` object should update its state with new tokens, after no-op refresh.

    If the protected method `_get_tokens()` returns new tokens, refresh is
    skipped, and those tokens are used.

    This is a regression test for issue #128 [1]. We would return the new
    tokens without updating the object state. Subsequent uses of the `OAuth2`
    object would use the old tokens.

    [1] <https://github.com/box/box-python-sdk/issues/128>
    """
    new_refresh_token = uuid.uuid4().hex
    new_tokens = (new_access_token, new_refresh_token)

    class GetTokensOAuth2(OAuth2):
        def _get_tokens(self):
            """Return a new set of tokens, without updating any state.

            In order for the test to pass, the `OAuth2` object must be
            correctly programmed to take this return value and use it to update
            its state.
            """
            return new_tokens

    oauth = GetTokensOAuth2(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
        session=mock_box_session,
    )
    assert oauth.access_token == access_token

    assert oauth.refresh(access_token) == new_tokens
    assert oauth.access_token == new_access_token


def test_closed_is_false_after_init(client_id, client_secret, mock_box_session):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, session=mock_box_session)
    assert auth.closed is False


def test_closed_is_true_after_close(client_id, client_secret, mock_box_session):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, session=mock_box_session)
    auth.close()
    assert auth.closed is True


def test_token_requests_fail_after_close(client_id, client_secret, mock_box_session):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, session=mock_box_session)
    auth.close()
    with pytest.raises(ValueError):
        auth.refresh(auth.access_token)


@pytest.mark.parametrize('raise_exception', [False, True])
def test_context_manager_closes_auth_object(client_id, client_secret, mock_box_session, raise_exception):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, session=mock_box_session)
    try:
        with auth.closing():
            if raise_exception:
                raise MyError
    except MyError:
        pass
    assert auth.closed is True


def test_context_manager_fails_after_close(client_id, client_secret, mock_box_session):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, session=mock_box_session)
    with auth.closing():
        pass
    with pytest.raises(ValueError):
        with auth.closing():
            assert False


@pytest.mark.parametrize(('close_args', 'close_kwargs'), [((), {}), ((True,), {}), ((), dict(revoke=True))])
def test_revoke_on_close(client_id, client_secret, access_token, mock_box_session, close_args, close_kwargs):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, access_token=access_token, session=mock_box_session)
    with patch.object(auth, 'revoke') as mock_revoke:
        auth.close(*close_args, **close_kwargs)
    mock_revoke.assert_called_once_with()


def test_auth_object_is_closed_even_if_revoke_fails(client_id, client_secret, access_token, mock_box_session):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, access_token=access_token, session=mock_box_session)
    with patch.object(auth, 'revoke', side_effect=BoxOAuthException(status=500)):
        with pytest.raises(BoxOAuthException):
            auth.close(revoke=True)
    assert auth.closed is True


@pytest.mark.parametrize(('close_args', 'close_kwargs'), [((False,), {}), ((), dict(revoke=False))])
def test_revoke_on_close_can_be_skipped(client_id, client_secret, access_token, mock_box_session, close_args, close_kwargs):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, access_token=access_token, session=mock_box_session)
    with patch.object(auth, 'revoke') as mock_revoke:
        auth.close(*close_args, **close_kwargs)
    mock_revoke.assert_not_called()


@pytest.mark.parametrize(('raise_from_block', 'raise_from_close', 'expected_exception'), [
    (MyError, None, MyError),
    (None, BoxOAuthException(status=500), BoxOAuthException),
    (MyError, BoxOAuthException(status=500), MyError),
])
@pytest.mark.parametrize('close_kwargs', [{}, dict(revoke=False), dict(revoke=True)])
def test_context_manager_reraises_first_exception_after_close(
        client_id, client_secret, mock_box_session, close_kwargs, raise_from_block, raise_from_close, expected_exception,
):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, session=mock_box_session)
    with patch.object(auth, 'close', side_effect=raise_from_close) as mock_close:
        with pytest.raises(expected_exception):
            with auth.closing(**close_kwargs):
                if raise_from_block:
                    raise raise_from_block
    mock_close.assert_called_once_with(**close_kwargs)


@pytest.mark.parametrize('close_kwargs', [{}, dict(revoke=False), dict(revoke=True)])
def test_context_manager_skips_revoke_on_base_exception(client_id, client_secret, mock_box_session, close_kwargs):
    auth = OAuth2(client_id=client_id, client_secret=client_secret, session=mock_box_session)
    with patch.object(auth, 'close') as mock_close:
        with pytest.raises(MyBaseException):
            with auth.closing(**close_kwargs):
                raise MyBaseException
    mock_close.assert_called_once_with(revoke=False)
