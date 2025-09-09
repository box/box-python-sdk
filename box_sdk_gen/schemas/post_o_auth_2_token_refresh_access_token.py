from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class PostOAuth2TokenRefreshAccessTokenGrantTypeField(str, Enum):
    REFRESH_TOKEN = 'refresh_token'


class PostOAuth2TokenRefreshAccessToken(BaseObject):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        *,
        grant_type: PostOAuth2TokenRefreshAccessTokenGrantTypeField = PostOAuth2TokenRefreshAccessTokenGrantTypeField.REFRESH_TOKEN,
        **kwargs
    ):
        """
        :param client_id: The client ID of the application requesting to refresh the token.
        :type client_id: str
        :param client_secret: The client secret of the application requesting to refresh the token.
        :type client_secret: str
        :param refresh_token: The refresh token to refresh.
        :type refresh_token: str
        :param grant_type: The type of request being made, in this case a refresh request., defaults to PostOAuth2TokenRefreshAccessTokenGrantTypeField.REFRESH_TOKEN
        :type grant_type: PostOAuth2TokenRefreshAccessTokenGrantTypeField, optional
        """
        super().__init__(**kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.grant_type = grant_type
