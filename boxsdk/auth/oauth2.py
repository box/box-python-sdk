# coding: utf-8

from contextlib import contextmanager
from logging import getLogger
import random
import string  # pylint:disable=deprecated-module
from threading import Lock
from typing import Optional, Callable, ContextManager, Tuple, TYPE_CHECKING, Any, Union
from urllib.parse import urlunsplit, urlencode

from ..config import API
from ..exception import BoxOAuthException, BoxAPIException
from ..object.base_api_json_object import BaseAPIJSONObject
from ..session.session import Session
from ..util.json import is_json_response
from ..util.text_enum import TextEnum

if TYPE_CHECKING:
    from boxsdk.session.box_response import BoxResponse
    from boxsdk import NetworkResponse


class TokenScope(TextEnum):
    """ Scopes used for a downscope token request.

    See https://developer.box.com/en/guides/authentication/access-tokens/downscope/.
    """
    ITEM_READ = 'item_read'
    ITEM_READWRITE = 'item_readwrite'
    ITEM_PREVIEW = 'item_preview'
    ITEM_UPLOAD = 'item_upload'
    ITEM_SHARE = 'item_share'
    ITEM_DELETE = 'item_delete'
    ITEM_DOWNLOAD = 'item_download'


class TokenResponse(BaseAPIJSONObject):
    """ Represents the response for a token request. """


class OAuth2:
    """
    Responsible for handling OAuth2 for the Box API. Can authenticate and refresh tokens.

    Can be used as a closeable resource, similar to a file. When `close()` is
    called, the current tokens are revoked, and the object is put into a state
    where it can no longer request new tokens. This action can also be managed
    with the `closing()` context manager method.
    """

    def __init__(
            self,
            client_id: Optional[str],
            client_secret: Optional[str],
            store_tokens: Optional[Callable] = None,
            box_device_id: str = '0',
            box_device_name: str = '',
            access_token: str = None,
            refresh_token: Optional[str] = None,
            session: Optional[Session] = None,
            refresh_lock: Optional[ContextManager] = None,
    ):
        """
        :param client_id:
            Box API key used for identifying the application the user is authenticating with.
        :param client_secret:
            Box API secret used for making OAuth2 requests.
        :param store_tokens:
            Optional callback for getting access to tokens for storing them.
        :param box_device_id:
            Optional unique ID of this device. Used for applications that want to support device-pinning.
        :param box_device_name:
            Optional human readable name for this device.
        :param access_token:
            Access token to use for auth until it expires.
        :param refresh_token:
            Refresh token to use for auth until it expires or is used.
        :param session:
            If specified, use it to make network requests. If not, the default session will be used.
        :param refresh_lock:
            Lock used to synchronize token refresh. If not specified, then a :class:`threading.Lock` will be used.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._store_tokens_callback = store_tokens
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._session = session or Session()
        self._refresh_lock = refresh_lock or Lock()
        self._box_device_id = box_device_id
        self._box_device_name = box_device_name
        self._closed = False
        self._api_config = API()
        self._logger = getLogger(__name__)

    @property
    def access_token(self) -> str:
        """
        Get the current access token.

        :return:
            current access token
        """
        return self._access_token

    @property
    def closed(self) -> bool:
        """True iff the auth object has been closed.

        When in the closed state, it can no longer request new tokens.
        """
        return self._closed

    @property
    def api_config(self) -> API:
        return self._api_config

    def get_authorization_url(self, redirect_url: Optional[str]) -> Tuple[str, str]:
        """
        Get the authorization url based on the client id and the redirect url passed in

        :param redirect_url:
            An HTTPS URI or custom URL scheme where the response will be redirected. Optional if the redirect URI is
            registered with Box already.
        :return:
            A tuple of the URL of Box's authorization page and the CSRF token.
            This is the URL that your application should forward the user to in first leg of OAuth 2.
        """
        csrf_token = self._get_state_csrf_token()
        # For the query string parameters, use a sequence of two-element
        # tuples, rather than a dictionary, in order to get a consistent and
        # predictable order of parameters in the output of `urlencode()`.
        params = [
            ('state', csrf_token),
            ('response_type', 'code'),
            ('client_id', self._client_id),
        ]
        if redirect_url:
            params.append(('redirect_uri', redirect_url))
        # `urlencode()` doesn't work with non-ASCII unicode characters, so
        # encode the parameters as ASCII bytes.
        params = [(key.encode('utf-8'), value.encode('utf-8')) for (key, value) in params]
        query_string = urlencode(params)
        return urlunsplit(('', '', self._api_config.OAUTH2_AUTHORIZE_URL, query_string, '')), csrf_token

    def authenticate(self, auth_code: Optional[str]) -> Tuple[str, str]:
        """
        Send token request and return the access_token, refresh_token tuple. The access token and refresh token will be
        stored by calling the `store_tokens` callback if provided in __init__.

        :param auth_code:
            An authorization code you retrieved in the first leg of OAuth 2.
        :return:
            (access_token, refresh_token)
        """
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        }
        if self._box_device_id:
            data['box_device_id'] = self._box_device_id
        if self._box_device_name:
            data['box_device_name'] = self._box_device_name
        return self.send_token_request(data, access_token=None)

    def _refresh(self, access_token: str) -> Tuple[str, str]:
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        }
        if self._box_device_id:
            data['box_device_id'] = self._box_device_id
        if self._box_device_name:
            data['box_device_name'] = self._box_device_name

        return self.send_token_request(data, access_token)

    def _get_tokens(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get the current access and refresh tokens.

        This is a protected method that can be overridden to look up tokens
        from an external source (the inverse of the `store_tokens` callback).

        This method does not need to update this object's private token
        attributes. Its caller in :class:`OAuth2` is responsible for that.

        :return:
            Tuple containing the current access token and refresh token.
            One or both of them may be `None`, if they aren't set.
        """
        return self._access_token, self._refresh_token

    def refresh(self, access_token_to_refresh: Optional[str]) -> Tuple[str, Optional[str]]:
        """
        Refresh the access token and the refresh token and return the access_token, refresh_token tuple. The access
        token and refresh token will be stored by calling the `store_tokens` callback if provided in __init__.

        :param access_token_to_refresh:
            The expired access token, which needs to be refreshed.
            Pass `None` if you don't have the access token.
        :return:
            Tuple containing the new access token and refresh token.
            The refresh token may be `None`, if the authentication scheme
            doesn't use one, or keeps it hidden from this client.
        """
        self._check_closed()
        with self._refresh_lock:
            self._check_closed()
            self._logger.debug('Refreshing tokens.')
            access_token, refresh_token = self._get_and_update_current_tokens()
            # The lock here is for handling that case that multiple requests fail, due to access token expired, at the
            # same time to avoid multiple session renewals.
            if (access_token is None) or (access_token_to_refresh == access_token):
                # If the active access token is the same as the token that needs to
                # be refreshed, or if we don't currently have any active access
                # token, we make the request to refresh the token.
                access_token, refresh_token = self._refresh(access_token_to_refresh)
            # Else, if the active access token (self._access_token) is not the same as the token needs to be refreshed,
            # it means the expired token has already been refreshed. Simply return the current active tokens.
            return access_token, refresh_token

    @staticmethod
    def _get_state_csrf_token() -> str:
        """ Generate a random state CSRF token to be used in the authorization url.
        Example: box_csrf_token_Iijw9aU31sNdgiQu

        :return:
            The security token
        """
        system_random = random.SystemRandom()
        ascii_alphabet = string.ascii_letters + string.digits
        ascii_len = len(ascii_alphabet)
        return 'box_csrf_token_' + ''.join(ascii_alphabet[int(system_random.random() * ascii_len)] for _ in range(16))

    def _store_tokens(self, access_token: Optional[str], refresh_token: Optional[str]) -> None:
        self._update_current_tokens(access_token, refresh_token)
        if self._store_tokens_callback is not None:
            self._store_tokens_callback(access_token, refresh_token)

    def _get_and_update_current_tokens(self) -> Tuple[Optional[str], Optional[str]]:
        """Get the current access and refresh tokens, while also storing them in this object's private attributes.

        :return:
            Same as for :meth:`_get_tokens()`.
        """
        tokens = self._get_tokens()
        self._update_current_tokens(*tokens)
        return tokens

    def _update_current_tokens(self, access_token: Optional[str], refresh_token: Optional[str]) -> None:
        """Store the latest tokens in this object's private attributes.

        :param access_token:
            The latest access token.
            May be `None`, if it hasn't been provided.
        :param refresh_token:
            The latest refresh token.
            May be `None`, if the authentication scheme doesn't use one, or if
            it hasn't been provided.
        """
        self._access_token, self._refresh_token = access_token, refresh_token

    def _execute_token_request(
            self,
            data: dict,
            access_token: Optional[str],
            expect_refresh_token: bool = True
    ) -> TokenResponse:
        """
        Send the request to acquire or refresh an access token.

        :param data:
            Dictionary containing the request parameters as specified by the Box API.
        :param access_token:
            The current access token.
        :return:
            The response for the token request.
        """
        self._check_closed()
        url = f'{self._api_config.OAUTH2_API_URL}/token'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        try:
            network_response = self._session.request(
                'POST',
                url,
                data=data,
                headers=headers,
                access_token=access_token,
            )
        except BoxAPIException as box_api_exception:
            raise self._oauth_exception(box_api_exception.network_response, url) from box_api_exception

        if not network_response.ok:
            raise self._oauth_exception(network_response, url)
        try:
            token_response = TokenResponse(network_response.json())
        except ValueError as value_exception:
            raise self._oauth_exception(network_response, url) from value_exception

        if ('access_token' not in token_response) or (expect_refresh_token and 'refresh_token' not in token_response):
            raise self._oauth_exception(network_response, url)

        return token_response

    @staticmethod
    def _oauth_exception(network_response: Union['NetworkResponse', 'BoxResponse'], url: str) -> BoxOAuthException:
        """
        Create a BoxOAuthException instance to raise. If the error response is JSON, parse it and include the
        code and message in the exception.
        """
        exception_kwargs = dict(
            status=network_response.status_code,
            url=url,
            method='POST',
            network_response=network_response,
        )
        if is_json_response(network_response):
            json_response = network_response.json()
            exception_kwargs.update(dict(
                code=json_response.get('code') or json_response.get('error'),
                message=json_response.get('message') or json_response.get('error_description'),
            ))
        else:
            exception_kwargs['message'] = network_response.content
        return BoxOAuthException(**exception_kwargs)

    def send_token_request(
            self,
            data: dict,
            access_token: Optional[str],
            expect_refresh_token: bool = True
    ) -> Tuple[str, str]:
        """
        Send the request to acquire or refresh an access token, and store the tokens.

        :param data:
            Dictionary containing the request parameters as specified by the Box API.
        :param access_token:
            The current access token.
        :param expect_refresh_token:
            Information if shoul we expect refresh token
        :return:
            The access token and refresh token.
        """
        token_response = self._execute_token_request(data, access_token, expect_refresh_token)
        # pylint:disable=no-member
        refresh_token = token_response.refresh_token if 'refresh_token' in token_response else None
        self._store_tokens(token_response.access_token, refresh_token)
        return self._access_token, self._refresh_token

    def revoke(self) -> None:
        """
        Revoke the authorization for the current access/refresh token pair.
        """
        with self._refresh_lock:
            access_token, refresh_token = self._get_and_update_current_tokens()
            token_to_revoke = access_token or refresh_token
            if token_to_revoke is None:
                return
            url = f'{self._api_config.OAUTH2_API_URL}/revoke'
            try:
                network_response = self._session.request(
                    'POST',
                    url,
                    data={
                        'client_id': self._client_id,
                        'client_secret': self._client_secret,
                        'token': token_to_revoke,
                    },
                    access_token=access_token,
                )
            except BoxAPIException as box_api_exception:
                raise self._oauth_exception(box_api_exception.network_response, url) from box_api_exception

            if not network_response.ok:
                raise BoxOAuthException(
                    network_response.status_code,
                    network_response.content,
                    url,
                    'POST',
                    network_response,
                )
            self._store_tokens(None, None)

    def close(self, revoke: bool = True) -> None:
        """Close the auth object.

        After this action is performed, the auth object can no longer request
        new tokens.

        This method may be called even if the auth object is already closed.

        :param revoke:
            (optional) Whether the current tokens should be revoked, via `revoke()`.
            Defaults to `True` as a security precaution, so that the tokens aren't usable
            by any adversaries after you are done with them.
            Note that the revoke isn't guaranteed to succeed (the network connection might
            fail, or the API call might respond with a non-200 HTTP response), so this
            isn't a fool-proof security mechanism.
            If the revoke fails, an exception is raised.
            The auth object is still considered to be closed, even if the revoke fails.
        """
        self._closed = True
        if revoke:
            self.revoke()

    @contextmanager
    def closing(self, **close_kwargs: Any) -> None:
        """Context manager to close the auth object on exit.

        The behavior is somewhat similar to `contextlib.closing(self)`, but has
        some differences.

        The context manager cannot be entered if the auth object is closed.

        If a non-`Exception` (e.g. `KeyboardInterrupt`) is caught from the
        block, this context manager prioritizes re-raising the exception as
        fast as possible, without blocking. Thus, in this case, the tokens will
        not be revoked, even if `revoke=True` was passed to this method.

        If exceptions are raised both from the block and from `close()`, the
        exception from the block will be reraised, and the exception from
        `close()` will be swallowed. The assumption is that the exception from
        the block is more relevant to the client, especially since the revoke
        can fail if the network is unavailable.

        :param close_kwargs:  Keyword arguments to pass to `close()`.
        """
        self._check_closed()
        exc_infos = []

        # pylint:disable=broad-except
        try:
            yield self
        except Exception as exception:
            exc_infos.append(exception)
        except BaseException as base_exception:
            exc_infos.append(base_exception)
            close_kwargs['revoke'] = False

        try:
            self.close(**close_kwargs)
        except Exception as exception:
            exc_infos.append(exception)

        if exc_infos:
            raise exc_infos[0]

    def _check_closed(self) -> None:
        if self.closed:
            raise ValueError("operation on a closed auth object")
