# coding: utf-8

from __future__ import absolute_import, unicode_literals

from functools import partial
from pprint import pformat
import sys

from six import text_type

from boxsdk.network.default_network import DefaultNetwork, DefaultNetworkResponse
from boxsdk.util.log import setup_logging


class LoggingNetwork(DefaultNetwork):
    """
    SDK Network subclass that logs requests and responses.
    """
    LOGGER_NAME = 'boxsdk.network'
    REQUEST_FORMAT = '\x1b[36m%(method)s %(url)s %(request_kwargs)s\x1b[0m'
    EXCEPTION_FORMAT = '\x1b[31mRequest "%(method)s %(url)s" failed with %(exc_type_name)s exception: %(exc_value)r\x1b[0m'
    _COMMON_RESPONSE_FORMAT = '"%(method)s %(url)s" %(status_code)s %(content_length)s\n%(headers)s\n%(content)s\n'
    SUCCESSFUL_RESPONSE_FORMAT = '\x1b[32m{0}\x1b[0m'.format(_COMMON_RESPONSE_FORMAT)
    ERROR_RESPONSE_FORMAT = '\x1b[31m{0}\x1b[0m'.format(_COMMON_RESPONSE_FORMAT)

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
        self._logger.info(self.REQUEST_FORMAT, {'method': method, 'url': url, 'request_kwargs': pformat(kwargs)})

    def _log_exception(self, method, url, exc_info):
        """Log information at WARNING level about the exception that was raised when trying to make the request.

        :param method:  The HTTP verb that was used to make the request.
        :type method:   `unicode`
        :param url:   The URL for the request.
        :type url:  `unicode`
        :param exc_info:  The exception info returned from `sys.exc_info()`.
        """
        exc_type, exc_value, _ = exc_info
        self._logger.warning(
            self.EXCEPTION_FORMAT,
            {'method': method, 'url': url, 'exc_type_name': exc_type.__name__, 'exc_value': exc_value},
        )

    def request(self, method, url, access_token, **kwargs):
        """
        Base class override. Logs information about an API request and response in addition to making the request.

        Also logs exceptions before re-raising them.

        The logging of the response is deferred to
        :class:`LoggingNetworkResponse`. See that class's docstring for more
        info.
        """
        self._log_request(method, url, **kwargs)
        try:
            return super(LoggingNetwork, self).request(method, url, access_token, **kwargs)
        except Exception:
            self._log_exception(method, url, sys.exc_info())
            raise

    @property
    def network_response_constructor(self):
        """Baseclass override.

        A callable that passes additional required keyword arguments to the
        :class:`LoggingNetworkResponse` constructor, and returns an instance of
        :class:`LoggingNetworkResponse`.
        """
        return partial(
            LoggingNetworkResponse,
            logger=self._logger,
            successful_response_format=self.SUCCESSFUL_RESPONSE_FORMAT,
            error_response_format=self.ERROR_RESPONSE_FORMAT,
        )


class LoggingNetworkResponse(DefaultNetworkResponse):
    """Response subclass that defers LoggingNetwork response logging until it is safe to do so.

    :class:`DefaultNetwork` is based off the `requests` library.
    :class:`requests.Response` has a few mutually-exclusive ways to read the
    content of the response:

        - With the `Response.raw` attribute, an `io.IOBase` instance returned
          from the `urllib3` library, that can be read once in chunks from
          beginning to end.
        - With `Response.iter_content()` and other iter_* generators, which
          also can only be read once and advance the `Response.raw` IO stream.
        - With the `Response.content` property (and other attributes such as
          `Response.text` and `Response.json()`), which reads and caches the
          remaining response content in memory. Can be accessed multiple times,
          but cannot be safely accessed if any of the previous mechanisms have
          been used at all. And if this property has already been accessed,
          then the other mechanisms will have been exhausted, and attempting to
          read from them will make it appear like the response content is
          empty.

    Any of these mechanisms may be used to read any response, regardless of
    whether `stream=True` or `stream=False` on the request.

    If the caller uses `Response.content`, then it is safe for
    :class:`LoggingNetwork` to also access it. But if the caller uses any of
    the streaming mechanisms, then it is not safe for :class:`LoggingNetwork`
    to ever read any of the content. Thus, the options available are:

        - Never log the content of a response.
        - Make logging part of the :class:`Network` interface, and add an
          optional keyword argument that callers can use to specify when it is
          unsafe to log the content of a response.
        - Defer logging until it is possible to auto-detect which mechanism is
          being used.

    This class is an implementation of the latter option. Instead of response
    logging taking place in `LoggingNetwork.request()`, it takes place in this
    `DefaultNetworkResponse` subclass, as soon as the caller starts reading the
    content. If `content` or `json()` are accessed, then the response will be
    logged with its content. Whereas if `response_as_stream` or
    `request_response` are accessed, then the response will be logged with a
    placeholder for the actual content.

    In theory, this could make the logs less useful, by adding a delay between
    when the network response was actually received, and when it is logged. Or
    the response may never be logged, if the content is never accessed. In
    practice, this is unlikely to happen, because nearly all SDK methods
    immediately read the content.
    """

    STREAM_CONTENT_NOT_LOGGED = '<File download contents unavailable for logging>'

    def __init__(self, logger, successful_response_format, error_response_format, **kwargs):
        """Extends baseclass method.

        :param logger:  The logger to use.
        :type logger:   :class:`Logger`
        :param successful_response_format:
            The logger %-style format string to use for logging ok responses.

            May use the following format placeholders:

                - %(method)s : The HTTP request method ('GET', 'POST', etc.).
                - %(url)s : The url of the request.
                - %(status_code)s : The HTTP status code of the response.
                - %(content_length)s : The Content-Length of the response body.
                - %(headers)s : The HTTP headers (as a pretty-printed dict).
                - %(content)s : The response body.

        :type successful_response_format:   `unicode`
        :param error_response_format:
            The logger %-style format string to use for logging ok responses.

            May use the same format placeholders as
            `successful_response_format`.
        :type error_response_format:  `unicode`
        """
        super(LoggingNetworkResponse, self).__init__(**kwargs)
        self._logger = logger
        self._successful_response_format = successful_response_format
        self._error_response_format = error_response_format
        self._did_log = False

    def log(self, can_safely_log_content=False):
        """Logs information about the Box API response.

        Will only execute once. Subsequent calls will be no-ops. This is
        partially because we only want to log responses once, and partially
        because this is necessary to prevent this method from infinite
        recursing with its use of the `content` property.

        :param can_safely_log_content:
            (optional) `True` if the caller is accessing the `content`
            property, `False` otherwise.

            As stated in the class docstring, it is unsafe for this logging
            method to access `content` unless the caller is also accessing it.

            Defaults to `False`.
        :type can_safely_log_content:   `bool`
        """
        if self._did_log:
            return
        self._did_log = True
        content_length = self.headers.get('Content-Length', None)
        content = self.STREAM_CONTENT_NOT_LOGGED
        if can_safely_log_content:
            if content_length is None:
                content_length = text_type(len(self.content))

            # If possible, get the content as a JSON `dict`, that way
            # `pformat(content)` will return pretty-printed JSON.
            try:
                content = self.json()
            except ValueError:
                content = self.content
            content = pformat(content)
        if content_length is None:
            content_length = '?'
        if self.ok:
            logger_method, response_format = self._logger.info, self._successful_response_format
        else:
            logger_method, response_format = self._logger.warning, self._error_response_format
        logger_method(
            response_format,
            {
                'method': self.request_response.request.method,
                'url': self.request_response.request.url,
                'status_code': self.status_code,
                'content_length': content_length,
                'headers': pformat(self.headers),
                'content': content,
            },
        )

    def json(self):
        """Extends baseclass method."""
        try:
            return super(LoggingNetworkResponse, self).json()
        finally:
            self.log(can_safely_log_content=True)

    @property
    def content(self):
        """Extends baseclass method."""
        content = super(LoggingNetworkResponse, self).content
        self.log(can_safely_log_content=True)
        return content

    @property
    def response_as_stream(self):
        """Extends baseclass method."""
        stream = super(LoggingNetworkResponse, self).response_as_stream
        self.log(can_safely_log_content=False)
        return stream

    @property
    def request_response(self):
        """Extends baseclass method."""
        response = super(LoggingNetworkResponse, self).request_response
        self.log(can_safely_log_content=False)
        return response
