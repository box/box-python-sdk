# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .client import Client
from ..network.logging_network import LoggingNetwork


class LoggingClient(Client):
    """
    Box client subclass which logs requests and responses.
    """
    def __init__(self, oauth=None, network_layer=None, session=None):
        super(LoggingClient, self).__init__(
            oauth=oauth,
            network_layer=network_layer or LoggingNetwork(),
            session=session,
        )
