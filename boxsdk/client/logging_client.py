# coding: utf-8

from .client import Client
from ..util.log import setup_logging


class LoggingClient(Client):
    """
    Box client subclass which logs requests and responses.
    """
    def __init__(self, *args, **kwargs):
        setup_logging(None)
        super().__init__(*args, **kwargs)
