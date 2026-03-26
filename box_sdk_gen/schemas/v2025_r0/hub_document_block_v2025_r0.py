from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class HubDocumentBlockV2025R0(BaseObject):
    def __init__(self, id: str, *, parent_id: Optional[str] = None, **kwargs):
        """
        :param id: The unique identifier for this block.
        :type id: str
        :param parent_id: The unique identifier of the parent block. Null for direct children of the page., defaults to None
        :type parent_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.parent_id = parent_id
