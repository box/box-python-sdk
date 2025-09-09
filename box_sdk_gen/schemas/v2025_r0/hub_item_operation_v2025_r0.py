from enum import Enum

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


class HubItemOperationV2025R0ActionField(str, Enum):
    ADD = 'add'
    REMOVE = 'remove'


class HubItemOperationV2025R0(BaseObject):
    def __init__(
        self,
        action: HubItemOperationV2025R0ActionField,
        item: HubItemReferenceV2025R0,
        **kwargs
    ):
        """
        :param action: The action to perform on a Box Hub item.
        :type action: HubItemOperationV2025R0ActionField
        """
        super().__init__(**kwargs)
        self.action = action
        self.item = item
