# coding: utf-8

from __future__ import unicode_literals

from threading import Lock
import random
import string  # pylint:disable=deprecated-module

from six.moves.urllib.parse import urlencode, urlunsplit  # pylint:disable=import-error,no-name-in-module

from boxsdk.network.default_network import DefaultNetwork
from boxsdk.config import API
from boxsdk.exception import BoxOAuthException


class OAuth2(object):
    """
    Responsible for handling OAuth2 for the Box API. Can authenticate and refresh tokens.
    """

    def __init__(
            self,
            client_id,
            client_secret,
            store_tokens=None,
            box_device_id='0',
            box_device_name='',
            access_token=None,
            refresh_token=None,
            network_layer=None,
            refresh_lock=None,
    ):
        """
        :param client_id:
            Box API key used for identifying the application the user is authenticating with.
        :type client_id:
            `unicode`
        :param client_secret:
            Box API secret used for making OAuth2 requests.
        :type client_secret:
            `unicode`
        :param store_tokens:
            Optional callback for getting access to tokens for storing them.
        :type store_tokens:
            `callable`
        :param box_device_id:
            Optional unique ID of this device. Used for applications that want to support device-pinning.
        :type box_device_id:
            `unicode`
        :param box_device_name:
            Optional human readable name for this device.
        :type box_device_name:
            `unicode`
        :param access_token:
            Access token to use for auth until it expires.
        :type access_token:
            `unicode`
        :param refresh_token:
            Refresh token to use for auth until it expires or is used.
        :type refresh_token:
            `unicode`
        :param network_layer:
            If specified, use it to make network requests. If not, the default network implementation will be used.
        :type network_layer:
            :class:`Network`
        :param refresh_lock:
            Lock used to synchronize token refresh. If not specified, then a :class:`threading.Lock` will be used.
        :type refresh_lock:
            Context Manager
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._store_tokens_callback = store_tokens
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._network_layer = network_layer if network_layer else DefaultNetwork()
        self._refresh_lock = refresh_lock or Lock()
        self._box_device_id = box_device_id
        self._box_device_name = box_device_name

    @property
    def access_token(self):
        """
        Get the current access token.

        :return:
            current access token
        :rtype:
            `unicode`
        """
        return self._access_token

    def get_authorization_url(self, redirect_url):
        """
        Get the authorization url based on the client id and the redirect url passed in

        :param redirect_url:
            An HTTPS URI or custom URL scheme where the response will be redirected. Optional if the redirect URI is
            registered with Box already.
        :type redirect_url:
            `unicode` or None
        :return:
            A tuple of the URL of Box's authorization page and the CSRF token.
            This is the URL that your application should forward the user to in first leg of OAuth 2.
        :rtype:
            (`unicode`, `unicode`)
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
        return urlunsplit(('', '', API.OAUTH2_AUTHORIZE_URL, query_string, '')), csrf_token

    def authenticate(self, auth_code):
        """
        Send token request and return the access_token, refresh_token tuple. The access token and refresh token will be
        stored by calling the `store_tokens` callback if provided in __init__.

        :param auth_code:
            An authorization code you retrieved in the first leg of OAuth 2.
        :type auth_code:
            `unicode` or None

        :return:
            (access_token, refresh_token)
        :rtype:
            (`unicode`, `unicode`)
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

    def _refresh(self, access_token):
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

    def _get_tokens(self):
        """
        Get the current access and refresh tokens.

        This is a protected method that can be overridden to look up tokens
        from an external source (the inverse of the `store_tokens` callback).

        This method does not need to update this object's private token
        attributes. Its caller in :class:`OAuth2` is responsible for that.

        :return:
            Tuple containing the current access token and refresh token.
            One or both of them may be `None`, if they aren't set.
        :rtype:
            `tuple` of ((`unicode` or `None`), (`unicode` or `None`))
        """
        return self._access_token, self._refresh_token

    def refresh(self, access_token_to_refresh):
        """
        Refresh the access token and the refresh token and return the access_token, refresh_token tuple. The access
        token and refresh token will be stored by calling the `store_tokens` callback if provided in __init__.

        :param access_token_to_refresh:
            The expired access token, which needs to be refreshed.
            Pass `None` if you don't have the access token.
        :type access_token_to_refresh:
            `unicode` or `None`
        :return:
            Tuple containing the new access token and refresh token.
            The refresh token may be `None`, if the authentication scheme
            doesn't use one, or keeps it hidden from this client.
        :rtype:
            `tuple` of (`unicode`, (`unicode` or `None`))
        """
        with self._refresh_lock:
            access_token, refresh_token = self._get_and_update_current_tokens()
            # The lock here is for handling that case that multiple requests fail, due to access token expired, at the
            # same time to avoid multiple session renewals.
            if (access_token is None) or (access_token_to_refresh == access_token):
                # If the active access token is the same as the token needs to
                # be refreshed, or if we don't currently have any active access
                # token, we make the request to refresh the token.
                return self._refresh(access_token_to_refresh)
            else:
                # If the active access token (self._access_token) is not the same as the token needs to be refreshed,
                # it means the expired token has already been refreshed. Simply return the current active tokens.
                return access_token, refresh_token

    @staticmethod
    def _get_state_csrf_token():
        """ Generate a random state CSRF token to be used in the authorization url.
        Example: box_csrf_token_Iijw9aU31sNdgiQu

        :return:
            The security token
        :rtype:
            `unicode`
        """
        system_random = random.SystemRandom()
        ascii_alphabet = string.ascii_letters + string.digits
        ascii_len = len(ascii_alphabet)
        return 'box_csrf_token_' + ''.join(ascii_alphabet[int(system_random.random() * ascii_len)] for _ in range(16))

    def _store_tokens(self, access_token, refresh_token):
        self._update_current_tokens(access_token, refresh_token)
        if self._store_tokens_callback is not None:
            self._store_tokens_callback(access_token, refresh_token)

    def _get_and_update_current_tokens(self):
        """Get the current access and refresh tokens, while also storing them in this object's private attributes.

        :return:
            Same as for :meth:`_get_tokens()`.
        """
        tokens = self._get_tokens()
        self._update_current_tokens(*tokens)
        return tokens

    def _update_current_tokens(self, access_token, refresh_token):
        """Store the latest tokens in this object's private attributes.

        :param access_token:
            The latest access token.
            May be `None`, if it hasn't been provided.
        :type access_token:
            `unicode` or `None`
        :param refresh_token:
            The latest refresh token.
            May be `None`, if the authentication scheme doesn't use one, or if
            it hasn't been provided.
        :type refresh_token:
            `unicode` or `None`
        """
        self._access_token, self._refresh_token = access_token, refresh_token

    def send_token_request(self, data, access_token, expect_refresh_token=True):
        """
        Send the request to acquire or refresh an access token.

        :param data:
            Dictionary containing the request parameters as specified by the Box API.
        :type data:
            `dict`
        :param access_token:
            The current access token.
        :type access_token:
            `unicode` or None
        :return:
            The access token and refresh token.
        :rtype:
            (`unicode`, `unicode`)
        """
        url = '{base_auth_url}/token'.format(base_auth_url=API.OAUTH2_API_URL)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        network_response = self._network_layer.request(
            'POST',
            url,
            data=data,
            headers=headers,
            access_token=access_token,
        )
        if not network_response.ok:
            raise BoxOAuthException(network_response.status_code, network_response.content, url, 'POST')
        try:
            response = network_response.json()
            access_token = response['access_token']
            refresh_token = response.get('refresh_token', None)
            if refresh_token is None and expect_refresh_token:
                raise BoxOAuthException(network_response.status_code, network_response.content, url, 'POST')
        except (ValueError, KeyError):
            raise BoxOAuthException(network_response.status_code, network_response.content, url, 'POST')
        self._store_tokens(access_token, refresh_token)
        return self._access_token, self._refresh_token

    def revoke(self):
        """
        Revoke the authorization for the current access/refresh token pair.
        """
        with self._refresh_lock:
            access_token, refresh_token = self._get_and_update_current_tokens()
            token_to_revoke = access_token or refresh_token
            if token_to_revoke is None:
                return
            url = '{base_auth_url}/revoke'.format(base_auth_url=API.OAUTH2_API_URL)
            network_response = self._network_layer.request(
                'POST',
                url,
                data={
                    'client_id': self._client_id,
                    'client_secret': self._client_secret,
                    'token': token_to_revoke,
                },
                access_token=access_token,
            )
            if not network_response.ok:
                raise BoxOAuthException(network_response.status_code, network_response.content, url, 'POST')
            self._store_tokens(None, None)
