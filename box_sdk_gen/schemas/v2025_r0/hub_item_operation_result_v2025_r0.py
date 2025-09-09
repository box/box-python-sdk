from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.file_reference_v2025_r0 import FileReferenceV2025R0

from box_sdk_gen.schemas.v2025_r0.folder_reference_v2025_r0 import (
    FolderReferenceV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.weblink_reference_v2025_r0 import (
    WeblinkReferenceV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_item_reference_v2025_r0 import (
    HubItemReferenceV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class HubItemOperationResultV2025R0(BaseObject):
    def __init__(
        self,
        *,
        action: Optional[str] = None,
        item: Optional[HubItemReferenceV2025R0] = None,
        status: Optional[int] = None,
        error: Optional[str] = None,
        **kwargs
    ):
        """
        :param action: The action performed on the item., defaults to None
        :type action: Optional[str], optional
        :param status: The HTTP status code of the operation., defaults to None
        :type status: Optional[int], optional
        :param error: Error message if the operation failed., defaults to None
        :type error: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.action = action
        self.item = item
        self.status = status
        self.error = error
