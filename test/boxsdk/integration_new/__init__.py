import base64
import configparser
import os
import json
from pathlib import Path
from typing import Optional

from boxsdk.auth.jwt_auth import JWTAuth
from boxsdk.client import Client

JWT_CONFIG_ENV_VAR_NAME = 'JWT_CONFIG_BASE_64'
ADMIN_USER_ID_ENV_VAR_NAME = 'ADMIN_USER_ID'
CURRENT_DIR_PATH = str(
    Path(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))
)
CONFIG_PATH = f'{CURRENT_DIR_PATH}/integration_tests.cfg'
CONFIG_PARSER = configparser.ConfigParser()
CONFIG_PARSER.read(CONFIG_PATH)


def get_jwt_config() -> JWTAuth:
    jwt_config = read_jwt_config_from_env_var() or read_jwt_config_from_file()

    if not jwt_config:
        raise RuntimeError(
            f'JWT config cannot be loaded. Missing environment variable: {JWT_CONFIG_ENV_VAR_NAME} or JWT config path.'
        )
    return jwt_config


def get_admin_user_id() -> str:
    admin_user_id = os.getenv(ADMIN_USER_ID_ENV_VAR_NAME) or CONFIG_PARSER["JWT"].get(
        'AdminUserID'
    )

    if not admin_user_id:
        raise RuntimeError(
            f'Unknown admin user id. Missing environment variable: {ADMIN_USER_ID_ENV_VAR_NAME} or value in {CONFIG_PATH}.'
        )

    return admin_user_id


def read_jwt_config_from_env_var() -> Optional[JWTAuth]:
    for key, value in os.environ.items():
        print(f"{key}={value}")
    jwt_config_base64 = os.getenv(JWT_CONFIG_ENV_VAR_NAME)
    if not jwt_config_base64:
        return None
    jwt_config_str = base64.b64decode(jwt_config_base64)
    jwt_config_json = json.loads(jwt_config_str)
    return JWTAuth.from_settings_dictionary(jwt_config_json)


def read_jwt_config_from_file() -> Optional[JWTAuth]:
    jwt_config_file_path = CONFIG_PARSER["JWT"].get('ConfigFilePath')
    if not jwt_config_file_path:
        return None
    return JWTAuth.from_settings_file(jwt_config_file_path)


def create_client(jwt_config: JWTAuth):
    return Client(jwt_config)


def create_user_client(jwt_config: JWTAuth):
    admin_user_id = get_admin_user_id()
    jwt_config.authenticate_user(admin_user_id)
    return Client(jwt_config)


config = get_jwt_config()
CLIENT = create_client(config)
USER_CLIENT = create_user_client(config)
