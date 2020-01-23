# coding: utf-8

from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
import json
import random
import string
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
import jwt
from six import binary_type, string_types, raise_from, text_type

from ..config import API
from ..exception import BoxOAuthException
from .oauth2 import OAuth2
from ..object.user import User
from ..util.compat import NoneType


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
            rsa_private_key_file_sys_path=None,
            rsa_private_key_passphrase=None,
            user=None,
            store_tokens=None,
            box_device_id='0',
            box_device_name='',
            access_token=None,
            session=None,
            jwt_algorithm='RS256',
            rsa_private_key_data=None,
            **kwargs
    ):
        """Extends baseclass method.

        Must pass exactly one of either `rsa_private_key_file_sys_path` or
        `rsa_private_key_data`.

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
            (optional) Path to an RSA private key file, used for signing the JWT assertion.
        :type rsa_private_key_file_sys_path:
            `unicode`
        :param rsa_private_key_passphrase:
            Passphrase used to unlock the private key. Do not pass a unicode string - this must be bytes.
        :type rsa_private_key_passphrase:
            `bytes` or None
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

            <https://developer.box.com/en/guides/applications/>
            <https://developer.box.com/en/guides/authentication/select/>
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
        :param rsa_private_key_data:
            (optional) Contents of RSA private key, used for signing the JWT assertion. Do not pass a
            unicode string. Can pass a byte string, or a file-like object that returns bytes, or an
            already-loaded `RSAPrivateKey` object.
        :type rsa_private_key_data:   `bytes` or :class:`io.IOBase` or :class:`RSAPrivateKey`
        """
        user_id = self._normalize_user_id(user)
        rsa_private_key = self._normalize_rsa_private_key(
            file_sys_path=rsa_private_key_file_sys_path,
            data=rsa_private_key_data,
            passphrase=rsa_private_key_passphrase,
        )
        del rsa_private_key_data
        del rsa_private_key_file_sys_path
        super(JWTAuth, self).__init__(
            client_id,
            client_secret,
            store_tokens=store_tokens,
            box_device_id=box_device_id,
            box_device_name=box_device_name,
            access_token=access_token,
            refresh_token=None,
            session=session,
            **kwargs
        )
        self._rsa_private_key = rsa_private_key
        self._enterprise_id = enterprise_id
        self._jwt_algorithm = jwt_algorithm
        self._jwt_key_id = jwt_key_id
        self._user_id = user_id

    def _construct_and_send_jwt_auth(self, sub, sub_type, now_time=None):
        """
        Construct the claims used for JWT auth and send a request to get a JWT.
        Pass an enterprise ID to get an enterprise token (which can be used to provision/deprovision users),
        or a user ID to get a user token.

        :param sub:
            The enterprise ID or user ID to auth.
        :type sub:
            `unicode`
        :param sub_type:
            Either 'enterprise' or 'user'
        :type sub_type:
            `unicode`
        :param now_time:
            Optional. The current UTC time is needed in order to construct the expiration time of the JWT claim.
            If None, `datetime.utcnow()` will be used.
        :type now_time:
            `datetime` or None
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
        if now_time is None:
            now_time = datetime.utcnow()
        now_plus_30 = now_time + timedelta(seconds=30)
        assertion = jwt.encode(
            {
                'iss': self._client_id,
                'sub': sub,
                'box_sub_type': sub_type,
                'aud': 'https://api.box.com/oauth2/token',
                'jti': jti,
                'exp': int((now_plus_30 - datetime(1970, 1, 1)).total_seconds()),
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

    def _auth_with_jwt(self, sub, sub_type):
        """
        Auth with JWT.
        If authorization fails because the expiration time is out of sync with the Box servers,
        retry using the time returned in the error response.
        Pass an enterprise ID to get an enterprise token (which can be used to provision/deprovision users),
        or a user ID to get a user token.

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
        attempt_number = 0
        jwt_time = None
        while True:
            try:
                return self._construct_and_send_jwt_auth(sub, sub_type, jwt_time)
            except BoxOAuthException as ex:
                network_response = ex.network_response
                code = network_response.status_code  # pylint: disable=maybe-no-member
                box_datetime = self._get_date_header(network_response)

                if attempt_number >= API.MAX_RETRY_ATTEMPTS:
                    raise ex

                if (code == 429 or code >= 500):
                    jwt_time = None
                elif box_datetime is not None and self._was_exp_claim_rejected_due_to_clock_skew(network_response):
                    jwt_time = box_datetime
                else:
                    raise ex

                time_delay = self._session.get_retry_after_time(attempt_number, network_response.headers.get('Retry-After', None))  # pylint: disable=maybe-no-member
                time.sleep(time_delay)
                attempt_number += 1
                self._logger.debug('Retrying JWT request')

    @staticmethod
    def _get_date_header(network_response):
        """
        Get datetime object for Date header, if the Date header is available.

        :param network_response:
            The response from the Box API that should include a Date header.
        :type network_response:
            :class:`Response`
        :return:
            The datetime parsed from the Date header, or None if the header is absent or if it couldn't be parsed.
        :rtype:
            `datetime` or `None`
        """
        box_date_header = network_response.headers.get('Date', None)
        if box_date_header is not None:
            try:
                return datetime.strptime(box_date_header, '%a, %d %b %Y %H:%M:%S %Z')
            except ValueError:
                pass
        return None

    @staticmethod
    def _was_exp_claim_rejected_due_to_clock_skew(network_response):
        """
        Determine whether the network response indicates that the authorization request was rejected because of
        the exp claim. This can happen if the current system time is too different from the Box server time.

        Returns True if the status code is 400, the error code is invalid_grant, and the error description indicates
        a problem with the exp claim; False, otherwise.

        :param network_response:
        :type network_response:
            :class:`Response`
        :rtype:
            `bool`
        """
        status_code = network_response.status_code
        try:
            json_response = network_response.json()
        except ValueError:
            return False
        error_code = json_response.get('error', '')
        error_description = json_response.get('error_description', '')
        return status_code == 400 and error_code == 'invalid_grant' and 'exp' in error_description

    def authenticate_user(self, user=None):
        """
        Get an access token for a User.

        May be one of this application's created App User. Depending on the
        configured User Access Level, may also be any other App User or Managed
        User in the enterprise.

        <https://developer.box.com/en/guides/applications/>
        <https://developer.box.com/en/guides/authentication/select/>

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
            new_access_token = self.authenticate_instance()
        else:
            new_access_token = self.authenticate_user()
        return new_access_token, None

    @classmethod
    def _normalize_rsa_private_key(cls, file_sys_path, data, passphrase=None):
        if len(list(filter(None, [file_sys_path, data]))) != 1:
            raise TypeError("must pass exactly one of either rsa_private_key_file_sys_path or rsa_private_key_data")
        if file_sys_path:
            with open(file_sys_path, 'rb') as key_file:
                data = key_file.read()
        if hasattr(data, 'read') and callable(data.read):
            data = data.read()
        if isinstance(data, text_type):
            try:
                data = data.encode('ascii')
            except UnicodeError:
                raise_from(
                    TypeError("rsa_private_key_data must contain binary data (bytes/str), not a text/unicode string"),
                    None,
                )
        if isinstance(data, binary_type):
            passphrase = cls._normalize_rsa_private_key_passphrase(passphrase)
            return serialization.load_pem_private_key(
                data,
                password=passphrase,
                backend=default_backend(),
            )
        if isinstance(data, RSAPrivateKey):
            return data
        raise TypeError(
            'rsa_private_key_data must be binary data (bytes/str), '
            'a file-like object with a read() method, '
            'or an instance of RSAPrivateKey, '
            'but got {0!r}'
            .format(data.__class__.__name__)
        )

    @staticmethod
    def _normalize_rsa_private_key_passphrase(passphrase):
        if isinstance(passphrase, text_type):
            try:
                return passphrase.encode('ascii')
            except UnicodeError:
                raise_from(
                    TypeError("rsa_private_key_passphrase must contain binary data (bytes/str), not a text/unicode string"),
                    None,
                )
        if not isinstance(passphrase, (binary_type, NoneType)):
            raise TypeError(
                "rsa_private_key_passphrase must contain binary data (bytes/str), got {0!r}"
                .format(passphrase.__class__.__name__)
            )
        return passphrase

    @classmethod
    def from_settings_dictionary(cls, settings_dictionary, **kwargs):
        """
        Create an auth instance as defined by the given settings dictionary.

        The dictionary should have the structure of the JSON file downloaded from the Box Developer Console.

        :param settings_dictionary:       Dictionary containing settings for configuring app auth.
        :type settings_dictionary:        `dict`
        :return:                        Auth instance configured as specified by the config dictionary.
        :rtype:                         :class:`JWTAuth`
        """
        if 'boxAppSettings' not in settings_dictionary:
            raise ValueError('boxAppSettings not present in configuration')
        return cls(
            client_id=settings_dictionary['boxAppSettings']['clientID'],
            client_secret=settings_dictionary['boxAppSettings']['clientSecret'],
            enterprise_id=settings_dictionary.get('enterpriseID', None),
            jwt_key_id=settings_dictionary['boxAppSettings']['appAuth'].get('publicKeyID', None),
            rsa_private_key_data=settings_dictionary['boxAppSettings']['appAuth'].get('privateKey', None),
            rsa_private_key_passphrase=settings_dictionary['boxAppSettings']['appAuth'].get('passphrase', None),
            **kwargs
        )

    @classmethod
    def from_settings_file(cls, settings_file_sys_path, **kwargs):
        """
        Create an auth instance as defined by a JSON file downloaded from the Box Developer Console.
        See https://developer.box.com/en/guides/authentication/jwt/ for more information.

        :param settings_file_sys_path:    Path to the JSON file containing the configuration.
        :type settings_file_sys_path:     `unicode`
        :return:                        Auth instance configured as specified by the JSON file.
        :rtype:                         :class:`JWTAuth`
        """
        with open(settings_file_sys_path) as config_file:
            config_dictionary = json.load(config_file)
            return cls.from_settings_dictionary(config_dictionary, **kwargs)
