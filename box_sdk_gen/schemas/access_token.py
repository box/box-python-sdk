from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_or_folder_scope import FileOrFolderScope

from box_sdk_gen.box.errors import BoxSDKError


class AccessTokenTokenTypeField(str, Enum):
    BEARER = 'bearer'


class AccessTokenIssuedTokenTypeField(str, Enum):
    URN_IETF_PARAMS_OAUTH_TOKEN_TYPE_ACCESS_TOKEN = (
        'urn:ietf:params:oauth:token-type:access_token'
    )


class AccessToken(BaseObject):
    def __init__(
        self,
        *,
        access_token: Optional[str] = None,
        expires_in: Optional[int] = None,
        token_type: Optional[AccessTokenTokenTypeField] = None,
        restricted_to: Optional[List[FileOrFolderScope]] = None,
        refresh_token: Optional[str] = None,
        issued_token_type: Optional[AccessTokenIssuedTokenTypeField] = None,
        **kwargs
    ):
        """
                :param access_token: The requested access token., defaults to None
                :type access_token: Optional[str], optional
                :param expires_in: The time in seconds by which this token will expire., defaults to None
                :type expires_in: Optional[int], optional
                :param token_type: The type of access token returned., defaults to None
                :type token_type: Optional[AccessTokenTokenTypeField], optional
                :param restricted_to: The permissions that this access token permits,
        providing a list of resources (files, folders, etc)
        and the scopes permitted for each of those resources., defaults to None
                :type restricted_to: Optional[List[FileOrFolderScope]], optional
                :param refresh_token: The refresh token for this access token, which can be used
        to request a new access token when the current one expires., defaults to None
                :type refresh_token: Optional[str], optional
                :param issued_token_type: The type of downscoped access token returned. This is only
        returned if an access token has been downscoped., defaults to None
                :type issued_token_type: Optional[AccessTokenIssuedTokenTypeField], optional
        """
        super().__init__(**kwargs)
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.restricted_to = restricted_to
        self.refresh_token = refresh_token
        self.issued_token_type = issued_token_type
