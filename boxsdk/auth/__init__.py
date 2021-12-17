# coding: utf-8

from .cooperatively_managed_oauth2 import CooperativelyManagedOAuth2
from .developer_token_auth import DeveloperTokenAuth
try:
    from .jwt_auth import JWTAuth
except ImportError:
    JWTAuth = None  # If extras[jwt] are not installed, JWTAuth won't be available.
from .oauth2 import OAuth2
try:
    from .redis_managed_oauth2 import RedisManagedOAuth2
except ImportError:
    RedisManagedOAuth2 = None  # If extras[redis] are not installed, RedisManagedOAuth2 won't be available.
try:
    from .redis_managed_jwt_auth import RedisManagedJWTAuth
except ImportError:
    RedisManagedJWTAuth = None  # If extras[jwt,redis] are not installed, RedisManagedJWTAuth won't be available.
from .remote_managed_oauth2 import RemoteOAuth2
