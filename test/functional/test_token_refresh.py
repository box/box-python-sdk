# coding: utf-8

import pytest
from boxsdk.exception import BoxOAuthException


def test_expired_access_token_is_refreshed(box_oauth, box_client, mock_box):
    # pylint:disable=protected-access
    mock_box.oauth.expire_token(box_oauth._access_token)
    # pylint:enable=protected-access
    box_client.folder('0').get()
    assert len(mock_box.requests) == 6  # GET /authorize, POST /authorize, /token, get_info, refresh /token, get_info


def test_expired_refresh_token_raises(box_oauth, box_client, mock_box):
    # pylint:disable=protected-access
    mock_box.oauth.expire_token(box_oauth._access_token)
    mock_box.oauth.expire_token(box_oauth._refresh_token)
    # pylint:enable=protected-access
    with pytest.raises(BoxOAuthException):
        box_client.folder('0').get()
