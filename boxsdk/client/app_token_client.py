# coding: utf-8

from __future__ import unicode_literals, absolute_import

from ..auth import OAuth2
from .client import Client


class AppTokenClient(Client):
    """
    Box client subclass which authorizes with a developer token.
    """
    def __init__(self, access_token, network_layer=None, session=None):
        oauth = OAuth2(
            client_id=None,
            client_secret=None,
            access_token=access_token,
        )
        super(AppTokenClient, self).__init__(
            oauth=oauth,
            network_layer=network_layer,
            session=session,
        )
