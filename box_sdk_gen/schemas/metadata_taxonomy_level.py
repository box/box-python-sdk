from typing import Optional

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class MetadataTaxonomyLevel(BaseObject):
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
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        level: Optional[int] = None,
        **kwargs
    ):
        """
        :param display_name: The display name of the level as it is shown to the user., defaults to None
        :type display_name: Optional[str], optional
        :param description: A description of the level., defaults to None
        :type description: Optional[str], optional
        :param level: An index of the level within the taxonomy. Levels are indexed starting from 1., defaults to None
        :type level: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.display_name = display_name
        self.description = description
        self.level = level
