from datetime import datetime, date
from enum import EnumMeta, Enum
from typing import get_args, get_origin, Union, Optional
from .null_value import NullValue


class BaseObject:
    _discriminator = (None, {})
    _json_to_fields_mapping = {}
    _fields_to_json_mapping = {}

    def __init__(self, **kwargs):
        self._raw_data: dict = {}
        self.__dict__.update(kwargs)

    @classmethod
    def from_dict(cls, data: dict):
        unpacked_attributes = {}
        for key, value in data.items():
            mapping_field_name = cls._json_to_fields_mapping.get(key, key)
            annotation = cls.__init__.__annotations__.get(mapping_field_name, None)
            unpacked_attributes[mapping_field_name] = cls._deserialize(
                key, value, annotation
            )
        return cls(**unpacked_attributes)

    @property
    def raw_data(self):
        """
        Returns the raw json representation returned by the API
        :return: dict with the raw json data
        """
        return self._raw_data

    def to_dict(self) -> dict:
        result_dict = {}
        for k, v in vars(self).items():
            # Skip private and protected attributes
            if k.startswith("_"):
                continue
            if v is None:
                continue
            if isinstance(v, NullValue):
                value = None
            elif type(v) is list:
                value = [
                    item.to_dict() if isinstance(item, BaseObject) else item
                    for item in v
                ]
            elif type(v) is dict:
                value = {
                    key: value.to_dict() if isinstance(value, BaseObject) else value
                    for key, value in v.items()
                }
            elif isinstance(v, BaseObject):
                value = v.to_dict()
            elif isinstance(v, Enum):
                value = v.value
            elif isinstance(v, date):
                value = v.isoformat()
            elif isinstance(v, datetime):
                value = v.isoformat().replace('+00:00', 'Z')
            else:
                value = v
            result_dict[self._fields_to_json_mapping.get(k, k)] = value

        return result_dict

    @classmethod
    def _deserialize(cls, key, value, annotation=None):
        if annotation is None or value is None:
            return value
        if get_origin(annotation) == Optional:
            return cls._deserialize(key, value, get_args(annotation))
        if get_origin(annotation) == Union:
            union_without_none_type = [
                arg for arg in get_args(annotation) if arg is not type(None)
            ]
            if len(union_without_none_type) == 1:
                return cls._deserialize(key, value, union_without_none_type[0])

        if get_origin(annotation) == list:
            return cls._deserialize_list(key, value, annotation)
        elif get_origin(annotation) == Union:
            return cls._deserialize_union(key, value, annotation)
        elif isinstance(annotation, EnumMeta):
            return cls._deserialize_enum(key, value, annotation)
        elif annotation == datetime:
            return cls._deserialize_datetime(key, value, annotation)
        elif annotation == date:
            return cls._deserialize_date(key, value, annotation)
        elif isinstance(annotation, type) and issubclass(annotation, BaseObject):
            return cls._deserialize_nested_type(key, value, annotation)
        else:
            return value

    @classmethod
    def _deserialize_list(cls, key, value, annotation: list):
        try:
            list_type = get_args(annotation)[0]
            return [
                cls._deserialize(key, list_entry, list_type) for list_entry in value
            ]
        except Exception:
            return value

    @classmethod
    def _deserialize_union(cls, key, value, annotation):
        try:
            possible_types = get_args(annotation)
            if value is None:
                if type(None) not in possible_types:
                    print(
                        'Value: ', value, 'should not be allowed in Union:', annotation
                    )
                return value

            for possible_type in possible_types:
                if (
                    isinstance(possible_type, type)
                    and issubclass(possible_type, BaseObject)
                    and value.get(possible_type._discriminator[0], None)
                    in possible_type._discriminator[1]
                ):
                    return cls._deserialize(key, value, possible_type)

            for possible_type in possible_types:
                try:
                    return cls._deserialize(key, value, possible_type)
                except Exception:
                    continue
            return value
        except Exception:
            return value

    @classmethod
    def _deserialize_enum(cls, key, value, annotation):
        try:
            return getattr(annotation, value.upper().replace(' ', '_'))
        except Exception:
            return value

    @classmethod
    def _deserialize_datetime(cls, key, value, annotation):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except Exception:
            return value

    @classmethod
    def _deserialize_date(cls, key, value, annotation):
        try:
            return date.fromisoformat(value)
        except Exception:
            return value

    @classmethod
    def _deserialize_nested_type(cls, key, value, annotation):
        try:
            return annotation.from_dict(value)
        except Exception:
            return value

    def __repr__(self) -> str:
        return f'{self.__class__} {self.to_dict()}'
