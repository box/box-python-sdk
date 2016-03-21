# coding: utf-8

from __future__ import unicode_literals, absolute_import

from ..auth import DeveloperTokenAuth
from .client import Client


class DeveloperTokenClient(Client):
    """
    Box client subclass which authorizes with a developer token.
    """
    def __init__(self, oauth=None, network_layer=None, session=None):
        super(DeveloperTokenClient, self).__init__(
            oauth=oauth or DeveloperTokenAuth(),
            network_layer=network_layer,
            session=session,
        )
