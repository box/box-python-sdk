# coding: utf-8

from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
import random
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt
from six import string_types, text_type

from .oauth2 import OAuth2
from ..object.user import User
from ..util.compat import total_seconds


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
            user=None,
            store_tokens=None,
            box_device_id='0',
            box_device_name='',
            access_token=None,
            network_layer=None,
            jwt_algorithm='RS256',
    ):
        """Extends baseclass method.

        If both `enterprise_id` and `user` are non-`None`, the `user` takes
        precedence when `refresh()` is called. This can be overruled with a
        call to `authenticate_instance()`.

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

            May be `None`, if the caller knows that it will not be
            authenticating as an enterprise instance / service account.

            If `user` is passed, this value is not used, unless
            `authenticate_instance()` is called to clear the user and
            authenticate as the enterprise instance.
        :type enterprise_id:
            `unicode` or `None`
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
        :param user:
            (optional) The user to authenticate, expressed as a Box User ID or
            as a :class:`User` instance.

            This value is not required. But if it is provided, then the user
            will be auto-authenticated at the time of the first API call or
            when calling `authenticate_user()` without any arguments.

            Should be `None` if the intention is to authenticate as the
            enterprise instance / service account. If both `enterprise_id` and
            `user` are non-`None`, the `user` takes precedense when `refresh()`
            is called.

            May be one of this application's created App User. Depending on the
            configured User Access Level, may also be any other App User or
            Managed User in the enterprise.

            <https://docs.box.com/docs/configuring-box-platform#section-3-enabling-app-auth-and-app-users>
            <https://docs.box.com/docs/authentication#section-choosing-an-authentication-type>
        :type user:
            `unicode` or :class:`User` or `None`
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
        user_id = self._normalize_user_id(user)
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
        with open(rsa_private_key_file_sys_path, 'rb') as key_file:
            self._rsa_private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=rsa_private_key_passphrase,
                backend=default_backend(),
            )
        self._enterprise_id = enterprise_id
        self._jwt_algorithm = jwt_algorithm
        self._jwt_key_id = jwt_key_id
        self._user_id = user_id

    def _auth_with_jwt(self, sub, sub_type):
        """
        Get an access token for use with Box Developer Edition. Pass an enterprise ID to get an enterprise token
        (which can be used to provision/deprovision users), or a user ID to get a user token.

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

    def authenticate_user(self, user=None):
        """
        Get an access token for a User.

        May be one of this application's created App User. Depending on the
        configured User Access Level, may also be any other App User or Managed
        User in the enterprise.

        <https://docs.box.com/docs/configuring-box-platform#section-3-enabling-app-auth-and-app-users>
        <https://docs.box.com/docs/authentication#section-choosing-an-authentication-type>

        :param user:
            (optional) The user to authenticate, expressed as a Box User ID or
            as a :class:`User` instance.

            If not given, then the most recently provided user ID, if
            available, will be used.
        :type user:
            `unicode` or :class:`User`
        :raises:
            :exc:`ValueError` if no user ID was passed and the object is not
            currently configured with one.
        :return:
            The access token for the user.
        :rtype:
            `unicode`
        """
        sub = self._normalize_user_id(user) or self._user_id
        if not sub:
            raise ValueError("authenticate_user: Requires the user ID, but it was not provided.")
        self._user_id = sub
        return self._auth_with_jwt(sub, 'user')

    authenticate_app_user = authenticate_user

    @classmethod
    def _normalize_user_id(cls, user):
        """Get a Box user ID from a selection of supported param types.

        :param user:
            An object representing the user or user ID.

            Currently supported types are `unicode` (which represents the user
            ID) and :class:`User`.

            If `None`, returns `None`.
        :raises:  :exc:`TypeError` for unsupported types.
        :rtype:   `unicode` or `None`
        """
        if user is None:
            return None
        if isinstance(user, User):
            return user.object_id
        if isinstance(user, string_types):
            return text_type(user)
        raise TypeError("Got unsupported type {0!r} for user.".format(user.__class__.__name__))

    def authenticate_instance(self, enterprise=None):
        """
        Get an access token for a Box Developer Edition enterprise.

        :param enterprise:
            The ID of the Box Developer Edition enterprise.

            Optional if the value was already given to `__init__`,
            otherwise required.
        :type enterprise:   `unicode` or `None`
        :raises:
            :exc:`ValueError` if `None` was passed for the enterprise ID here
            and in `__init__`, or if the non-`None` value passed here does not
            match the non-`None` value passed to `__init__`.
        :return:
            The access token for the enterprise which can provision/deprovision app users.
        :rtype:
            `unicode`
        """
        enterprises = [enterprise, self._enterprise_id]
        if not any(enterprises):
            raise ValueError("authenticate_instance: Requires the enterprise ID, but it was not provided.")
        if all(enterprises) and (enterprise != self._enterprise_id):
            raise ValueError(
                "authenticate_instance: Given enterprise ID {given_enterprise!r}, but {auth} already has ID {existing_enterprise!r}"
                .format(auth=self, given_enterprise=enterprise, existing_enterprise=self._enterprise_id)
            )
        if not self._enterprise_id:
            self._enterprise_id = enterprise
        self._user_id = None
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
            return self.authenticate_user()
