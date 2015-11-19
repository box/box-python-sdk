# coding: utf-8

from __future__ import unicode_literals

import requests
import time

from .default_network_response import DefaultNetworkResponse
from .network_interface import Network


class DefaultNetworkSync(Network):
    """Implementation of the network interface using the requests library."""

    def __init__(self):
        super(DefaultNetworkSync, self).__init__()
        self._session = requests.Session()

    def request(self, method, url, access_token, **kwargs):
        """Base class override.
        Make a network request using a requests.Session.
        """
        return DefaultNetworkResponse(self._session.request(method, url, **kwargs), access_token)

    def retry_after(self, delay, request_method, *args, **kwargs):
        """Base class override.
        Retry after sleeping for delay seconds.
        """
        time.sleep(delay)
        return request_method(*args, **kwargs)
