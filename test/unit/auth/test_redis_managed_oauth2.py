# coding: utf-8

import uuid

from mock import Mock, patch

from boxsdk.auth import redis_managed_oauth2


def test_redis_managed_oauth2_gets_tokens_from_redis_on_init(access_token, refresh_token):
    redis_server = Mock(redis_managed_oauth2.StrictRedis)
    redis_server.hvals.return_value = access_token, refresh_token
    unique_id = Mock()
    oauth2 = redis_managed_oauth2.RedisManagedOAuth2(
        client_id=None,
        client_secret=None,
        unique_id=unique_id,
        redis_server=redis_server,
    )
    redis_server.hvals.assert_called_once_with(unique_id)
    assert oauth2.unique_id is unique_id


def test_redis_managed_oauth2_gets_tokens_from_redis_during_refresh(access_token, refresh_token, new_access_token):
    new_refresh_token = uuid.uuid4().hex
    redis_server = Mock(redis_managed_oauth2.StrictRedis)
    redis_server.hvals.return_value = new_access_token, new_refresh_token
    unique_id = Mock()
    oauth2 = redis_managed_oauth2.RedisManagedOAuth2(
        access_token=access_token,
        refresh_token=refresh_token,
        client_id=None,
        client_secret=None,
        unique_id=unique_id,
        redis_server=redis_server,
    )
    assert oauth2.access_token == access_token
    redis_server.hvals.assert_not_called()

    assert oauth2.refresh('bogus_access_token') == (new_access_token, new_refresh_token)
    assert oauth2.access_token == new_access_token
    redis_server.hvals.assert_called_once_with(unique_id)


def test_redis_managed_oauth2_stores_tokens_to_redis_during_refresh(
        access_token,
        refresh_token,
        mock_box_session,
        successful_token_response,
):
    redis_server = Mock(redis_managed_oauth2.StrictRedis)
    redis_server.hvals.return_value = access_token, refresh_token
    unique_id = Mock()
    with patch.object(redis_managed_oauth2.RedisManagedOAuth2, '_update_current_tokens'):
        oauth2 = redis_managed_oauth2.RedisManagedOAuth2(
            client_id=None,
            client_secret=None,
            unique_id=unique_id,
            redis_server=redis_server,
            session=mock_box_session,
        )
    mock_box_session.request.return_value = successful_token_response
    oauth2.send_token_request({}, access_token=None, expect_refresh_token=True)
    redis_server.hmset.assert_called_once_with(unique_id, {'access': access_token, 'refresh': refresh_token})
