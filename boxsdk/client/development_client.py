# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .developer_token_client import DeveloperTokenClient
from ..util.log import setup_logging


class DevelopmentClient(DeveloperTokenClient):
    """
    Client subclass that uses developer token auth and logs requests and responses.
    Great for use in development!
    """
    def __init__(self, *args, **kwargs):
        setup_logging()
        super(DevelopmentClient, self).__init__(*args, **kwargs)