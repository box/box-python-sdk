# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .developer_token_client import DeveloperTokenClient
from .logging_client import LoggingClient


class DevelopmentClient(DeveloperTokenClient, LoggingClient):
    """
    Client subclass that uses developer token auth and logs requests and responses.
    Great for use in development!
    """
    pass
