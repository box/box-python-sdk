from typing import Optional

from typing import List

from box_sdk_gen.schemas.post_o_auth_2_token import PostOAuth2TokenGrantTypeField

from box_sdk_gen.schemas.post_o_auth_2_token import PostOAuth2TokenSubjectTokenTypeField

from box_sdk_gen.schemas.access_token import AccessToken

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.box.token_storage import TokenStorage

from box_sdk_gen.box.token_storage import InMemoryTokenStorage

from box_sdk_gen.managers.authorization import AuthorizationManager

from box_sdk_gen.schemas.post_o_auth_2_token import PostOAuth2Token

from box_sdk_gen.schemas.post_o_auth_2_revoke import PostOAuth2Revoke


class DeveloperTokenConfig:
    def __init__(
        self, *, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret


class BoxDeveloperTokenAuth(Authentication):
    def __init__(self, token: str, *, config: DeveloperTokenConfig = None, **kwargs):
        """
        :param config: Configuration object of DeveloperTokenAuth., defaults to None
        :type config: DeveloperTokenConfig, optional
        """
        super().__init__(**kwargs)
        self.token = token
        self.config = config
        self.token_storage = InMemoryTokenStorage(
            token=AccessToken(access_token=self.token)
        )

    def retrieve_token(
        self, *, network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        """
        Retrieves stored developer token
        :param network_session: An object to keep network session state, defaults to None
        :type network_session: Optional[NetworkSession], optional
        """
        token: Optional[AccessToken] = self.token_storage.get()
        if token == None:
            raise BoxSDKError(message='No access token is available.')
        return token

    def refresh_token(
        self, *, network_session: Optional[NetworkSession] = None
    ) -> AccessToken:
        """
        Developer token cannot be refreshed
        :param network_session: An object to keep network session state, defaults to None
        :type network_session: Optional[NetworkSession], optional
        """
        raise BoxSDKError(
            message='Developer token has expired. Please provide a new one.'
        )

    def retrieve_authorization_header(
        self, *, network_session: Optional[NetworkSession] = None
    ) -> str:
        token: AccessToken = self.retrieve_token(network_session=network_session)
        return ''.join(['Bearer ', token.access_token])

    def revoke_token(self, *, network_session: Optional[NetworkSession] = None) -> None:
        """
        Revoke an active Access Token, effectively logging a user out that has been previously authenticated.
        :param network_session: An object to keep network session state, defaults to None
        :type network_session: Optional[NetworkSession], optional
        """
        token: Optional[AccessToken] = self.token_storage.get()
        if token == None:
            return None
        auth_manager: AuthorizationManager = AuthorizationManager(
            network_session=(
                network_session if not network_session == None else NetworkSession()
            )
        )
        auth_manager.revoke_access_token(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            token=token.access_token,
        )
        self.token_storage.clear()
        return None

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
        if token == None or token.access_token == None:
            raise BoxSDKError(message='No access token is available.')
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
