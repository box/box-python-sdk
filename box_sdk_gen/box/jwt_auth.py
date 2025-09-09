from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from box_sdk_gen.serialization.json import deserialize

from typing import List

from box_sdk_gen.schemas.post_o_auth_2_token import PostOAuth2TokenGrantTypeField

from box_sdk_gen.schemas.post_o_auth_2_token import PostOAuth2TokenSubjectTokenTypeField

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.schemas.access_token import AccessToken

from box_sdk_gen.schemas.post_o_auth_2_token import PostOAuth2Token

from box_sdk_gen.schemas.post_o_auth_2_revoke import PostOAuth2Revoke

from box_sdk_gen.box.token_storage import TokenStorage

from box_sdk_gen.box.token_storage import InMemoryTokenStorage

from box_sdk_gen.serialization.json import json_to_serialized_data

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import read_text_from_file

from box_sdk_gen.internal.utils import is_browser

from box_sdk_gen.internal.utils import get_epoch_time_in_seconds

from box_sdk_gen.internal.utils import create_jwt_assertion

from box_sdk_gen.internal.utils import JwtSignOptions

from box_sdk_gen.internal.utils import JwtKey

from box_sdk_gen.internal.utils import JwtAlgorithm

from box_sdk_gen.internal.utils import PrivateKeyDecryptor

from box_sdk_gen.internal.utils import DefaultPrivateKeyDecryptor

from box_sdk_gen.managers.authorization import AuthorizationManager

from box_sdk_gen.box.errors import BoxSDKError


class JwtConfigAppSettingsAppAuth(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'public_key_id': 'publicKeyID',
        'private_key': 'privateKey',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'publicKeyID': 'public_key_id',
        'privateKey': 'private_key',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(self, public_key_id: str, private_key: str, passphrase: str, **kwargs):
        """
        :param public_key_id: Public key ID
        :type public_key_id: str
        :param private_key: Private key
        :type private_key: str
        :param passphrase: Passphrase
        :type passphrase: str
        """
        super().__init__(**kwargs)
        self.public_key_id = public_key_id
        self.private_key = private_key
        self.passphrase = passphrase


class JwtConfigAppSettings(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'client_id': 'clientID',
        'client_secret': 'clientSecret',
        'app_auth': 'appAuth',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'clientID': 'client_id',
        'clientSecret': 'client_secret',
        'appAuth': 'app_auth',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        app_auth: JwtConfigAppSettingsAppAuth,
        **kwargs
    ):
        """
        :param client_id: App client ID
        :type client_id: str
        :param client_secret: App client secret
        :type client_secret: str
        :param app_auth: App auth settings
        :type app_auth: JwtConfigAppSettingsAppAuth
        """
        super().__init__(**kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.app_auth = app_auth


class JwtConfigFile(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'enterprise_id': 'enterpriseID',
        'user_id': 'userID',
        'box_app_settings': 'boxAppSettings',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'enterpriseID': 'enterprise_id',
        'userID': 'user_id',
        'boxAppSettings': 'box_app_settings',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        box_app_settings: JwtConfigAppSettings,
        *,
        enterprise_id: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs
    ):
        """
        :param box_app_settings: App settings
        :type box_app_settings: JwtConfigAppSettings
        :param enterprise_id: Enterprise ID, defaults to None
        :type enterprise_id: Optional[str], optional
        :param user_id: User ID, defaults to None
        :type user_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.box_app_settings = box_app_settings
        self.enterprise_id = enterprise_id
        self.user_id = user_id


class JWTConfig:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        jwt_key_id: str,
        private_key: str,
        private_key_passphrase: str,
        *,
        enterprise_id: Optional[str] = None,
        user_id: Optional[str] = None,
        algorithm: Optional[JwtAlgorithm] = JwtAlgorithm.RS256,
        token_storage: TokenStorage = None,
        private_key_decryptor: PrivateKeyDecryptor = None
    ):
        """
        :param client_id: App client ID
        :type client_id: str
        :param client_secret: App client secret
        :type client_secret: str
        :param jwt_key_id: Public key ID
        :type jwt_key_id: str
        :param private_key: Private key
        :type private_key: str
        :param private_key_passphrase: Passphrase
        :type private_key_passphrase: str
        :param enterprise_id: Enterprise ID, defaults to None
        :type enterprise_id: Optional[str], optional
        :param user_id: User ID, defaults to None
        :type user_id: Optional[str], optional
        """
        if token_storage is None:
            token_storage = InMemoryTokenStorage()
        if private_key_decryptor is None:
            private_key_decryptor = DefaultPrivateKeyDecryptor()
        self.client_id = client_id
        self.client_secret = client_secret
        self.jwt_key_id = jwt_key_id
        self.private_key = private_key
        self.private_key_passphrase = private_key_passphrase
        self.enterprise_id = enterprise_id
        self.user_id = user_id
        self.algorithm = algorithm
        self.token_storage = token_storage
        self.private_key_decryptor = private_key_decryptor

    @staticmethod
    def from_config_json_string(
        config_json_string: str,
        *,
        token_storage: Optional[TokenStorage] = None,
        private_key_decryptor: Optional[PrivateKeyDecryptor] = None
    ) -> 'JWTConfig':
        """
        Create an auth instance as defined by a string content of JSON file downloaded from the Box Developer Console.

        See https://developer.box.com/en/guides/authentication/jwt/ for more information.

        :param config_json_string: String content of JSON file containing the configuration.
        :type config_json_string: str
        :param token_storage: Object responsible for storing token. If no custom implementation provided, the token will be stored in memory, defaults to None
        :type token_storage: Optional[TokenStorage], optional
        :param private_key_decryptor: Object responsible for decrypting private key for jwt auth. If no custom implementation provided, the DefaultPrivateKeyDecryptor will be used., defaults to None
        :type private_key_decryptor: Optional[PrivateKeyDecryptor], optional
        """
        config_json: JwtConfigFile = deserialize(
            json_to_serialized_data(config_json_string), JwtConfigFile
        )
        token_storage_to_use: Optional[TokenStorage] = (
            InMemoryTokenStorage() if token_storage == None else token_storage
        )
        private_key_decryptor_to_use: Optional[PrivateKeyDecryptor] = (
            DefaultPrivateKeyDecryptor()
            if private_key_decryptor == None
            else private_key_decryptor
        )
        new_config: 'JWTConfig' = JWTConfig(
            client_id=config_json.box_app_settings.client_id,
            client_secret=config_json.box_app_settings.client_secret,
            enterprise_id=config_json.enterprise_id,
            user_id=config_json.user_id,
            jwt_key_id=config_json.box_app_settings.app_auth.public_key_id,
            private_key=config_json.box_app_settings.app_auth.private_key,
            private_key_passphrase=config_json.box_app_settings.app_auth.passphrase,
            token_storage=token_storage_to_use,
            private_key_decryptor=private_key_decryptor_to_use,
        )
        return new_config

    @staticmethod
    def from_config_file(
        config_file_path: str,
        *,
        token_storage: Optional[TokenStorage] = None,
        private_key_decryptor: Optional[PrivateKeyDecryptor] = None
    ) -> 'JWTConfig':
        """
        Create an auth instance as defined by a JSON file downloaded from the Box Developer Console.

        See https://developer.box.com/en/guides/authentication/jwt/ for more information.

        :param config_file_path: Path to the JSON file containing the configuration.
        :type config_file_path: str
        :param token_storage: Object responsible for storing token. If no custom implementation provided, the token will be stored in memory., defaults to None
        :type token_storage: Optional[TokenStorage], optional
        :param private_key_decryptor: Object responsible for decrypting private key for jwt auth. If no custom implementation provided, the DefaultPrivateKeyDecryptor will be used., defaults to None
        :type private_key_decryptor: Optional[PrivateKeyDecryptor], optional
        """
        config_json_string: str = read_text_from_file(config_file_path)
        return JWTConfig.from_config_json_string(
            config_json_string,
            token_storage=token_storage,
            private_key_decryptor=private_key_decryptor,
        )


class BoxJWTAuth(Authentication):
    def __init__(self, config: JWTConfig, **kwargs):
        """
        :param config: An object containing all JWT configuration to use for authentication
        :type config: JWTConfig
        """
        super().__init__(**kwargs)
        self.config = config
        self.token_storage = self.config.token_storage
        self.subject_id = (
            self.config.enterprise_id
            if not self.config.enterprise_id == None
            else self.config.user_id
        )
        self.subject_type = (
            'enterprise' if not self.config.enterprise_id == None else 'user'
        )

    def refresh_token(
        self, *, network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        """
        Get new access token using JWT auth.
        :param network_session: An object to keep network session state, defaults to None
        :type network_session: Optional[NetworkSession], optional
        """
        if is_browser():
            raise BoxSDKError(
                message='JWT auth is not supported in browser environment.'
            )
        alg: JwtAlgorithm = (
            self.config.algorithm
            if not self.config.algorithm == None
            else JwtAlgorithm.RS256
        )
        claims: Dict = {
            'exp': get_epoch_time_in_seconds() + 30,
            'box_sub_type': self.subject_type,
        }
        jwt_options: JwtSignOptions = JwtSignOptions(
            algorithm=alg,
            audience='https://api.box.com/oauth2/token',
            subject=self.subject_id,
            issuer=self.config.client_id,
            jwtid=get_uuid(),
            keyid=self.config.jwt_key_id,
            private_key_decryptor=self.config.private_key_decryptor,
        )
        jwt_key: JwtKey = JwtKey(
            key=self.config.private_key, passphrase=self.config.private_key_passphrase
        )
        assertion: str = create_jwt_assertion(claims, jwt_key, jwt_options)
        auth_manager: AuthorizationManager = AuthorizationManager(
            network_session=(
                network_session if not network_session == None else NetworkSession()
            )
        )
        token: AccessToken = auth_manager.request_access_token(
            PostOAuth2TokenGrantTypeField.URN_IETF_PARAMS_OAUTH_GRANT_TYPE_JWT_BEARER,
            assertion=assertion,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
        )
        self.token_storage.store(token)
        return token

    def retrieve_token(
        self, *, network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        """
        Get the current access token. If the current access token is expired or not found, this method will attempt to refresh the token.
        :param network_session: An object to keep network session state, defaults to None
        :type network_session: Optional[NetworkSession], optional
        """
        old_token: Optional[AccessToken] = self.token_storage.get()
        if old_token == None:
            new_token: AccessToken = self.refresh_token(network_session=network_session)
            return new_token
        return old_token

    def retrieve_authorization_header(
        self, *, network_session: Optional[NetworkSession] = None
    ) -> str:
        token: AccessToken = self.retrieve_token(network_session=network_session)
        return ''.join(['Bearer ', token.access_token])

    def with_user_subject(
        self, user_id: str, *, token_storage: TokenStorage = None
    ) -> 'BoxJWTAuth':
        """
        Create a new BoxJWTAuth instance that uses the provided user ID as the subject of the JWT assertion.

        May be one of this application's created App User. Depending on the configured User Access Level, may also be any other App User or Managed User in the enterprise.


        <https://developer.box.com/en/guides/applications/>


        <https://developer.box.com/en/guides/authentication/select/>

        :param user_id: The id of the user to authenticate
        :type user_id: str
        :param token_storage: Object responsible for storing token in newly created BoxJWTAuth. If no custom implementation provided, the token will be stored in memory., defaults to None
        :type token_storage: TokenStorage, optional
        """
        if token_storage is None:
            token_storage = InMemoryTokenStorage()
        new_config: JWTConfig = JWTConfig(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            enterprise_id=None,
            user_id=user_id,
            jwt_key_id=self.config.jwt_key_id,
            private_key=self.config.private_key,
            private_key_passphrase=self.config.private_key_passphrase,
            token_storage=token_storage,
        )
        new_auth: 'BoxJWTAuth' = BoxJWTAuth(config=new_config)
        return new_auth

    def with_enterprise_subject(
        self, enterprise_id: str, *, token_storage: TokenStorage = None
    ) -> 'BoxJWTAuth':
        """
        Create a new BoxJWTAuth instance that uses the provided enterprise ID as the subject of the JWT assertion.
        :param enterprise_id: The id of the enterprise to authenticate
        :type enterprise_id: str
        :param token_storage: Object responsible for storing token in newly created BoxJWTAuth. If no custom implementation provided, the token will be stored in memory., defaults to None
        :type token_storage: TokenStorage, optional
        """
        if token_storage is None:
            token_storage = InMemoryTokenStorage()
        new_config: JWTConfig = JWTConfig(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            enterprise_id=enterprise_id,
            user_id=None,
            jwt_key_id=self.config.jwt_key_id,
            private_key=self.config.private_key,
            private_key_passphrase=self.config.private_key_passphrase,
            token_storage=token_storage,
        )
        new_auth: 'BoxJWTAuth' = BoxJWTAuth(config=new_config)
        return new_auth

    def downscope_token(
        self,
        scopes: List[str],
        *,
        resource: Optional[str] = None,
        shared_link: Optional[str] = None,
        network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        """
        Downscope access token to the provided scopes. Returning a new access token with the provided scopes, with the original access token unchanged.
        :param scopes: The scope(s) to apply to the resulting token.
        :type scopes: List[str]
        :param resource: The file or folder to get a downscoped token for. If None and shared_link None, the resulting token will not be scoped down to just a single item. The resource should be a full URL to an item, e.g. https://api.box.com/2.0/files/123456., defaults to None
        :type resource: Optional[str], optional
        :param shared_link: The shared link to get a downscoped token for. If None and item None, the resulting token will not be scoped down to just a single item., defaults to None
        :type shared_link: Optional[str], optional
        :param network_session: An object to keep network session state, defaults to None
        :type network_session: Optional[NetworkSession], optional
        """
        token: Optional[AccessToken] = self.retrieve_token(
            network_session=network_session
        )
        if token == None:
            raise BoxSDKError(
                message='No access token is available. Make an API call to retrieve a token before calling this method.'
            )
        auth_manager: AuthorizationManager = AuthorizationManager(
            network_session=(
                network_session if not network_session == None else NetworkSession()
            )
        )
        downscoped_token: AccessToken = auth_manager.request_access_token(
            PostOAuth2TokenGrantTypeField.URN_IETF_PARAMS_OAUTH_GRANT_TYPE_TOKEN_EXCHANGE,
            subject_token=token.access_token,
            subject_token_type=PostOAuth2TokenSubjectTokenTypeField.URN_IETF_PARAMS_OAUTH_TOKEN_TYPE_ACCESS_TOKEN,
            resource=resource,
            scope=' '.join(scopes),
            box_shared_link=shared_link,
        )
        return downscoped_token

    def revoke_token(self, *, network_session: Optional[NetworkSession] = None) -> None:
        """
        Revoke the current access token and remove it from token storage.
        :param network_session: An object to keep network session state, defaults to None
        :type network_session: Optional[NetworkSession], optional
        """
        old_token: Optional[AccessToken] = self.token_storage.get()
        if old_token == None:
            return None
        auth_manager: AuthorizationManager = AuthorizationManager(
            network_session=(
                network_session if not network_session == None else NetworkSession()
            )
        )
        auth_manager.revoke_access_token(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            token=old_token.access_token,
        )
        self.token_storage.clear()
        return None
