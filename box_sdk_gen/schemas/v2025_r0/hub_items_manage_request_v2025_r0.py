from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.hub_item_operation_v2025_r0 import (
    HubItemOperationV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class HubItemsManageRequestV2025R0(BaseObject):
    def __init__(
        self, *, operations: Optional[List[HubItemOperationV2025R0]] = None, **kwargs
    ):
        """
        :param operations: List of operations to perform on Box Hub items., defaults to None
        :type operations: Optional[List[HubItemOperationV2025R0]], optional
        """
        super().__init__(**kwargs)
        self.operations = operations
