from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.v2025_r0.hub_document_block_v2025_r0 import (
    HubDocumentBlockV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class HubSectionTitleTextBlockV2025R0TypeField(str, Enum):
    SECTION_TITLE = 'section_title'


class HubSectionTitleTextBlockV2025R0(HubDocumentBlockV2025R0):
    def __init__(
        self,
        fragment: str,
        id: str,
        *,
        type: HubSectionTitleTextBlockV2025R0TypeField = HubSectionTitleTextBlockV2025R0TypeField.SECTION_TITLE,
        parent_id: Optional[str] = None,
        **kwargs
    ):
        """
        :param fragment: Text content of the block. Includes rich text formatting.
        :type fragment: str
        :param id: The unique identifier for this block.
        :type id: str
        :param type: The type of this block. The value is always `section_title`., defaults to HubSectionTitleTextBlockV2025R0TypeField.SECTION_TITLE
        :type type: HubSectionTitleTextBlockV2025R0TypeField, optional
        :param parent_id: The unique identifier of the parent block. Null for direct children of the page., defaults to None
        :type parent_id: Optional[str], optional
        """
        super().__init__(id=id, parent_id=parent_id, **kwargs)
        self.fragment = fragment
        self.type = type
