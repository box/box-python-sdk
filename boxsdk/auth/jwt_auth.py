# coding: utf-8

from __future__ import unicode_literals

from datetime import datetime, timedelta
import random
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt

from .oauth2 import OAuth2
from boxsdk.util.compat import total_seconds


class JWTAuth(OAuth2):
    """
    Responsible for handling JWT Auth for Box Developer Edition. Can authenticate enterprise instances or app users.
    """
    _GRANT_TYPE = 'urn:ietf:params:oauth:grant-type:jwt-bearer'

    def __init__(
            self,
            client_id,
            client_secret,
            enterprise_id,
            jwt_key_id,
            rsa_private_key_file_sys_path,
            rsa_private_key_passphrase=None,
            store_tokens=None,
            box_device_id='0',
            box_device_name='',
            access_token=None,
            network_layer=None,
            jwt_algorithm='RS256',
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
        :param enterprise_id:
            The ID of the Box Developer Edition enterprise.
        :type enterprise_id:
            `unicode`
        :param jwt_key_id:
            Key ID for the JWT assertion.
        :type jwt_key_id:
            `unicode`
        :param rsa_private_key_file_sys_path:
            Path to an RSA private key file, used for signing the JWT assertion.
        :type rsa_private_key_file_sys_path:
            `unicode`
        :param rsa_private_key_passphrase:
            Passphrase used to unlock the private key. Do not pass a unicode string - this must be bytes.
        :type rsa_private_key_passphrase:
            `str` or None
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
        :param network_layer:
            If specified, use it to make network requests. If not, the default network implementation will be used.
        :type network_layer:
            :class:`Network`
        :param jwt_algorithm:
            Which algorithm to use for signing the JWT assertion. Must be one of 'RS256', 'RS384', 'RS512'.
        :type jwt_algorithm:
            `unicode`
        """
        super(JWTAuth, self).__init__(
            client_id,
            client_secret,
            store_tokens=store_tokens,
            box_device_id=box_device_id,
            box_device_name=box_device_name,
            access_token=access_token,
            refresh_token=None,
            network_layer=network_layer,
        )
        with open(rsa_private_key_file_sys_path) as key_file:
            self._rsa_private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=rsa_private_key_passphrase,
                backend=default_backend(),
            )
        self._enterprise_id = enterprise_id
        self._jwt_algorithm = jwt_algorithm
        self._jwt_key_id = jwt_key_id
        self._user_id = None

    def _auth_with_jwt(self, sub, sub_type):
        """
        Get an access token for use with Box Developer Edition. Pass an enterprise ID to get an enterprise token
        (which can be used to provision/deprovision users), or a user ID to get an app user token.

        :param sub:
            The enterprise ID or user ID to auth.
        :type sub:
            `unicode`
        :param sub_type:
            Either 'enterprise' or 'user'
        :type sub_type:
            `unicode`
        :return:
            The access token for the enterprise or app user.
        :rtype:
            `unicode`
        """
        system_random = random.SystemRandom()
        jti_length = system_random.randint(16, 128)
        ascii_alphabet = string.ascii_letters + string.digits
        ascii_len = len(ascii_alphabet)
        jti = ''.join(ascii_alphabet[int(system_random.random() * ascii_len)] for _ in range(jti_length))
        now_plus_30 = datetime.utcnow() + timedelta(seconds=30)
        assertion = jwt.encode(
            {
                'iss': self._client_id,
                'sub': sub,
                'box_sub_type': sub_type,
                'aud': 'https://api.box.com/oauth2/token',
                'jti': jti,
                'exp': int(total_seconds(now_plus_30 - datetime(1970, 1, 1))),
            },
            self._rsa_private_key,
            algorithm=self._jwt_algorithm,
            headers={
                'kid': self._jwt_key_id,
            },
        )
        data = {
            'grant_type': self._GRANT_TYPE,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'assertion': assertion,
        }
        if self._box_device_id:
            data['box_device_id'] = self._box_device_id
        if self._box_device_name:
            data['box_device_name'] = self._box_device_name
        return self.send_token_request(data, access_token=None, expect_refresh_token=False)[0]

    def authenticate_app_user(self, user):
        """
        Get an access token for an App User (part of Box Developer Edition).

        :param user:
            The user to authenticate.
        :type user:
            :class:`User`
        :return:
            The access token for the app user.
        :rtype:
            `unicode`
        """
        sub = self._user_id = user.object_id
        return self._auth_with_jwt(sub, 'user')

    def authenticate_instance(self):
        """
        Get an access token for a Box Developer Edition enterprise.

        :return:
            The access token for the enterprise which can provision/deprovision app users.
        :rtype:
            `unicode`
        """
        return self._auth_with_jwt(self._enterprise_id, 'enterprise')

    def _refresh(self, access_token):
        """
        Base class override.

        Instead of refreshing an access token using a refresh token, we just issue a new JWT request.
        """
        # pylint:disable=unused-argument
        if self._user_id is None:
            return self.authenticate_instance()
        else:
            return self._auth_with_jwt(self._user_id, 'user')
