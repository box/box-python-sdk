# coding: utf-8

from __future__ import unicode_literals

from functools import partial
import re
from threading import Thread
import uuid

from mock import Mock
import pytest
from six.moves import range   # pylint:disable=redefined-builtin
from six.moves.urllib import parse as urlparse  # pylint:disable=import-error,no-name-in-module,wrong-import-order

from boxsdk.exception import BoxOAuthException
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.auth.oauth2 import OAuth2
from boxsdk.config import API


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
        urlparse.quote_plus((redirect_url or '').encode('utf-8')),
    )
    assert re.match('^box_csrf_token_[A-Za-z0-9]{16}$', csrf_token)


def test_authenticate_send_post_request_with_correct_params(mock_network_layer, successful_token_response):
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
    mock_network_layer.request.return_value = successful_token_response
    oauth = OAuth2(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
        network_layer=mock_network_layer,
        box_device_name='my_awesome_device',
    )

    oauth.authenticate(fake_auth_code)

    mock_network_layer.request.assert_called_once_with(
        'POST',
        '{0}/token'.format(API.OAUTH2_API_URL),
        data=data,
        headers={'content-type': 'application/x-www-form-urlencoded'},
        access_token=None,
    )

    assert oauth.access_token == successful_token_response.json()['access_token']


@pytest.mark.parametrize('_', range(10))
def test_refresh_send_post_request_with_correct_params_and_handles_multiple_requests(
        mock_network_layer,
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
    mock_network_layer.request.return_value = successful_token_response
    oauth = OAuth2(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
        access_token=fake_access_token,
        refresh_token=fake_refresh_token,
        network_layer=mock_network_layer,
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
    mock_network_layer.request.assert_called_once_with(
        'POST',
        '{0}/token'.format(API.OAUTH2_API_URL),
        data=data,
        headers={'content-type': 'application/x-www-form-urlencoded'},
        access_token=fake_access_token,
    )


def test_authenticate_stores_tokens_correctly(mock_network_layer, successful_token_response):
    fake_client_id = 'fake_client_id'
    fake_client_secret = 'fake_client_secret'
    fake_auth_code = 'fake_auth_code'

    mock_network_layer.request.return_value = successful_token_response
    mock_token_callback = Mock()
    oauth = OAuth2(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
        network_layer=mock_network_layer,
        store_tokens=mock_token_callback,
    )

    access_token, refresh_token = oauth.authenticate(fake_auth_code)
    mock_token_callback.assert_called_once_with(access_token, refresh_token)

    assert access_token == successful_token_response.json()['access_token']
    assert refresh_token == successful_token_response.json()['refresh_token']


@pytest.mark.parametrize('_', range(10))
def test_refresh_gives_back_the_correct_response_and_handles_multiple_requests(
        mock_network_layer,
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
    mock_network_layer.request.side_effect = [successful_token_response, network_response_with_missing_tokens]
    oauth = OAuth2(
        client_id=fake_client_id,
        client_secret=fake_client_secret,
        access_token=fake_access_token,
        refresh_token=fake_refresh_token,
        network_layer=mock_network_layer,
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


@pytest.mark.parametrize('test_method', [
    partial(OAuth2.refresh, access_token_to_refresh='fake_access_token'),
    partial(OAuth2.authenticate, auth_code='fake_code')
])
def test_token_request_raises_box_oauth_exception_when_getting_bad_network_response(
        test_method,
        mock_network_layer,
        bad_network_response,
):
    with pytest.raises(BoxOAuthException):
        mock_network_layer.request.return_value = bad_network_response
        oauth = OAuth2(
            client_id='',
            client_secret='',
            access_token='fake_access_token',
            network_layer=mock_network_layer,
        )
        test_method(oauth)


@pytest.mark.parametrize('test_method', [
    partial(OAuth2.refresh, access_token_to_refresh='fake_access_token'),
    partial(OAuth2.authenticate, auth_code='fake_code')
])
def test_token_request_raises_box_oauth_exception_when_no_json_object_can_be_decoded(
        test_method,
        mock_network_layer,
        non_json_response,
):
    mock_network_layer.request.return_value = non_json_response
    oauth = OAuth2(
        client_id='',
        client_secret='',
        access_token='fake_access_token',
        network_layer=mock_network_layer,
    )
    with pytest.raises(BoxOAuthException):
        test_method(oauth)


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
        mock_network_layer,
        network_response_with_missing_tokens,
):
    # pylint:disable=redefined-outer-name
    mock_network_layer.request.return_value = network_response_with_missing_tokens
    oauth = OAuth2(
        client_id='',
        client_secret='',
        access_token='fake_access_token',
        network_layer=mock_network_layer,
    )
    with pytest.raises(BoxOAuthException):
        test_method(oauth)


def test_token_request_allows_missing_refresh_token(mock_network_layer):
    mock_network_response = Mock()
    mock_network_response.ok = True
    mock_network_response.json.return_value = {'access_token': 'fake_token'}
    mock_network_layer.request.return_value = mock_network_response
    oauth = OAuth2(
        client_id='',
        client_secret='',
        access_token='fake_access_token',
        network_layer=mock_network_layer,
    )
    oauth.send_token_request({}, access_token=None, expect_refresh_token=False)


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
        mock_network_layer,
        access_token,
        refresh_token,
        expected_token_to_revoke,
):
    mock_network_response = Mock()
    mock_network_response.ok = True
    mock_network_layer.request.return_value = mock_network_response
    oauth = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
        network_layer=mock_network_layer,
    )
    oauth.revoke()
    mock_network_layer.request.assert_called_once_with(
        'POST',
        '{0}/revoke'.format(API.OAUTH2_API_URL),
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'token': expected_token_to_revoke,
        },
        access_token=access_token,
    )
    assert oauth.access_token is None


def test_tokens_get_updated_after_noop_refresh(client_id, client_secret, access_token, new_access_token, refresh_token, mock_network_layer):
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
        network_layer=mock_network_layer,
    )
    assert oauth.access_token == access_token

    assert oauth.refresh(access_token) == new_tokens
    assert oauth.access_token == new_access_token
