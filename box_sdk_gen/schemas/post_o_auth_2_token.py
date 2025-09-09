from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class PostOAuth2TokenGrantTypeField(str, Enum):
    AUTHORIZATION_CODE = 'authorization_code'
    REFRESH_TOKEN = 'refresh_token'
    CLIENT_CREDENTIALS = 'client_credentials'
    URN_IETF_PARAMS_OAUTH_GRANT_TYPE_JWT_BEARER = (
        'urn:ietf:params:oauth:grant-type:jwt-bearer'
    )
    URN_IETF_PARAMS_OAUTH_GRANT_TYPE_TOKEN_EXCHANGE = (
        'urn:ietf:params:oauth:grant-type:token-exchange'
    )


class PostOAuth2TokenSubjectTokenTypeField(str, Enum):
    URN_IETF_PARAMS_OAUTH_TOKEN_TYPE_ACCESS_TOKEN = (
        'urn:ietf:params:oauth:token-type:access_token'
    )


class PostOAuth2TokenActorTokenTypeField(str, Enum):
    URN_IETF_PARAMS_OAUTH_TOKEN_TYPE_ID_TOKEN = (
        'urn:ietf:params:oauth:token-type:id_token'
    )


class PostOAuth2TokenBoxSubjectTypeField(str, Enum):
    ENTERPRISE = 'enterprise'
    USER = 'user'


class PostOAuth2Token(BaseObject):
    def __init__(
        self,
        grant_type: PostOAuth2TokenGrantTypeField,
        *,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        code: Optional[str] = None,
        refresh_token: Optional[str] = None,
        assertion: Optional[str] = None,
        subject_token: Optional[str] = None,
        subject_token_type: Optional[PostOAuth2TokenSubjectTokenTypeField] = None,
        actor_token: Optional[str] = None,
        actor_token_type: Optional[PostOAuth2TokenActorTokenTypeField] = None,
        scope: Optional[str] = None,
        resource: Optional[str] = None,
        box_subject_type: Optional[PostOAuth2TokenBoxSubjectTypeField] = None,
        box_subject_id: Optional[str] = None,
        box_shared_link: Optional[str] = None,
        **kwargs
    ):
        """
                :param grant_type: The type of request being made, either using a client-side obtained
        authorization code, a refresh token, a JWT assertion, client credentials
        grant or another access token for the purpose of downscoping a token.
                :type grant_type: PostOAuth2TokenGrantTypeField
                :param client_id: The Client ID of the application requesting an access token.

        Used in combination with `authorization_code`, `client_credentials`, or
        `urn:ietf:params:oauth:grant-type:jwt-bearer` as the `grant_type`., defaults to None
                :type client_id: Optional[str], optional
                :param client_secret: The client secret of the application requesting an access token.

        Used in combination with `authorization_code`, `client_credentials`, or
        `urn:ietf:params:oauth:grant-type:jwt-bearer` as the `grant_type`., defaults to None
                :type client_secret: Optional[str], optional
                :param code: The client-side authorization code passed to your application by
        Box in the browser redirect after the user has successfully
        granted your application permission to make API calls on their
        behalf.

        Used in combination with `authorization_code` as the `grant_type`., defaults to None
                :type code: Optional[str], optional
                :param refresh_token: A refresh token used to get a new access token with.

        Used in combination with `refresh_token` as the `grant_type`., defaults to None
                :type refresh_token: Optional[str], optional
                :param assertion: A JWT assertion for which to request a new access token.

        Used in combination with `urn:ietf:params:oauth:grant-type:jwt-bearer`
        as the `grant_type`., defaults to None
                :type assertion: Optional[str], optional
                :param subject_token: The token to exchange for a downscoped token. This can be a regular
        access token, a JWT assertion, or an app token.

        Used in combination with `urn:ietf:params:oauth:grant-type:token-exchange`
        as the `grant_type`., defaults to None
                :type subject_token: Optional[str], optional
                :param subject_token_type: The type of `subject_token` passed in.

        Used in combination with `urn:ietf:params:oauth:grant-type:token-exchange`
        as the `grant_type`., defaults to None
                :type subject_token_type: Optional[PostOAuth2TokenSubjectTokenTypeField], optional
                :param actor_token: The token used to create an annotator token.
        This is a JWT assertion.

        Used in combination with `urn:ietf:params:oauth:grant-type:token-exchange`
        as the `grant_type`., defaults to None
                :type actor_token: Optional[str], optional
                :param actor_token_type: The type of `actor_token` passed in.

        Used in combination with `urn:ietf:params:oauth:grant-type:token-exchange`
        as the `grant_type`., defaults to None
                :type actor_token_type: Optional[PostOAuth2TokenActorTokenTypeField], optional
                :param scope: The space-delimited list of scopes that you want apply to the
        new access token.

        The `subject_token` will need to have all of these scopes or
        the call will error with **401 Unauthorized**.., defaults to None
                :type scope: Optional[str], optional
                :param resource: Full URL for the file that the token should be generated for., defaults to None
                :type resource: Optional[str], optional
                :param box_subject_type: Used in combination with `client_credentials` as the `grant_type`., defaults to None
                :type box_subject_type: Optional[PostOAuth2TokenBoxSubjectTypeField], optional
                :param box_subject_id: Used in combination with `client_credentials` as the `grant_type`.
        Value is determined by `box_subject_type`. If `user` use user ID and if
        `enterprise` use enterprise ID., defaults to None
                :type box_subject_id: Optional[str], optional
                :param box_shared_link: Full URL of the shared link on the file or folder
        that the token should be generated for., defaults to None
                :type box_shared_link: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.refresh_token = refresh_token
        self.assertion = assertion
        self.subject_token = subject_token
        self.subject_token_type = subject_token_type
        self.actor_token = actor_token
        self.actor_token_type = actor_token_type
        self.scope = scope
        self.resource = resource
        self.box_subject_type = box_subject_type
        self.box_subject_id = box_subject_id
        self.box_shared_link = box_shared_link
