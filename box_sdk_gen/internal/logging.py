from typing import Dict

from typing import Optional

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.internal.utils import sanitize_map

from box_sdk_gen.serialization.json import sanitize_serialized_data

from box_sdk_gen.serialization.json import sanitize_form_encoded_body_from_string

from box_sdk_gen.serialization.json import json_to_serialized_data

from box_sdk_gen.serialization.json import sd_to_json


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

    def sanitize_form_encoded_body(self, body: str) -> str:
        return sanitize_form_encoded_body_from_string(body, self._keys_to_sanitize)

    def sanitize_string_body(
        self, body: str, *, content_type: Optional[str] = None
    ) -> str:
        if (
            content_type == 'application/json'
            or content_type == 'application/json-patch+json'
        ):
            try:
                return sd_to_json(self.sanitize_body(json_to_serialized_data(body)))
            except Exception:
                return body
        if content_type == 'application/x-www-form-urlencoded':
            return self.sanitize_form_encoded_body(body)
        return body
