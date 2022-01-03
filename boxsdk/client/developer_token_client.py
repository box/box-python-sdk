# coding: utf-8
from typing import TYPE_CHECKING

from ..auth import DeveloperTokenAuth
from .client import Client

if TYPE_CHECKING:
    from boxsdk import OAuth2
    from boxsdk.session.session import Session


class DeveloperTokenClient(Client):
    """
    Box client subclass which authorizes with a developer token.
    """
    def __init__(self, oauth: 'OAuth2' = None, session: 'Session' = None):
        super().__init__(oauth=oauth or DeveloperTokenAuth(), session=session)
