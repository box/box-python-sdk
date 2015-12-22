# coding: utf-8

from __future__ import unicode_literals
from .oauth2 import OAuth2


class RemoteOAuth2Mixin(OAuth2):
    """
    Box SDK OAuth2 mixin.
    Allows for storing auth tokens remotely.

    """
    def __init__(self, retrieve_access_token=None, *args, **kwargs):
        """
        :param retrieve_access_token:
            Callback to exchange an existing access token for a new one.
        :type retrieve_access_token:
            `callable` of `unicode` => `unicode`
        """
        self._retrieve_access_token = retrieve_access_token
        super(RemoteOAuth2Mixin, self).__init__(*args, **kwargs)

    def _refresh(self, access_token):
        """
        Base class override. Ask the remote host for a new token.
        """
        self._access_token = self._retrieve_access_token(access_token)
        return self._access_token, None


class RemoteOAuth2(RemoteOAuth2Mixin):
    """
    Box SDK OAuth2 subclass.
    Allows for storing auth tokens remotely. The retrieve_access_token callback should
    return an access token, presumably acquired from a remote server on which your auth credentials are available.
    """
    pass
