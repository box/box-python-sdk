# coding: utf-8

from __future__ import unicode_literals
from boxsdk import OAuth2


class RemoteOAuth2Mixin(OAuth2):
    """
    Box SDK OAuth2 subclass.
    Allows for storing auth tokens remotely.

    :param retrieve_access_token:
        Callback to exchange an existing access token for a new one.
    :type retrieve_access_token:
        `callable` of `unicode` => `unicode`
    """
    def __init__(self, retrieve_access_token=None, *args, **kwargs):
        self._retrieve_access_token = retrieve_access_token
        super(RemoteOAuth2Mixin, self).__init__(*args, **kwargs)

    def _refresh(self, access_token):
        """
        Base class override. Ask the remote host for a new token.
        """
        self._access_token = self._retrieve_access_token(access_token)
        return self._access_token, None
