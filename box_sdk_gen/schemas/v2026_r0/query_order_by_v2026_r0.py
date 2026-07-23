from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class QueryOrderByV2026R0DirectionField(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class QueryOrderByV2026R0(BaseObject):
    def __init__(
        self, field_key: str, direction: QueryOrderByV2026R0DirectionField, **kwargs
    ):
        """
        :param field_key: The fully qualified field key to sort by.
        :type field_key: str
        :param direction: The direction in which results are ordered.
        :type direction: QueryOrderByV2026R0DirectionField
        """
        super().__init__(**kwargs)
        self.field_key = field_key
        self.direction = direction
