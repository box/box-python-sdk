# coding: utf-8

from __future__ import unicode_literals
from redis import StrictRedis
from redis.lock import Lock
from uuid import uuid4
from boxsdk import JWTAuth, OAuth2


class RedisManagedOAuth2Mixin(OAuth2):
    """
    Box SDK OAuth2 subclass.
    Allows for storing auth tokens in redis.

    :param unique_id:
        An identifier for this auth object. Auth instances which wish to share tokens must use the same ID.
    :type unique_id:
        `unicode`
    :param redis_server:
        An instance of a Redis server, configured to talk to Redis.
    :type redis_server:
        :class:`Redis`
    """
    def __init__(self, unique_id=uuid4(), redis_server=None, *args, **kwargs):
        self._unique_id = unique_id
        self._redis_server = redis_server or StrictRedis()
        refresh_lock = Lock(redis=self._redis_server, name='{0}_lock'.format(self._unique_id))
        super(RedisManagedOAuth2Mixin, self).__init__(*args, refresh_lock=refresh_lock, **kwargs)
        if self._access_token is None:
            self._update_current_tokens()

    def _update_current_tokens(self):
        """
        Get the latest tokens from redis and store them.
        """
        self._access_token, self._refresh_token = self._redis_server.hvals(self._unique_id) or (None, None)

    @property
    def unique_id(self):
        """
        Get the unique ID used by this auth instance. Other instances can share tokens with this instance
        if they share the ID with this instance.
        """
        return self._unique_id

    def _get_tokens(self):
        """
        Base class override.
        Gets the latest tokens from redis before returning them.
        """
        self._update_current_tokens()
        return super(RedisManagedOAuth2Mixin, self)._get_tokens()

    def _store_tokens(self, access_token, refresh_token):
        """
        Base class override.
        Saves the refreshed tokens in redis.
        """
        super(RedisManagedOAuth2Mixin, self)._store_tokens(access_token, refresh_token)
        self._redis_server.hmset(self._unique_id, {'access': access_token, 'refresh': refresh_token})


class RedisManagedOAuth2(RedisManagedOAuth2Mixin):
    """
    OAuth2 subclass which uses Redis to manage tokens.
    """
    pass


class RedisManagedJWTAuth(RedisManagedOAuth2Mixin, JWTAuth):
    """
    JWT Auth subclass which uses Redis to manage access tokens.
    """
    def _auth_with_jwt(self, sub, sub_type):
        """
        Base class override. Returns the access token in a tuple to match the OAuth2 interface.
        """
        return super(RedisManagedJWTAuth, self)._auth_with_jwt(sub, sub_type), None
