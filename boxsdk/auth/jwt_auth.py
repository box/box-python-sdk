from datetime import datetime, timedelta
import json
import random
import string
from io import IOBase
from typing import Optional, Union, Callable, TYPE_CHECKING, Any
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
import jwt

from boxsdk.auth.server_auth import ServerAuth

if TYPE_CHECKING:
    from boxsdk.network.network_interface import Network
    from boxsdk.object.user import User


class JWTAuth(ServerAuth):
    """
    Responsible for handling JWT Auth for Box Developer Edition. Can authenticate enterprise instances or app users.
    """
    _GRANT_TYPE = 'urn:ietf:params:oauth:grant-type:jwt-bearer'

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            enterprise_id: Optional[str],
            jwt_key_id: str,
            rsa_private_key_file_sys_path: Optional[str] = None,
            rsa_private_key_passphrase: Optional[Union[str, bytes]] = None,
            user: Optional[Union[str, 'User']] = None,
            store_tokens: Optional[Callable[[str, str], None]] = None,
            box_device_id: str = '0',
            box_device_name: str = '',
            access_token: str = None,
            session: Optional['Network'] = None,
            jwt_algorithm: str = 'RS256',
            rsa_private_key_data: Union[bytes, IOBase, RSAPrivateKey] = None,
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
        :param client_secret:
            Box API secret used for making OAuth2 requests.
        :param enterprise_id:
            The ID of the Box Developer Edition enterprise.

            May be `None`, if the caller knows that it will not be
            authenticating as an enterprise instance / service account.

            If `user` is passed, this value is not used, unless
            `authenticate_instance()` is called to clear the user and
            authenticate as the enterprise instance.
        :param jwt_key_id:
            Key ID for the JWT assertion.
        :param rsa_private_key_file_sys_path:
            (optional) Path to an RSA private key file, used for signing the JWT assertion.
        :param rsa_private_key_passphrase:
            Passphrase used to unlock the private key. Do not pass a unicode string - this must be bytes.
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
        :param store_tokens:
            Optional callback to get access to tokens and store them. Callback method should take two
             paramaters - access_token: str and refresh_token: str - and it is not expected to return anything.
        :param box_device_id:
            Optional unique ID of this device. Used for applications that want to support device-pinning.
        :param box_device_name:
            Optional human-readable name for this device.
        :param access_token:
            Access token to use for auth until it expires.
        :param session:
            If specified, use it to make network requests. If not, the default session will be used.
        :param jwt_algorithm:
            Which algorithm to use for signing the JWT assertion. Must be one of 'RS256', 'RS384', 'RS512'.
        :param rsa_private_key_data:
            (optional) Contents of RSA private key, used for signing the JWT assertion. Do not pass a
            unicode string. Can pass a byte string, or a file-like object that returns bytes, or an
            already-loaded `RSAPrivateKey` object.
        """
        rsa_private_key = self._normalize_rsa_private_key(
            file_sys_path=rsa_private_key_file_sys_path,
            data=rsa_private_key_data,
            passphrase=rsa_private_key_passphrase,
        )
        del rsa_private_key_data
        del rsa_private_key_file_sys_path
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            enterprise_id=enterprise_id,
            user=user,
            store_tokens=store_tokens,
            box_device_id=box_device_id,
            box_device_name=box_device_name,
            access_token=access_token,
            refresh_token=None,
            session=session,
            **kwargs
        )
        self._rsa_private_key = rsa_private_key
        self._jwt_algorithm = jwt_algorithm
        self._jwt_key_id = jwt_key_id

    def _fetch_access_token(self, subject_id: str, subject_type: str, now_time: Optional[datetime] = None) -> str:
        """
        Construct the claims used for JWT auth and send a request to get a JWT.
        Pass an enterprise ID to get an enterprise token (which can be used to provision/deprovision users),
        or a user ID to get a user token.

        :param subject_id:
            The enterprise ID or user ID to auth.
        :param subject_type:
            Either 'enterprise' or 'user'
        :param now_time:
            Optional. The current UTC time is needed in order to construct the expiration time of the JWT claim.
            If None, `datetime.utcnow()` will be used.
        :return:
            The access token for the enterprise or app user.
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
                'sub': subject_id,
                'box_sub_type': subject_type,
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

    @classmethod
    def _normalize_rsa_private_key(
            cls,
            file_sys_path: str,
            data: Union[bytes, IOBase, RSAPrivateKey],
            passphrase: Optional[Union[str, bytes]] = None
    ) -> Any:
        if len(list(filter(None, [file_sys_path, data]))) != 1:
            raise TypeError("must pass exactly one of either rsa_private_key_file_sys_path or rsa_private_key_data")
        if file_sys_path:
            with open(file_sys_path, 'rb') as key_file:
                data = key_file.read()
        if hasattr(data, 'read') and callable(data.read):
            data = data.read()
        if isinstance(data, str):
            try:
                data = data.encode('ascii')
            except UnicodeError as unicode_error:
                raise TypeError(
                    "rsa_private_key_data must contain binary data (bytes/str), not a text/unicode string"
                ) from unicode_error

        if isinstance(data, bytes):
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
            f'but got {data.__class__.__name__!r}'
        )

    @staticmethod
    def _normalize_rsa_private_key_passphrase(passphrase: Any):
        if isinstance(passphrase, str):
            try:
                return passphrase.encode('ascii')
            except UnicodeError as unicode_error:
                raise TypeError(
                    "rsa_private_key_passphrase must contain binary data (bytes/str), not a text/unicode string"
                ) from unicode_error

        if not isinstance(passphrase, (bytes, type(None))):
            raise TypeError(
                f"rsa_private_key_passphrase must contain binary data (bytes/str), "
                f"got {passphrase.__class__.__name__!r}"
            )
        return passphrase

    @classmethod
    def from_settings_dictionary(cls, settings_dictionary: dict, **kwargs: Any) -> 'JWTAuth':
        """
        Create an auth instance as defined by the given settings dictionary.

        The dictionary should have the structure of the JSON file downloaded from the Box Developer Console.

        :param settings_dictionary:       Dictionary containing settings for configuring app auth.
        :return:                        Auth instance configured as specified by the config dictionary.
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
    def from_settings_file(cls, settings_file_sys_path: str, **kwargs: Any) -> 'JWTAuth':
        """
        Create an auth instance as defined by a JSON file downloaded from the Box Developer Console.
        See https://developer.box.com/en/guides/authentication/jwt/ for more information.

        :param settings_file_sys_path:    Path to the JSON file containing the configuration.
        :return:                        Auth instance configured as specified by the JSON file.
        """
        with open(settings_file_sys_path, encoding='utf-8') as config_file:
            config_dictionary = json.load(config_file)
            return cls.from_settings_dictionary(config_dictionary, **kwargs)
