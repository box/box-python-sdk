# coding: utf-8

from __future__ import unicode_literals, absolute_import

from mock import Mock, patch
from boxsdk.auth import developer_token_auth


def test_developer_token_auth_calls_callback_during_init_and_refresh(access_token):
    get_new_token_callback = Mock()
    get_new_token_callback.return_value = access_token
    auth = developer_token_auth.DeveloperTokenAuth(
        get_new_token_callback=get_new_token_callback,
    )
    assert auth.access_token == access_token
    get_new_token_callback.assert_called_once_with()
    assert auth.refresh(access_token) == (access_token, None)
    assert len(get_new_token_callback.mock_calls) == 2


def test_developer_token_auth_uses_raw_input_by_default(access_token):
    with patch('boxsdk.auth.developer_token_auth.input', create=True) as mock_raw_input:
        mock_raw_input.return_value = access_token
        auth = developer_token_auth.DeveloperTokenAuth()
        mock_raw_input.assert_called_once_with(auth.ENTER_TOKEN_PROMPT)
        assert auth.access_token == access_token
        assert auth.refresh(access_token) == (access_token, None)
        assert len(mock_raw_input.mock_calls) == 2
