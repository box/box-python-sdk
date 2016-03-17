# coding: utf-8

from __future__ import unicode_literals

from boxsdk.config import API, Client
from boxsdk.exception import BoxAPIException
from boxsdk.util.multipart_stream import MultipartStream
from boxsdk.util.shared_link import get_shared_link_header


class BoxResponse(object):
    """Represents a response to a Box API request."""

    def __init__(self, network_response):
        self._network_response = network_response

    def json(self):
        """Return the parsed JSON response.

        :rtype:
            `dict` or `list` or `str` or `int` or `float`
        """
        return self._network_response.json()

    @property
    def content(self):
        """Return the content of the response body.

        :rtype:
            varies
        """
        return self._network_response.content

    @property
    def ok(self):
        """Return whether or not the request was successful.

        :rtype:
            `bool`
        """
        # pylint:disable=invalid-name
        return self._network_response.ok

    @property
    def status_code(self):
        """Return the HTTP status code of the response.

        :rtype:
            `int`
        """
        return self._network_response.status_code

    @property
    def network_response(self):
        """Return the underlying network response.

        :rtype:
            :class:`NetworkResponse`
        """
        return self._network_response


class BoxSession(object):
    """
    Box API session. Provides auth, automatic retry of failed requests, and session renewal.
    """

    def __init__(self, oauth, network_layer, default_headers=None):
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
        """
        self._oauth = oauth
        self._network_layer = network_layer
        self._default_headers = {'User-Agent': Client.USER_AGENT_STRING}
        if default_headers:
            self._default_headers.update(default_headers)

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
        url = ['{0}/{1}'.format(API.BASE_API_URL, endpoint)]
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
        return self.__class__(self._oauth, self._network_layer, headers)

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
        return self.__class__(self._oauth, self._network_layer, headers)

    def _renew_session(self, access_token_used):
        """
        Renews the session by refreshing the access token.

        :param access_token_used:
            The access token that's currently being used by the session, that needs to be refreshed.
        :type access_token_used:
            `unicode`
        """
        self._oauth.refresh(access_token_used)

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

    def _retry_request_if_necessary(self, network_response, attempt_number, *args, **kwargs):
        """
        Retry a request for certain types of failure.
        For 401 Unauthorized responses, renew the session by refreshing the access token; then retry.
        For 202 Accepted (thumbnail or file not ready) and 429 (too many requests), retry later, after a delay
        specified by the Retry-After header.
        For 5xx Server Error, retry later, after a delay; use exponential backoff to determine the delay.

        :param network_response:
            The response from the Box API.
        :type network_response:
            :class:`NetworkResponse`
        :param attempt_number:
            How many attempts at this request have already been tried. Used for exponential backoff calculations.
        :type attempt_number:
            `int`
        """
        if network_response.status_code == 401 and kwargs['auto_session_renewal']:
            self._renew_session(network_response.access_token_used)
            kwargs['auto_session_renewal'] = False
            return self._make_request(*args, **kwargs)
        elif network_response.status_code == 202 or network_response.status_code == 429:
            return self._network_layer.retry_after(
                float(network_response.headers['Retry-After']),
                self._make_request,
                *args,
                **kwargs
            )
        elif network_response.status_code >= 500 and attempt_number < 10:
            return self._network_layer.retry_after(
                2 ** attempt_number,
                self._make_request,
                *args,
                attempt_number=attempt_number + 1,
                **kwargs
            )
        return network_response

    def _raise_on_unsuccessful_request(self, network_response, expect_json_response, method, url):
        """
        Raise an exception if the request was unsuccessful.

        :param network_response:
            The network response which is being tested for success.
        :type network_response:
            :class:`NetworkResponse`
        :param expect_json_response:
            Whether or not the response content should be json.
        :type expect_json_response:
            `bool`
        :param method:
            The HTTP verb used to make the request.
        :type method:
            `unicode`
        :param url:
            The request URL.
        :type url:
            `unicode`
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
                url=url,
                method=method,
                context_info=response_json.get('context_info', None),
            )
        if expect_json_response and not self._is_json_response(network_response):
            raise BoxAPIException(
                status=network_response.status_code,
                headers=network_response.headers,
                message='Non-json response received, while expecting json response.',
                url=url,
                method=method,
            )

    def _prepare_and_send_request(
            self,
            method,
            url,
            headers=None,
            auto_session_renewal=True,
            expect_json_response=True,
            attempt_number=0,
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
        file_stream_positions = None
        if files:
            file_stream_positions = dict((name, file_tuple[1].tell()) for name, file_tuple in files.items())
        return self._make_request(
            method,
            url,
            headers,
            auto_session_renewal,
            expect_json_response,
            attempt_number,
            file_stream_positions=file_stream_positions,
            **kwargs
        )

    def _make_request(
            self,
            method,
            url,
            headers=None,
            auto_session_renewal=True,
            expect_json_response=True,
            attempt_number=0,
            **kwargs
    ):
        """
        Make a request to the Box API.

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
        # Since there can be session renewal happening in the middle of preparing the request, it's important to be
        # consistent with the access_token being used in the request.
        access_token_will_be_used = self._oauth.access_token
        authorization_header = {'Authorization': 'Bearer {0}'.format(access_token_will_be_used)}
        if headers is None:
            headers = self._default_headers.copy()
        headers.update(authorization_header)

        # Reset stream positions to what they were when the request was made so the same data is sent even if this
        # is a retried attempt.
        request_kwargs = kwargs
        files, file_stream_positions = kwargs.get('files'), kwargs.pop('file_stream_positions')
        if files and file_stream_positions:
            request_kwargs = kwargs.copy()
            for name, position in file_stream_positions.items():
                files[name][1].seek(position)
            data = request_kwargs.pop('data', {})
            multipart_stream = MultipartStream(data, files)
            request_kwargs['data'] = multipart_stream
            del request_kwargs['files']
            headers['Content-Type'] = multipart_stream.content_type

        # send the request
        network_response = self._network_layer.request(
            method,
            url,
            access_token=access_token_will_be_used,
            headers=headers,
            **request_kwargs
        )

        network_response = self._retry_request_if_necessary(
            network_response,
            attempt_number,
            method,
            url,
            headers=headers,
            auto_session_renewal=auto_session_renewal,
            expect_json_response=expect_json_response,
            file_stream_positions=file_stream_positions,
            **kwargs
        )

        self._raise_on_unsuccessful_request(network_response, expect_json_response, method, url)

        return network_response

    def get(self, url, **kwargs):
        """Make a GET request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        response = self._prepare_and_send_request('GET', url, **kwargs)
        return BoxResponse(response)

    def post(self, url, **kwargs):
        """Make a POST request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        response = self._prepare_and_send_request('POST', url, **kwargs)
        return BoxResponse(response)

    def put(self, url, **kwargs):
        """Make a PUT request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        response = self._prepare_and_send_request('PUT', url, **kwargs)
        return BoxResponse(response)

    def delete(self, url, **kwargs):
        """Make a DELETE request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        if 'expect_json_response' not in kwargs:
            kwargs['expect_json_response'] = False
        response = self._prepare_and_send_request('DELETE', url, **kwargs)
        return BoxResponse(response)

    def options(self, url, **kwargs):
        """Make an OPTIONS request to the Box API.

        :param url:
            The URL for the request.
        :type url:
            `unicode`
        """
        response = self._prepare_and_send_request('OPTIONS', url, **kwargs)
        return BoxResponse(response)

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
        return BoxResponse(response)
