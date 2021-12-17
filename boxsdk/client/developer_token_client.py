# coding: utf-8

from ..auth import DeveloperTokenAuth
from .client import Client


class DeveloperTokenClient(Client):
    """
    Box client subclass which authorizes with a developer token.
    """
    def __init__(self, oauth=None, session=None):
        super().__init__(oauth=oauth or DeveloperTokenAuth(), session=session)
