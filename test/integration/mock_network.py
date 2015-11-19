# coding: utf-8

from __future__ import unicode_literals
from aplus import Promise
from six.moves.queue import Queue  # pylint:disable=import-error,no-name-in-module
from threading import Thread
from boxsdk.network.default_network_response import DefaultNetworkResponse
from boxsdk.network.network_interface import Network


class MockNetwork(Network):
    """Mock implementation of the network interface for testing purposes."""

    def __init__(self, session, async=True):
        super(MockNetwork, self).__init__()
        self._session = session
        self._retries = []
        self._async = async
        self._requests = Queue()
        self._fulfillment_thread = Thread(target=self._fulfill_requests)
        self._fulfillment_thread.start()

    def join(self):
        self._requests.put((None, None))
        self._requests.join()
        self._fulfillment_thread.join()

    def _fulfill_requests(self):
        while True:
            request, value = self._requests.get()
            if request is None:
                self._requests.task_done()
                break
            request.fulfill(value)
            self._requests.task_done()

    def request(self, method, url, access_token, **kwargs):
        """Base class override.
        Make a mock network request using a mock requests.Session.
        """
        promise = Promise()
        response = self._session.request(method, url, **kwargs)
        value = DefaultNetworkResponse(response, access_token)
        if self._async:
            self._requests.put((promise, value))
        else:
            promise.fulfill(value)
        return promise

    def retry_after(self, delay, request_method, *args, **kwargs):
        """Base class override.
        Retry immediately, recording the retry request.
        """
        self._retries.append((delay, request_method, args, kwargs))
        promise = Promise()
        value = request_method(*args, **kwargs)
        if self._async:
            self._requests.put((promise, value))
        else:
            promise.fulfill(value)
        return promise

    @property
    def session(self):
        return self._session
