import base64
import os
import json

from boxsdk.auth.jwt_auth import JWTAuth
from boxsdk.client import Client


JWT_CONFIG_ENV_VAR_NAME = 'JWT_CONFIG_BASE64'


def read_jwt_path_from_env_var() -> dict:

    jwt_config_base64 = os.getenv(JWT_CONFIG_ENV_VAR_NAME)
    if not jwt_config_base64:
        raise RuntimeError("JWT config cannot be loaded. Missing required environment variable: JWT_CONFIG_BASE64.")
    jwt_config_str = base64.b64decode(jwt_config_base64)

    return json.loads(jwt_config_str)


jwt_config_json = read_jwt_path_from_env_var()
jwt_config = JWTAuth.from_settings_dictionary(jwt_config_json)
CLIENT = Client(jwt_config)
