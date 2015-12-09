# coding: utf-8

from __future__ import unicode_literals

from aplus import Promise

from .default_network_async import DefaultNetworkAsync
from .network_interface import Network


class DefaultNetwork(Network):
    """Implementation of the network interface using the requests library."""

    def __init__(self):
        super(DefaultNetwork, self).__init__()
        self._network = DefaultNetworkAsync()

    def request(self, method, url, access_token, **kwargs):
        """Base class override.
        Make a network request using the default async network.
        """
        return Promise.fulfilled(self._network.request(method, url, access_token, **kwargs))

    def retry_after(self, delay, request_method, *args, **kwargs):
        """Base class override.
        Retry after sleeping for delay seconds.
        """
        return Promise.fulfilled(self._network.retry_after(delay, request_method, *args, **kwargs))
