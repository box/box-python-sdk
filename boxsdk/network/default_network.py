import logging
from logging import getLogger
from pprint import pformat
import sys
import time
from typing import Any, Callable, Type, Optional

import requests
from requests import Response
from requests.structures import CaseInsensitiveDict
from urllib3 import HTTPResponse

from .network_interface import Network, NetworkResponse
from ..util.log import sanitize_dictionary


class DefaultNetwork(Network):
    """Implements the network interface using the requests library."""

    LOGGER_NAME = 'boxsdk.network'
    REQUEST_FORMAT = '\x1b[36m%(method)s %(url)s %(request_kwargs)s\x1b[0m'
    EXCEPTION_FORMAT = '\x1b[31mRequest "%(method)s %(url)s" failed with %(exc_type_name)s exception: %(exc_value)r\x1b[0m'

    def __init__(self):
        super().__init__()
        self._session = requests.Session()
        self._logger = getLogger(__name__)

    def request(self, method: str, url: str, access_token: str, **kwargs: Any) -> NetworkResponse:
        """Base class override.

        Make a network request using a requests.Session. Logs information about an API request and response.

        Also logs exceptions before re-raising them.

        The logging of the response is deferred to :class:`DefaultNetworkResponse`.
        See that class's docstring for more info.
        """
        log_response_content = kwargs.pop('log_response_content', True)
        self._log_request(method, url, **kwargs)
        # pylint:disable=abstract-class-instantiated
        try:
            return self.network_response_constructor(
                request_response=self._session.request(method, url, **kwargs),
                access_token_used=access_token,
                log_response_content=log_response_content
            )
        except Exception:
            self._log_exception(method, url, sys.exc_info())
            raise

    def retry_after(self, delay: float, request_method: Callable, *args: Any, **kwargs: Any) -> Any:
        """Base class override.
        Retry after sleeping for delay seconds.
        """
        time.sleep(delay)
        return request_method(*args, **kwargs)

    @property
    def network_response_constructor(self) -> Type['DefaultNetworkResponse']:
        """Baseclass override.

        A callable that accepts `request_response` and `access_token_used`
        keyword arguments for the :class:`DefaultNetworkResponse` constructor,
        and returns an instance of :class:`DefaultNetworkResponse`.
        """
        return DefaultNetworkResponse

    def _log_request(self, method: str, url: str, **kwargs: Any) -> None:
        """
        Logs information about the Box API request.

        :param method:
            The HTTP verb that should be used to make the request.
        :param url:
            The URL for the request.
        """
        if self._logger.isEnabledFor(logging.INFO):
            self._logger.info(
                self.REQUEST_FORMAT,
                {'method': method, 'url': url, 'request_kwargs': pformat(sanitize_dictionary(kwargs))},
            )

    def _log_exception(self, method: str, url: str, exc_info: Any) -> None:
        """Log information at WARNING level about the exception that was raised when trying to make the request.

        :param method:  The HTTP verb that was used to make the request.
        :param url:   The URL for the request.
        :param exc_info:  The exception info returned from `sys.exc_info()`.
        """
        if self._logger.isEnabledFor(logging.WARNING):
            exc_type, exc_value, _ = exc_info
            self._logger.warning(
                self.EXCEPTION_FORMAT,
                {'method': method, 'url': url, 'exc_type_name': exc_type.__name__, 'exc_value': exc_value},
            )


class DefaultNetworkResponse(NetworkResponse):
    """Implementation of the network interface using the requests library.

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
    :class:`DefaultNetwork` to also access it. But if the caller uses any of
    the streaming mechanisms, then it is not safe for :class:`DefaultNetwork`
    to ever read any of the content.

    The SDK logs only the response content of type JSON. Non-JSON responses, e.g.
    the content of the downloaded file should not be logged by the SDK at any time.
    In that case the response will be logged with a placeholder for the actual content.

    :param: `log_response_content` specifies wheather the response content should be logged or not.
    Its value is determined by `BoxRequest.expect_json_response` field, which is set to False,
    only if explicitly specified inside SDK method, e.g. self._session.get(url, expect_json_response=False).
    So the contenet of the response will be read by the logger only when the call inside an SDK method
    expects a JSON response. In this case we can be sure that the SDK method will read the content
    of the response using non-streaming mechanism and accessing content of the response by logger
    with `response.json()` or 'response.content` is safe.
    """

    _COMMON_RESPONSE_FORMAT = '"%(method)s %(url)s" %(status_code)s %(content_length)s\n%(headers)s\n%(content)s\n'
    SUCCESSFUL_RESPONSE_FORMAT = f'\x1b[32m{_COMMON_RESPONSE_FORMAT}\x1b[0m'
    ERROR_RESPONSE_FORMAT = f'\x1b[31m{_COMMON_RESPONSE_FORMAT}\x1b[0m'
    CONTENT_NOT_LOGGED = '<No content or content unavailable for logging>'

    def __init__(self, request_response: 'Response', access_token_used: str, log_response_content: bool = True):
        self._logger = getLogger(__name__)
        self._request_response = request_response
        self._access_token_used = access_token_used
        self._did_log = False
        self._json = None
        self.log(can_safely_log_content=log_response_content)

    def json(self) -> dict:
        """Base class override."""
        if self._json is None:
            self._json = self._request_response.json()
        return self._json

    @property
    def content(self) -> Optional[bytes]:
        """Base class override."""
        return self._request_response.content

    @property
    def status_code(self) -> int:
        """Base class override."""
        return self._request_response.status_code

    @property
    def ok(self) -> bool:
        """Base class override."""
        # pylint:disable=invalid-name
        return self._request_response.ok

    @property
    def headers(self) -> CaseInsensitiveDict:
        """Base class override."""
        return self._request_response.headers

    @property
    def response_as_stream(self) -> HTTPResponse:
        """Base class override."""
        return self._request_response.raw

    @property
    def access_token_used(self) -> str:
        """Base class override."""
        return self._access_token_used

    @property
    def request_response(self) -> Response:
        """
        The response returned from the Requests library.
        """
        return self._request_response

    def log(self, can_safely_log_content: bool = False) -> None:
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
        """
        if self._did_log:
            return
        self._did_log = True

        if self.ok:
            logger_method, logger_level, response_format = self._logger.info, logging.INFO, self.SUCCESSFUL_RESPONSE_FORMAT
        else:
            logger_method, logger_level, response_format = self._logger.warning, logging.WARNING, self.ERROR_RESPONSE_FORMAT

        if not self._logger.isEnabledFor(logger_level):
            return

        content_length = self.headers.get('Content-Length', None)
        content = self.CONTENT_NOT_LOGGED
        if can_safely_log_content:
            if content_length is None:
                content_length = str(len(self.content))

            # If possible, get the content as a JSON `dict`, that way
            # `pformat(content)` will return pretty-printed JSON.
            try:
                content = self.json()
            except ValueError:
                content = self.content
            content = pformat(sanitize_dictionary(content))
        if content_length is None:
            content_length = '?'
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

    def __repr__(self) -> str:
        return f'<Box Network Response ({self._request_response.request.method} {self._request_response.request.url} ' \
               f'{self.status_code})>'
