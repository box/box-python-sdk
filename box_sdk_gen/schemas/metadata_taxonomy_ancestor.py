from typing import Optional

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class MetadataTaxonomyAncestor(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'display_name': 'displayName',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'displayName': 'display_name',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        display_name: Optional[str] = None,
        level: Optional[int] = None,
        **kwargs
    ):
        """
        :param id: A unique identifier of the metadata taxonomy node., defaults to None
        :type id: Optional[str], optional
        :param display_name: The display name of the metadata taxonomy node., defaults to None
        :type display_name: Optional[str], optional
        :param level: An index of the level to which the node belongs., defaults to None
        :type level: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.display_name = display_name
        self.level = level
