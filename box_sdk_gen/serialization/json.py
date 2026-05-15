import json
from typing import Dict, get_origin, Union, Type
from urllib.parse import urlencode

from ..internal.base_object import BaseObject

SerializedData = Dict


def json_to_serialized_data(data: str) -> SerializedData:
    return json.loads(data)


def sd_to_json(data: SerializedData) -> str:
    return json.dumps(data)


def sd_to_url_params(data: SerializedData) -> str:
    return urlencode(data)


def get_sd_value_by_key(data: SerializedData, key: str):
    return data.get(key)


def serialize(obj: Union[BaseObject, dict, list]) -> SerializedData:
    if isinstance(obj, dict):
        obj = BaseObject(**obj).to_dict()
    if isinstance(obj, BaseObject):
        obj = obj.to_dict()
    if isinstance(obj, list):
        obj = [
            element.to_dict() if isinstance(element, BaseObject) else element
            for element in obj
        ]
    return obj


def deserialize(value: SerializedData, type: Type[BaseObject]):
    if get_origin(type) == Union:
        type = BaseObject._deserialize_union('', value, type)
    obj = type.from_dict(value)
    obj._raw_data = value
    return obj


def sanitized_value() -> str:
    return '---[redacted]---'


def sanitize_form_encoded_body_from_string(
    body: str, keys_to_sanitize: Dict[str, str]
) -> str:
    return '&'.join(
        [
            _sanitize_form_encoded_parameter(parameter, keys_to_sanitize)
            for parameter in body.split('&')
        ]
    )


def _sanitize_form_encoded_parameter(
    parameter: str, keys_to_sanitize: Dict[str, str]
) -> str:
    separator_index = parameter.find('=')
    if separator_index < 0:
        return parameter

    key = parameter[:separator_index]
    value = parameter[separator_index + 1 :]
    sanitized_parameter_value = (
        sanitized_value() if key.lower() in keys_to_sanitize else value
    )
    return f'{key}={sanitized_parameter_value}'


def sanitize_serialized_data(
    sd: SerializedData, keys_to_sanitize: Dict[str, str]
) -> SerializedData:
    if not isinstance(sd, Dict):
        return sd
    sanitized_dictionary = {}
    for key, value in sd.items():
        if key.lower() in keys_to_sanitize and isinstance(value, str):
            sanitized_dictionary[key] = sanitized_value()
        elif isinstance(value, Dict):
            sanitized_dictionary[key] = sanitize_serialized_data(
                value, keys_to_sanitize
            )
        else:
            sanitized_dictionary[key] = value
    return sanitized_dictionary
