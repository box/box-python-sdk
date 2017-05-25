# coding: utf-8

from __future__ import unicode_literals, absolute_import

from six.moves import input  # pylint:disable=redefined-builtin

from .oauth2 import OAuth2


class DeveloperTokenAuth(OAuth2):
    ENTER_TOKEN_PROMPT = 'Enter developer token: '

    def __init__(self, get_new_token_callback=None, **kwargs):
        self._get_new_token = get_new_token_callback
        super(DeveloperTokenAuth, self).__init__(
            client_id=None,
            client_secret=None,
            access_token=self._refresh_developer_token(),
            **kwargs
        )

    def _refresh_developer_token(self):
        if self._get_new_token is not None:
            return self._get_new_token()
        else:
            return input(self.ENTER_TOKEN_PROMPT)

    def _refresh(self, access_token):
        """
        Base class override.
        Ask for a new developer token.
        """
        self._access_token = self._refresh_developer_token()
        return self._access_token, None

    def revoke(self):
        """
        Base class override.
        Do nothing; developer tokens can't be revoked without client ID and secret.
        """
