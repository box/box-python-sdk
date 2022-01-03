# coding: utf-8

from mock import Mock
import requests
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.network.network_interface import Network


class MockNetwork(Network):
    """Mock implementation of the network interface for testing purposes."""

    def __init__(self):
        super().__init__()
        self._session = Mock(requests.Session)
        self._retries = []

    def request(self, method, url, access_token, **kwargs):
        """Base class override.
        Make a mock network request using a mock requests.Session.
        """
        return DefaultNetworkResponse(self._session.request(method, url, **kwargs), access_token)

    def retry_after(self, delay, request_method, *args, **kwargs):
        """Base class override.
        Retry immediately, recording the retry request.
        """
        self._retries.append((delay, request_method, args, kwargs))
        return request_method(*args, **kwargs)

    @property
    def session(self):
        return self._session
