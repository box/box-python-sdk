# coding: utf-8

from __future__ import unicode_literals
from .oauth2 import OAuth2


class CooperativelyManagedOAuth2Mixin(OAuth2):
    """
    Box SDK OAuth2 mixin.
    Allows for sharing auth tokens between multiple clients.
    """
    def __init__(self, retrieve_tokens=None, *args, **kwargs):
        """
        :param retrieve_tokens:
            Callback to get the current access/refresh token pair.
        :type retrieve_tokens:
            `callable` of () => (`unicode`, `unicode`)
        """
        self._retrieve_tokens = retrieve_tokens
        super(CooperativelyManagedOAuth2Mixin, self).__init__(*args, **kwargs)

    def _get_tokens(self):
        """
        Base class override. Get the tokens from the user-specified callback.
        """
        return self._retrieve_tokens()


class CooperativelyManagedOAuth2(CooperativelyManagedOAuth2Mixin):
    """
    Box SDK OAuth2 subclass.
    Allows for sharing auth tokens between multiple clients. The retrieve_tokens callback should
    return the current access/refresh token pair.
    """
    pass
