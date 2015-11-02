# coding: utf-8

from __future__ import unicode_literals
from pprint import pformat
from boxsdk.network.default_network import DefaultNetwork
from boxsdk.util.log import setup_logging


class LoggingNetwork(DefaultNetwork):
    """
    SDK Network subclass that logs requests and responses.
    """
    LOGGER_NAME = 'boxsdk.network'
    REQUEST_FORMAT = '\x1b[36m%s %s %s\x1b[0m'
    SUCCESSFUL_RESPONSE_FORMAT = '\x1b[32m%s\x1b[0m'
    ERROR_RESPONSE_FORMAT = '\x1b[31m%s\n%s\n%s\n\x1b[0m'

    def __init__(self, logger=None):
        """
        :param logger:
            The logger to use. If you instantiate this class more than once, you should use the same logger
            to avoid duplicate log entries.
        :type logger:
            :class:`Logger`
        """
        super(LoggingNetwork, self).__init__()
        self._logger = logger or setup_logging(name=self.LOGGER_NAME)

    @property
    def logger(self):
        return self._logger

    def _log_request(self, method, url, **kwargs):
        """
        Logs information about the Box API request.

        :param method:
            The HTTP verb that should be used to make the request.
        :type method:
            `unicode`
        :param url:
            The URL for the request.
        :type url:
            `unicode`
        :param access_token:
            The OAuth2 access token used to authorize the request.
        :type access_token:
            `unicode`
        """
        self._logger.info(self.REQUEST_FORMAT, method, url, pformat(kwargs))

    def _log_response(self, response):
        """
        Logs information about the Box API response.

        :param response: The Box API response.
        """
        if response.ok:
            self._logger.info(self.SUCCESSFUL_RESPONSE_FORMAT, response.content)
        else:
            self._logger.warning(
                self.ERROR_RESPONSE_FORMAT,
                response.status_code,
                response.headers,
                pformat(response.content),
            )

    def request(self, method, url, access_token, **kwargs):
        """
        Base class override. Logs information about an API request and response in addition to making the request.
        """
        self._log_request(method, url, **kwargs)
        response = super(LoggingNetwork, self).request(method, url, access_token, **kwargs)
        self._log_response(response)
        return response
