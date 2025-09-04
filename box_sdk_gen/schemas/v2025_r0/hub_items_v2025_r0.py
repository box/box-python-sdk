from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.hub_item_v2025_r0 import HubItemV2025R0

from box_sdk_gen.box.errors import BoxSDKError


class HubItemsV2025R0(BaseObject):
    def __init__(
        self,
        *,
        entries: Optional[List[HubItemV2025R0]] = None,
        limit: Optional[int] = None,
        next_marker: Optional[str] = None,
        **kwargs
    ):
        """
                :param entries: A list of Box Hub items., defaults to None
                :type entries: Optional[List[HubItemV2025R0]], optional
                :param limit: The limit that was used for these entries. This will be the same as the
        `limit` query parameter unless that value exceeded the maximum value
        allowed. The maximum value varies by API., defaults to None
                :type limit: Optional[int], optional
                :param next_marker: The marker for the start of the next page of results., defaults to None
                :type next_marker: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
        self.limit = limit
        self.next_marker = next_marker
