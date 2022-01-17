# coding: utf-8

import random
import math

from functools import partial
from logging import getLogger
from numbers import Number
from typing import TYPE_CHECKING, Optional, Any, Type, Callable

from boxsdk.exception import BoxException
from .box_request import BoxRequest as _BoxRequest
from .box_response import BoxResponse as _BoxResponse
from ..config import API, Client, Proxy
from ..exception import BoxAPIException
from ..network.default_network import DefaultNetwork
from ..util.json import is_json_response
from ..util.multipart_stream import MultipartStream
from ..util.shared_link import get_shared_link_header
from ..util.translator import Translator

if TYPE_CHECKING:
    from boxsdk.network.network_interface import Network
    from boxsdk.object.user import User
    from boxsdk import NetworkResponse, OAuth2


class Session:

    _retry_randomization_factor = 0.5
    _retry_base_interval = 1
    _JWT_GRANT_TYPE = 'urn:ietf:params:oauth:grant-type:jwt-bearer'

    """
    Box API session. Provides automatic retry of failed requests.
    """
    def __init__(
            self,
            network_layer: 'Network' = None,
            default_headers: Optional['dict'] = None,
            translator: Translator = None,
            default_network_request_kwargs: Optional['dict'] = None,
            api_config: API = None,
            client_config: Client = None,
            proxy_config: Optional[Proxy] = None,
    ):
        """
        :param network_layer:
            Network implementation used by the session to make requests.
        :param default_headers:
            A dictionary containing default values to be used as headers when this session makes an API request.
        :param translator:
            (optional) The translator to use for translating Box API JSON
            responses into :class:`BaseAPIJSONObject` smart objects.
            Defaults to a new :class:`Translator` that inherits the
            registrations of the default translator.
        :param default_network_request_kwargs:
            A dictionary containing default values to be passed to the network layer
            when this session makes an API request.
        :param api_config:
            Object containing URLs for the Box API.
        :param client_config:
            Object containing client information, including user agent string.
        :param proxy_config:
            Object containing proxy information.
        """
        if translator is None:
            translator = Translator(extend_default_translator=True, new_child=True)
        self._api_config = api_config or API()
        self._client_config = client_config or Client()
        self._proxy_config = proxy_config or Proxy()
        super().__init__()
        self._network_layer = network_layer or DefaultNetwork()
        self._default_headers = {
            'User-Agent': self._client_config.USER_AGENT_STRING,
            'X-Box-UA': self._client_config.BOX_UA_STRING,
        }
        self._translator = translator
        self._default_network_request_kwargs = {}
        if default_headers:
            self._default_headers.update(default_headers)
        if default_network_request_kwargs:
            self._default_network_request_kwargs.update(default_network_request_kwargs)
        self._logger = getLogger(__name__)

    def get(self, url: str, **kwargs: Any) -> '_BoxResponse':
        """Make a GET request to the Box API.

        :param url:
            The URL for the request.
        """
        return self.request('GET', url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> '_BoxResponse':
        """Make a POST request to the Box API.

        :param url:
            The URL for the request.
        """
        return self.request('POST', url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> '_BoxResponse':
        """Make a PUT request to the Box API.

        :param url:
            The URL for the request.
        """
        return self.request('PUT', url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> '_BoxResponse':
        """Make a DELETE request to the Box API.

        :param url:
            The URL for the request.
        """
        if 'expect_json_response' not in kwargs:
            kwargs['expect_json_response'] = False
        return self.request('DELETE', url, **kwargs)

    def options(self, url: str, **kwargs: Any) -> '_BoxResponse':
        """Make an OPTIONS request to the Box API.

        :param url:
            The URL for the request.
        """
        return self.request('OPTIONS', url, **kwargs)

    def request(self, method: str, url: str, **kwargs: Any) -> '_BoxResponse':
        """Make a request to the Box API.

        :param method:
            The HTTP verb for the request.
        :param url:
            The URL for the request.
        """
        response = self._prepare_and_send_request(method, url, **kwargs)
        return self.box_response_constructor(response)

    @property
    def box_request_constructor(self) -> Type[_BoxRequest]:
        """Get the constructor for the container class representing an API request"""
        return _BoxRequest

    @property
    def box_response_constructor(self) -> Type[_BoxResponse]:
        """Get the constructor for the container class representing an API response"""
        return _BoxResponse

    @property
    def translator(self) -> Translator:
        """
        The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.
        """
        return self._translator

    @property
    def api_config(self) -> API:
        return self._api_config

    @property
    def client_config(self) -> Client:
        return self._client_config

    @property
    def proxy_config(self) -> Proxy:
        return self._proxy_config

    def get_url(self, endpoint: str, *args: Any) -> str:
        """
        Return the URL for the given Box API endpoint.

        :param endpoint:
            The name of the endpoint.
        :param args:
            Additional parts of the endpoint URL.
        """
        # pylint:disable=no-self-use
        url = [f'{self._api_config.BASE_API_URL}/{endpoint}']
        url.extend([f'/{x}' for x in args])
        return ''.join(url)

    def get_constructor_kwargs(self) -> dict:
        return dict(
            network_layer=self._network_layer,
            translator=self._translator,
            default_network_request_kwargs=self._default_network_request_kwargs.copy(),
            api_config=self._api_config,
            client_config=self._client_config,
            proxy_config=self._proxy_config,
            default_headers=self._default_headers.copy(),
        )

    def as_user(self, user: 'User') -> 'Session':
        """
        Returns a new session object with default headers set up to make requests as the specified user.

        :param user:
            The user to impersonate when making API requests.
        """
        kwargs = self.get_constructor_kwargs()
        kwargs['default_headers']['As-User'] = user.object_id
        return self.__class__(**kwargs)

    def with_shared_link(self, shared_link: str, shared_link_password: str = None) -> 'Session':
        """
        Returns a new session object with default headers set up to make requests using the shared link for auth.

        :param shared_link:
            The shared link.
        :param shared_link_password:
            The password for the shared link.
        """
        kwargs = self.get_constructor_kwargs()
        kwargs['default_headers'].update(get_shared_link_header(shared_link, shared_link_password))
        return self.__class__(**kwargs)

    def with_default_network_request_kwargs(self, extra_network_parameters: dict) -> 'Session':
        kwargs = self.get_constructor_kwargs()
        kwargs['default_network_request_kwargs'].update(extra_network_parameters)
        return self.__class__(**kwargs)

    # We updated our retry strategy to use exponential backoff instead of the header returned from the API response.
    # This is something we can remove in latter major bumps.
    # pylint: disable=unused-argument
    def get_retry_after_time(self, attempt_number: int, retry_after_header: Optional[str]) -> Number:
        """
        Get the amount of time to wait before retrying the API request, using the attempt number that failed to
        calculate the retry time for the next retry attempt.

        If the Retry-After header is supplied, use it; otherwise, use exponential backoff
        For 202 Accepted (thumbnail or file not ready) and 429 (too many requests), retry later, after a delay
        specified by the Retry-After header.
        For 5xx Server Error, retry later, after a delay; use exponential backoff to determine the delay.

        :param attempt_number:          How many attempts at this request have already been tried.
        :param retry_after_header:      Value of the 'Retry-After` response header.
        :return:                        Number of seconds to wait before retrying.
        """
        if retry_after_header is not None:
            try:
                return int(retry_after_header)
            except (ValueError, TypeError):
                pass
        min_randomization = 1 - self._retry_randomization_factor
        max_randomization = 1 + self._retry_randomization_factor
        randomization = (random.uniform(0, 1) * (max_randomization - min_randomization)) + min_randomization
        exponential = math.pow(2, attempt_number)
        return exponential * self._retry_base_interval * randomization

    @staticmethod
    def _raise_on_unsuccessful_request(network_response: 'NetworkResponse', request: '_BoxRequest') -> None:
        """
        Raise an exception if the request was unsuccessful.

        :param network_response:
            The network response which is being tested for success.
        :param request:
            The API request that could be unsuccessful.
        """
        if not network_response.ok:
            response_json = {}
            try:
                response_json = network_response.json()
            except ValueError:
                pass
            raise BoxAPIException(
                status=network_response.status_code,
                headers=network_response.headers,
                code=response_json.get('code', None) or response_json.get('error', None),
                message=response_json.get('message', None) or response_json.get('error_description', None),
                request_id=response_json.get('request_id', None),
                url=request.url,
                method=request.method,
                context_info=response_json.get('context_info', None),
                network_response=network_response
            )
        if request.expect_json_response and not is_json_response(network_response):
            raise BoxAPIException(
                status=network_response.status_code,
                headers=network_response.headers,
                message='Non-json response received, while expecting json response.',
                url=request.url,
                method=request.method,
                network_response=network_response,
            )

    def _prepare_and_send_request(
            self,
            method: str,
            url: str,
            headers: dict = None,
            auto_session_renewal: bool = True,
            expect_json_response: bool = True,
            **kwargs: Any
    ) -> 'NetworkResponse':
        """
        Prepare a request to be sent to the Box API.

        :param method:
            The HTTP verb to use to make the request.
        :param url:
            The request URL.
        :param headers:
            Headers to include with the request.
        :param auto_session_renewal:
            Whether or not to automatically renew the session if the request fails due to an expired access token.
        :param expect_json_response:
            Whether or not the response content should be json.
        """
        files = kwargs.get('files')
        kwargs['file_stream_positions'] = None
        if files:
            kwargs['file_stream_positions'] = dict((name, file_tuple[1].tell()) for name, file_tuple in files.items())
        attempt_number = 0
        request_headers = self._get_request_headers()
        request_headers.update(headers or {})

        request = self.box_request_constructor(
            url=url,
            method=method,
            headers=request_headers,
            auto_session_renewal=auto_session_renewal,
            expect_json_response=expect_json_response,
        )

        skip_retry_codes = kwargs.pop('skip_retry_codes', set())
        network_response = self._send_request(request, **kwargs)

        while True:
            retry = self._get_retry_request_callable(network_response, attempt_number, request, **kwargs)

            if retry is None or attempt_number >= API.MAX_RETRY_ATTEMPTS or network_response.status_code in skip_retry_codes:
                break

            attempt_number += 1
            self._logger.debug('Retrying request')
            network_response = retry(request, **kwargs)

        self._raise_on_unsuccessful_request(network_response, request)

        return network_response

    def _get_retry_request_callable(
            self,
            network_response: 'NetworkResponse',
            attempt_number: int,
            request: '_BoxRequest',
            **kwargs: Any
    ) -> Optional[Callable]:
        """
        Get a callable that retries a request for certain types of failure.

        For 202 Accepted (thumbnail or file not ready) and 429 (too many requests), retry later, after a delay
        specified by the Retry-After header.
        For 5xx Server Error, retry later, after a delay; use exponential backoff to determine the delay.

        Otherwise, return None.

        :param network_response:
            The response from the Box API.
        :param attempt_number:
            How many attempts at this request have already been tried. Used for exponential backoff calculations.
        :param request:
            The API request that could require retrying.
        :return:
            Callable that, when called, will retry the request. Takes the same parameters as :meth:`_send_request`.
        """
        # pylint:disable=unused-argument
        data = kwargs.get('data', {})
        grant_type = None
        try:
            if 'grant_type' in data:
                grant_type = data['grant_type']
        except TypeError:
            pass
        code = network_response.status_code
        if (code in (202, 429) or code >= 500) and grant_type != self._JWT_GRANT_TYPE:
            return partial(
                self._network_layer.retry_after,
                self.get_retry_after_time(attempt_number, network_response.headers.get('Retry-After', None)),
                self._send_request,
            )
        return None

    def _get_request_headers(self) -> dict:
        return self._default_headers.copy()

    def _prepare_proxy(self) -> Optional[dict]:
        """
        Prepares basic authenticated and unauthenticated proxies for requests.

        :return:
            A prepared proxy dict to send along with the request. None if incorrect parameters were passed.
        """
        proxy = {}
        if self._proxy_config.URL is None:
            return None
        if self._proxy_config.AUTH and {'user', 'password'} <= set(self._proxy_config.AUTH):
            host = self._proxy_config.URL
            address = host.split('//')[1]
            proxy_string = f'http://{self._proxy_config.AUTH.get("user", None)}:' \
                           f'{self._proxy_config.AUTH.get("password", None)}@{address}'
        elif self._proxy_config.AUTH is None:
            proxy_string = self._proxy_config.URL
        else:
            raise BoxException("The proxy auth dict you provided does not match pattern "
                               "{'user': 'example_user', 'password': 'example_password'}")
        proxy['http'] = proxy_string
        proxy['https'] = proxy['http']

        return proxy

    def _send_request(self, request: '_BoxRequest', **kwargs: Any) -> 'NetworkResponse':
        """
        Make a request to the Box API.

        :param request:
            The API request to send.
        """
        # Reset stream positions to what they were when the request was made so the same data is sent even if this
        # is a retried attempt.
        files, file_stream_positions = kwargs.get('files'), kwargs.pop('file_stream_positions')
        request_kwargs = self._default_network_request_kwargs.copy()
        request_kwargs.update(kwargs)
        proxy_dict = self._prepare_proxy()
        if proxy_dict is not None:
            request_kwargs.update({'proxies': proxy_dict})
        if files and file_stream_positions:
            for name, position in file_stream_positions.items():
                files[name][1].seek(position)
            data = request_kwargs.pop('data', {})
            multipart_stream = MultipartStream(data, files)
            request_kwargs['data'] = multipart_stream
            del request_kwargs['files']
            request.headers['Content-Type'] = multipart_stream.content_type

        # send the request
        network_response = self._network_layer.request(
            request.method,
            request.url,
            access_token=request_kwargs.pop('access_token', None),
            headers=request.headers,
            **request_kwargs
        )

        return network_response


class AuthorizedSession(Session):
    """
    Box API authorized session. Provides auth, automatic retry of failed requests, and session renewal.
    """

    def __init__(self, oauth: 'OAuth2', **kwargs: Any):
        """
        :param oauth:
            OAuth2 object used by the session to authorize requests.
        :param session:
            The Box API session to wrap for authorization.
        """
        super().__init__(**kwargs)
        self._oauth = oauth

    def get_constructor_kwargs(self) -> dict:
        kwargs = super().get_constructor_kwargs()
        kwargs['oauth'] = self._oauth
        return kwargs

    def _renew_session(self, access_token_used: Optional[str]) -> str:
        """
        Renews the session by refreshing the access token.

        :param access_token_used:
            The access token that's currently being used by the session, that needs to be refreshed.
        """
        new_access_token, _ = self._oauth.refresh(access_token_used)
        return new_access_token

    def _get_retry_request_callable(
            self,
            network_response: 'NetworkResponse',
            attempt_number: int,
            request: '_BoxRequest',
            **kwargs: Any
    ) -> Callable:
        """
        Get a callable that retries a request for certain types of failure.

        For 401 Unauthorized responses, renew the session by refreshing the access token; then retry.

        Otherwise, defer to baseclass implementation.

        :param network_response:
            The response from the Box API.
        :param attempt_number:
            How many attempts at this request have already been tried. Used for exponential backoff calculations.
        :param request:
            The API request that could require retrying.
        :return:
            Callable that, when called, will retry the request. Takes the same parameters as :meth:`_send_request`.
        """
        code = network_response.status_code
        if code == 401 and request.auto_session_renewal:
            self._renew_session(network_response.access_token_used)
            request.auto_session_renewal = False
            return self._send_request
        return super()._get_retry_request_callable(
            network_response,
            attempt_number,
            request,
            **kwargs
        )

    def _send_request(self, request: '_BoxRequest', **kwargs: Any) -> 'NetworkResponse':
        """
        Make a request to the Box API.

        :param request:
            The API request to send.
        """
        # Since there can be session renewal happening in the middle of preparing the request, it's important to be
        # consistent with the access_token being used in the request.
        access_token = self._oauth.access_token
        if request.auto_session_renewal and access_token is None:
            access_token = self._renew_session(None)
            request.auto_session_renewal = False
        authorization_header = {'Authorization': f'Bearer {access_token}'}
        request.headers.update(authorization_header)
        kwargs['access_token'] = access_token
        return super()._send_request(request, **kwargs)
