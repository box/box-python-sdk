from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.schemas.v2025_r0.hub_document_block_v2025_r0 import (
    HubDocumentBlockV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class HubItemListBlockV2025R0TypeField(str, Enum):
    ITEM_LIST = 'item_list'


class HubItemListBlockV2025R0(HubDocumentBlockV2025R0):
    def __init__(
        self,
        id: str,
        *,
        type: HubItemListBlockV2025R0TypeField = HubItemListBlockV2025R0TypeField.ITEM_LIST,
        parent_id: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this block.
        :type id: str
        :param type: The type of this block. The value is always `item_list`., defaults to HubItemListBlockV2025R0TypeField.ITEM_LIST
        :type type: HubItemListBlockV2025R0TypeField, optional
        :param parent_id: The unique identifier of the parent block. Null for direct children of the page., defaults to None
        :type parent_id: Optional[str], optional
        """
        super().__init__(id=id, parent_id=parent_id, **kwargs)
        self.type = type
