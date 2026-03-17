from enum import Enum

from typing import List

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.hub_paragraph_text_block_v2025_r0 import (
    HubParagraphTextBlockV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_section_title_text_block_v2025_r0 import (
    HubSectionTitleTextBlockV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_callout_box_text_block_v2025_r0 import (
    HubCalloutBoxTextBlockV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_item_list_block_v2025_r0 import (
    HubItemListBlockV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_divider_block_v2025_r0 import (
    HubDividerBlockV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_document_block_entry_v2025_r0 import (
    HubDocumentBlockEntryV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class HubDocumentBlocksV2025R0TypeField(str, Enum):
    DOCUMENT_BLOCKS = 'document_blocks'


class HubDocumentBlocksV2025R0(BaseObject):
    _discriminator = 'type', {'document_blocks'}

    def __init__(
        self,
        entries: List[HubDocumentBlockEntryV2025R0],
        *,
        type: HubDocumentBlocksV2025R0TypeField = HubDocumentBlocksV2025R0TypeField.DOCUMENT_BLOCKS,
        limit: Optional[int] = None,
        next_marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param entries: Ordered list of blocks.
                :type entries: List[HubDocumentBlockEntryV2025R0]
                :param type: The value will always be `document_blocks`., defaults to HubDocumentBlocksV2025R0TypeField.DOCUMENT_BLOCKS
                :type type: HubDocumentBlocksV2025R0TypeField, optional
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed. The maximum value varies by API., defaults to None
                :type limit: Optional[int], optional
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.type = type
        self.limit = limit
        self.next_marker = next_marker
