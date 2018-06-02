# coding: utf-8

from __future__ import unicode_literals, absolute_import

from functools import partial
from logging import getLogger

from .box_request import BoxRequest as _BoxRequest
from .box_response import BoxResponse as _BoxResponse
from ..config import API, Client
from ..exception import BoxAPIException
from ..util.multipart_stream import MultipartStream
from ..util.shared_link import get_shared_link_header
from ..util.translator import Translator


class BoxSession(object):
    """
    Box API session. Provides auth, automatic retry of failed requests, and session renewal.
    """

    def __init__(
            self,
            oauth,
            network_layer,
            default_headers=None,
            translator=None,
            default_network_request_kwargs=None,
            api_config=None,
            client_config=None,
    ):
        """
        :param oauth:
            OAuth2 object used by the session to authorize requests.
        :type oauth:
            :class:`OAuth2`
        :param network_layer:
            Network implementation used by the session to make requests.
        :type network_layer:
            :class:`Network`
        :param default_headers:
            A dictionary containing default values to be used as headers when this session makes an API request.
        :type default_headers:
            `dict` or None
        :param translator:
            (optional) The translator to use for translating Box API JSON
            responses into :class:`BaseAPIJSONObject` smart objects.
            Defaults to a new :class:`Translator` that inherits the
            registrations of the default translator.
        :type translator:   :class:`Translator`
        :param default_network_request_kwargs:
            A dictionary containing default values to be passed to the network layer
            when this session makes an API request.
        :type default_network_request_kwargs:
            `dict` or None
        :param api_config:
            Object containing URLs for the Box API.
        :type api_config:
            :class:`API`
        :param client_config:
            Object containing client information, including user agent string.
        :type client_config:
            :class:`Client`
        """
        if translator is None:
            translator = Translator(extend_default_translator=True, new_child=True)
        self._api_config = api_config or API()
        self._client_config = client_config or Client()
        super(BoxSession, self).__init__()
        self._oauth = oauth
        self._network_layer = network_layer
        self._default_headers = {'User-Agent': self._client_config.USER_AGENT_STRING}
        self._translator = translator
        self._default_network_request_kwargs = {}
        if default_headers:
            self._default_headers.update(default_headers)
        if default_network_request_kwargs:
            self._default_network_request_kwargs.update(default_network_request_kwargs)
        self._logger = getLogger(__name__)

    @property
    def box_request_constructor(self):
        """Get the constructor for the container class representing an API request"""
        return _BoxRequest

    @property
    def box_response_constructor(self):
        """Get the constructor for the container class representing an API response"""
        return _BoxResponse

    @property
    def translator(self):
        """The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.

        :rtype:   :class:`Translator`
        """
        return self._translator

    @property
    def api_config(self):
        """

        :rtype:     :class:`API`
        """
        return self._api_config

    @property
    def client_config(self):
        """

        :rtype:     :class:`Client`
        """
        return self._client_config

    def get_url(self, endpoint, *args):
        """
        Return the URL for the given Box API endpoint.

        :param endpoint:
            The name of the endpoint.
        :type endpoint:
            `url`
        :param args:
            Additional parts of the endpoint URL.
        :type args:
            `Iterable`
        :rtype:
            `unicode`
        """
        # pylint:disable=no-self-use
        url = ['{0}/{1}'.format(self._api_config.BASE_API_URL, endpoint)]
        url.extend(['/{0}'.format(x) for x in args])
        return ''.join(url)

    def as_user(self, user):
        """
        Returns a new session object with default headers set up to make requests as the specified user.

        :param user:
            The user to impersonate when making API requests.
        :type user:
            :class:`User`
        """
        headers = self._default_headers.copy()
        headers['As-User'] = user.object_id
        return self.__class__(
            self._oauth,
            self._network_layer,
            default_headers=headers,
            translator=self._translator,
            default_network_request_kwargs=self._default_network_request_kwargs.copy(),
            api_config=self._api_config,
            client_config=self._client_config,
        )

    def with_shared_link(self, shared_link, shared_link_password=None):
        """
        Returns a new session object with default headers set up to make requests using the shared link for auth.

        :param shared_link:
            The shared link.
        :type shared_link:
            `unicode`
        :param shared_link_password:
            The password for the shared link.
        :type shared_link_password:
            `unicode`
        """
        headers = self._default_headers.copy()
        headers.update(get_shared_link_header(shared_link, shared_link_password))
        return self.__class__(
            self._oauth,
            self._network_layer,
            default_headers=headers,
            translator=self._translator,
            default_network_request_kwargs=self._default_network_request_kwargs.copy(),
            api_config=self._api_config,
            client_config=self._client_config,
        )

    def with_default_network_request_kwargs(self, extra_network_parameters):
        return self.__class__(
            self._oauth,
            self._network_layer,
            default_headers=self._default_headers.copy(),
            translator=self._translator,
            default_network_request_kwargs=extra_network_parameters,
            api_config=self._api_config,
            client_config=self._client_config,
        )

    def _renew_session(self, access_token_used):
        """
        Renews the session by refreshing the access token.

        :param access_token_used:
            The access token that's currently being used by the session, that needs to be refreshed.
        :type access_token_used:
            `unicode` or None
        """
        new_access_token, _ = self._oauth.refresh(access_token_used)
        return new_access_token

    @staticmethod
    def _is_json_response(network_response):
        """Return whether or not the network response content is json.

        :param network_response:
            The response from the Box API.
        :type network_response:
            :class:`NetworkResponse`
        """
        try:
            network_response.json()
            return True
        except ValueError:
            return False

    def _get_retry_after_time(self, attempt_number, retry_after_header):
        """
        Get the amount of time to wait before retrying the API request.

        If the Retry-After header is supplied, use it; otherwise, use exponential backoff
        For 202 Accepted (thumbnail or file not ready) and 429 (too many requests), retry later, after a delay
        specified by the Retry-After header.
        For 5xx Server Error, retry later, after a delay; use exponential backoff to determine the delay.

        :param attempt_number:          How many attempts at this request have already been tried.
        :type attempt_number:           `int`
        :param retry_after_header:      Value of the 'Retry-After` response header.
        :type retry_after_header:       `unicode` or None
        :return:                        Number of seconds to wait before retrying.
        :rtype:                         `Number`
        """
        # pylint:disable=no-self-use
        if retry_after_header is not None:
            return float(retry_after_header)
        return 2 ** attempt_number

    def _get_retry_request_callable(self, network_response, attempt_number, request):
        """
        Get a callable that retries a request for certain types of failure.

        For 401 Unauthorized responses, renew the session by refreshing the access token; then retry.
        For 202 Accepted (thumbnail or file not ready) and 429 (too many requests), retry later, after a delay
        specified by the Retry-After header.
        For 5xx Server Error, retry later, after a delay; use exponential backoff to determine the delay.

        Otherwise, return None.

        :param network_response:
            The response from the Box API.
        :type network_response:
            :class:`NetworkResponse`
        :param attempt_number:
            How many attempts at this request have already been tried. Used for exponential backoff calculations.
        :type attempt_number:
            `int`
        :param request:
            The API request that could require retrying.
        :type request:
            :class:`BoxRequest`
        :return:
            Callable that, when called, will retry the request. Takes the same parameters as :meth:`_send_request`.
        :rtype:
            `callable`
        """
        code = network_response.status_code
        if code == 401 and request.auto_session_renewal:
            self._renew_session(network_response.access_token_used)
            request.auto_session_renewal = False
            return self._send_request
        elif code in (202, 429) or code >= 500:
            return partial(
                self._network_layer.retry_after,
                self._get_retry_after_time(attempt_number, network_response.headers.get('Retry-After', None)),
                self._send_request,
            )
        return None

    def _raise_on_unsuccessful_request(self, network_response, request):
        """
        Raise an exception if the request was unsuccessful.

        :param network_response:
            The network response which is being tested for success.
        :type network_response:
            :class:`NetworkResponse`
        :param request:
            The API request that could be unsuccessful.
        :type request:
            :class:`BoxRequest`
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
                code=response_json.get('code', None),
                message=response_json.get('message', None),
                request_id=response_json.get('request_id', None),
                url=request.url,
                method=request.method,
                context_info=response_json.get('context_info', None),
                network_response=network_response
            )
        if request.expect_json_response and not self._is_json_response(network_response):
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
            method,
            url,
            headers=None,
            auto_session_renewal=True,
            expect_json_response=True,
            **kwargs
    ):
        """
        Prepare a request to be sent to the Box API.

        :param method:
            The HTTP verb to use to make the request.
        :type method:
            `unicode`
        :param url:
            The request URL.
        :type url:
            `unicode`
        :param headers:
            Headers to include with the request.
        :type headers:
            `dict`
        :param auto_session_renewal:
            Whether or not to automatically renew the session if the request fails due to an expired access token.
        :type auto_session_renewal:
            `bool`
        :param expect_json_response:
            Whether or not the response content should be json.
        :type expect_json_response:
            `bool`
        :param attempt_number:
            How many attempts at this request have already been tried. Used for exponential backoff calculations.
        :type attempt_number:
            `int`
        """
        files = kwargs.get('files')
        kwargs['file_stream_positions'] = None
        if files:
            kwargs['file_stream_positions'] = dict((name, file_tuple[1].tell()) for name, file_tuple in files.items())
        attempt_number = 0

        request = self.box_request_constructor(
            url=url,
            method=method,
            headers=headers,
            auto_session_renewal=auto_session_renewal,
            expect_json_response=expect_json_response,
        )

        network_response = self._send_request(request, **kwargs)

        while True:
            retry = self._get_retry_request_callable(network_response, attempt_number, request)

            if retry is None or attempt_number >= 10:
                break

            attempt_number += 1
            network_response.log(can_safely_log_content=True)
            self._logger.debug('Retrying request')
            network_response = retry(request, **kwargs)

        self._raise_on_unsuccessful_request(network_response, request)

        return network_response

    def _send_request(self, request, **kwargs):
        """
        Make a request to the Box API.

        :param request:
            The API request to send.
        :type request:
            :class:`BoxRequest`
        :param expect_json_response:
            Whether or not the response content should be json.
        :type expect_json_response:
            `bool`
        """
        # Since there can be session renewal happening in the middle of preparing the request, it's important to be
        # consistent with the access_token being used in the request.
        access_token = self._oauth.access_token
        if request.auto_session_renewal and access_token is None:
            access_token = self._renew_session(None)
            request.auto_session_renewal = False
        authorization_header = {'Authorization': 'Bearer {0}'.format(access_token)}
        if request.headers is None:
            request.headers = self._default_headers.copy()
        request.headers.update(authorization_header)

        # Reset stream positions to what they were when the request was made so the same data is sent even if this
        # is a retried attempt.
        files, file_stream_positions = kwargs.get('files'), kwargs.pop('file_stream_positions')
        request_kwargs = self._default_network_request_kwargs.copy()
        request_kwargs.update(kwargs)
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
            access_token=access_token,
            headers=request.headers,
            **request_kwargs
        )

        return network_response

    def get(self, url, **kwargs):
        """Make a GET request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        """Make a POST request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        """Make a PUT request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        """Make a DELETE request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        if 'expect_json_response' not in kwargs:
            kwargs['expect_json_response'] = False
        return self.request('DELETE', url, **kwargs)

    def options(self, url, **kwargs):
        """Make an OPTIONS request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        return self.request('OPTIONS', url, **kwargs)

    def request(self, method, url, **kwargs):
        """Make a request to the Box API.

        :param method:
            The HTTP verb for the request.
        :type method:
            `unicode`
        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        response = self._prepare_and_send_request(method, url, **kwargs)
        return self.box_response_constructor(response)
