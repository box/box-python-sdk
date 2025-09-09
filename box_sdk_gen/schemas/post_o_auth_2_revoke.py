from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class PostOAuth2Revoke(BaseObject):
    def __init__(
        self,
        *,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[str] = None,
        **kwargs
    ):
        """
                :param client_id: The Client ID of the application requesting to revoke the
        access token., defaults to None
                :type client_id: Optional[str], optional
                :param client_secret: The client secret of the application requesting to revoke
        an access token., defaults to None
                :type client_secret: Optional[str], optional
                :param token: The access token to revoke., defaults to None
                :type token: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
