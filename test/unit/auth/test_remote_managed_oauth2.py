# coding: utf-8

from mock import Mock

from boxsdk.auth import remote_managed_oauth2


def test_remote_managed_oauth2_calls_retrieve_tokens_during_refresh(access_token):
    retrieve_access_token = Mock()
    oauth2 = remote_managed_oauth2.RemoteOAuth2(
        retrieve_access_token=retrieve_access_token,
        client_id=None,
        client_secret=None,
        access_token=access_token,
    )
    retrieve_access_token.return_value = access_token
    assert oauth2.refresh(access_token) == (access_token, None)
    retrieve_access_token.assert_called_once_with(access_token)
