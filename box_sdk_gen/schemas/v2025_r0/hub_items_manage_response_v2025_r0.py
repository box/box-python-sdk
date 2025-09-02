from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.hub_item_operation_result_v2025_r0 import (
    HubItemOperationResultV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class HubItemsManageResponseV2025R0(BaseObject):
    def __init__(self, operations: List[HubItemOperationResultV2025R0], **kwargs):
        """
        :param operations: List of operations performed on Box Hub items.
        :type operations: List[HubItemOperationResultV2025R0]
        """
        super().__init__(**kwargs)
        self.operations = operations
