# coding: utf-8

from __future__ import unicode_literals, absolute_import
from aplus import spawn
from functools import partial
from .default_network_sync import DefaultNetworkSync
from .network_interface import Network


class DefaultNetworkAsync(Network):
    """
    Implementation of the network interface using the requests library and aplus promises.
    """
    def __init__(self):
        super(DefaultNetworkAsync, self).__init__()
        self._sync_network = DefaultNetworkSync()

    def request(self, method, url, access_token, **kwargs):
        """
        Base class override.
        Make a network request using a requests.Session.
        """
        return spawn(partial(self._sync_network.request, method, url, access_token, **kwargs))

    def retry_after(self, delay, request_method, *args, **kwargs):
        """
        Base class override.
        Retry after sleeping for delay seconds.
        """
        return spawn(partial(self._sync_network.retry_after, delay, request_method, *args, **kwargs))
