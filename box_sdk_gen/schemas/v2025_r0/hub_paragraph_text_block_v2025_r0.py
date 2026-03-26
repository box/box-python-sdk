from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.v2025_r0.hub_document_block_v2025_r0 import (
    HubDocumentBlockV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class HubParagraphTextBlockV2025R0TypeField(str, Enum):
    PARAGRAPH = 'paragraph'


class HubParagraphTextBlockV2025R0(HubDocumentBlockV2025R0):
    _discriminator = 'type', {'paragraph'}

    def __init__(
        self,
        fragment: str,
        id: str,
        *,
        type: HubParagraphTextBlockV2025R0TypeField = HubParagraphTextBlockV2025R0TypeField.PARAGRAPH,
        parent_id: Optional[str] = None,
        **kwargs
    ):
        """
        :param fragment: Text content of the block. Includes rich text formatting.
        :type fragment: str
        :param id: The unique identifier for this block.
        :type id: str
        :param type: The type of this block. The value is always `paragraph`., defaults to HubParagraphTextBlockV2025R0TypeField.PARAGRAPH
        :type type: HubParagraphTextBlockV2025R0TypeField, optional
        :param parent_id: The unique identifier of the parent block. Null for direct children of the page., defaults to None
        :type parent_id: Optional[str], optional
        """
        super().__init__(id=id, parent_id=parent_id, **kwargs)
        self.fragment = fragment
        self.type = type
