# coding: utf-8
from typing import Any

from .client import Client
from ..util.log import setup_logging


class LoggingClient(Client):
    """
    Box client subclass which logs requests and responses.
    """
    def __init__(self, *args: Any, **kwargs: Any):
        setup_logging(None)
        super().__init__(*args, **kwargs)
