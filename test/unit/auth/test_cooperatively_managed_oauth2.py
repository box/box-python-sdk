# coding: utf-8

from __future__ import unicode_literals, absolute_import

from mock import Mock

from boxsdk.auth import cooperatively_managed_oauth2


def test_cooperatively_managed_oauth2_calls_retrieve_tokens_during_refresh(access_token, refresh_token):
    retrieve_tokens = Mock()
    oauth2 = cooperatively_managed_oauth2.CooperativelyManagedOAuth2(
        retrieve_tokens=retrieve_tokens,
        client_id=None,
        client_secret=None,
    )
    retrieve_tokens.return_value = access_token, refresh_token
    assert oauth2.refresh(None) == (access_token, refresh_token)
    retrieve_tokens.assert_called_once_with()
