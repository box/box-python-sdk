import base64
import configparser
import os
import json
from pathlib import Path
from typing import Optional

from boxsdk.auth.jwt_auth import JWTAuth
from boxsdk.client import Client


JWT_CONFIG_ENV_VAR_NAME = 'JWT_CONFIG_BASE_64'
CURRENT_DIR_PATH = str(Path(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))))
CONFIG_PATH = f'{CURRENT_DIR_PATH}/integration_tests.cfg'


def get_jwt_config() -> JWTAuth:
    jwt_config = read_jwt_config_from_env_var() or read_jwt_config_from_file()

    if not jwt_config:
        raise RuntimeError(
            f'JWT config cannot be loaded. Missing environment variable: {JWT_CONFIG_ENV_VAR_NAME} or JWT config path.'
        )
    return jwt_config


def read_jwt_config_from_env_var() -> Optional[JWTAuth]:

    jwt_config_base64 = os.getenv(JWT_CONFIG_ENV_VAR_NAME)
    if not jwt_config_base64:
        return None
    jwt_config_str = base64.b64decode(jwt_config_base64)
    jwt_config_json = json.loads(jwt_config_str)
    return JWTAuth.from_settings_dictionary(jwt_config_json)


def read_jwt_config_from_file() -> Optional[JWTAuth]:
    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_PATH)
    jwt_config_file_path = config_parser["JWT"].get('ConfigFilePath')
    if not jwt_config_file_path:
        return None
    return JWTAuth.from_settings_file(jwt_config_file_path)


CLIENT = Client(get_jwt_config())
