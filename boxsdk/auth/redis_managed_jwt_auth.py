# coding: utf-8
from typing import Tuple

from .jwt_auth import JWTAuth
from .redis_managed_oauth2 import RedisManagedOAuth2Mixin


class RedisManagedJWTAuth(RedisManagedOAuth2Mixin, JWTAuth):
    """
    JWT Auth subclass which uses Redis to manage access tokens.
    """
    def _auth_with_jwt(self, sub: str, sub_type: str) -> Tuple[str, None]:
        """
        Base class override. Returns the access token in a tuple to match the OAuth2 interface.
        """
        return super()._auth_with_jwt(sub, sub_type), None
