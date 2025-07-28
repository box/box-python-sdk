from typing import Dict

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.internal.utils import sanitize_map

from box_sdk_gen.serialization.json import sanitize_serialized_data


class DataSanitizer:
    def __init__(self):
        self._keys_to_sanitize = {
            'authorization': '',
            'access_token': '',
            'refresh_token': '',
            'subject_token': '',
            'token': '',
            'client_id': '',
            'client_secret': '',
            'shared_link': '',
            'download_url': '',
            'jwt_private_key': '',
            'jwt_private_key_passphrase': '',
            'password': '',
        }

    def sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        return sanitize_map(headers, self._keys_to_sanitize)

    def sanitize_body(self, body: SerializedData) -> SerializedData:
        return sanitize_serialized_data(body, self._keys_to_sanitize)
