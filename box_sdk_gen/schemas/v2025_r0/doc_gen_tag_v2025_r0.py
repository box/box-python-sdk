from enum import Enum

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class DocGenTagV2025R0TagTypeField(str, Enum):
    TEXT = 'text'
    ARITHMETIC = 'arithmetic'
    CONDITIONAL = 'conditional'
    FOR_LOOP = 'for-loop'
    TABLE_LOOP = 'table-loop'
    IMAGE = 'image'


class DocGenTagV2025R0(BaseObject):
    def __init__(
        self,
        tag_content: str,
        tag_type: DocGenTagV2025R0TagTypeField,
        json_paths: List[str],
        **kwargs
    ):
        """
        :param tag_content: The content of the tag.
        :type tag_content: str
        :param tag_type: Type of the tag.
        :type tag_type: DocGenTagV2025R0TagTypeField
        :param json_paths: List of the paths.
        :type json_paths: List[str]
        """
        super().__init__(**kwargs)
        self.tag_content = tag_content
        self.tag_type = tag_type
        self.json_paths = json_paths
