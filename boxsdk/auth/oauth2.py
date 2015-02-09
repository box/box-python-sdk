# coding: utf-8

from __future__ import unicode_literals

from threading import Lock
import random
import string  # pylint:disable=deprecated-module

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
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._store_tokens = store_tokens
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._network_layer = network_layer if network_layer else DefaultNetwork()
        self._refresh_lock = Lock()
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
        Get the authorization url based on the client id and the redirect url, passed in

        :param redirect_url:
            An HTTPS URI or custom URL scheme where the response will be redirected. Optional if the redirect URI is
            registered with Box already.
        :type redirect_url:
            `unicode`
        :return:
            A tuple of the URL of Box’s authorization page and the CSRF token.
            This is the URL that your application should forward the user to in first leg of OAuth 2.
        :rtype:
            (`unicode`, `unicode`)
        """
        csrf_token = self._get_state_csrf_token()
        return '{0}?state={1}&response_type=code&client_id={2}&redirect_uri={3}'.format(
            API.OAUTH2_AUTHORIZE_URL,
            csrf_token,
            self._client_id,
            redirect_url,
        ), csrf_token

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

    def refresh(self, access_token_to_refresh):
        """
        Refresh the access token and the refresh token and return the access_token, refresh_token tuple. The access
        token and refresh token will be stored by calling the `store_tokens` callback if provided in __init__.

        :param access_token_to_refresh:
            The expired access token, which needs to be refreshed.
        :type access_token_to_refresh:
            `unicode`
        """
        with self._refresh_lock:
            # The lock here is for handling that case that multiple requests fail, due to access token expired, at the
            # same time to avoid multiple session renewals.
            if access_token_to_refresh == self._access_token:
                # If the active access token is the same as the token needs to be refreshed, we make the request to
                # refresh the token.
                return self._refresh(access_token_to_refresh)
            else:
                # If the active access token (self._access_token) is not the same as the token needs to be refreshed,
                # it means the expired token has already been refreshed. Simply return the current active tokens.
                return self._access_token, self._refresh_token

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

    def send_token_request(self, data, access_token):
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
            access_token=access_token
        )
        if not network_response.ok:
            raise BoxOAuthException(network_response.status_code, network_response.content, url, 'POST')
        try:
            response = network_response.json()
            self._access_token = response['access_token']
            self._refresh_token = response['refresh_token']
        except (ValueError, KeyError):
            raise BoxOAuthException(network_response.status_code, network_response.content, url, 'POST')
        if self._store_tokens:
            self._store_tokens(self._access_token, self._refresh_token)
        return self._access_token, self._refresh_token
