import configparser
import os
from pathlib import Path

from boxsdk.auth.jwt_auth import JWTAuth
from boxsdk.client import Client


def read_jwt_path_from_config(config_path: str):
    config_parser = configparser.ConfigParser()
    config_parser.read(config_path)
    return config_parser["JWT"].get('SettingsFilePath')


current_dir_path = str(Path(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))))
jwt_config_path = read_jwt_path_from_config(config_path=f'{current_dir_path}/integration_tests.cfg')
jwt_config = JWTAuth.from_settings_file(jwt_config_path)
CLIENT = Client(jwt_config)
