from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError


class MetadataQueryIndexStatusField(str, Enum):
    BUILDING = 'building'
    ACTIVE = 'active'
    DISABLED = 'disabled'


class MetadataQueryIndexFieldsSortDirectionField(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class MetadataQueryIndexFieldsField(BaseObject):
    def __init__(
        self,
        *,
        key: Optional[str] = None,
        sort_direction: Optional[MetadataQueryIndexFieldsSortDirectionField] = None,
        **kwargs
    ):
        """
        :param key: The metadata template field key., defaults to None
        :type key: Optional[str], optional
        :param sort_direction: The sort direction of the field., defaults to None
        :type sort_direction: Optional[MetadataQueryIndexFieldsSortDirectionField], optional
        """
        super().__init__(**kwargs)
        self.key = key
        self.sort_direction = sort_direction


class MetadataQueryIndex(BaseObject):
    def __init__(
        self,
        type: str,
        status: MetadataQueryIndexStatusField,
        *,
        id: Optional[str] = None,
        fields: Optional[List[MetadataQueryIndexFieldsField]] = None,
        **kwargs
    ):
        """
        :param type: Value is always `metadata_query_index`.
        :type type: str
        :param status: The status of the metadata query index.
        :type status: MetadataQueryIndexStatusField
        :param id: The ID of the metadata query index., defaults to None
        :type id: Optional[str], optional
        :param fields: A list of template fields which make up the index., defaults to None
        :type fields: Optional[List[MetadataQueryIndexFieldsField]], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.status = status
        self.id = id
        self.fields = fields
