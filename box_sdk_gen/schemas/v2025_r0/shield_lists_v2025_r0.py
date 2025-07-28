from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.shield_list_mini_v2025_r0 import ShieldListMiniV2025R0

from box_sdk_gen.box.errors import BoxSDKError


class ShieldListsV2025R0(BaseObject):
    def __init__(
        self, *, entries: Optional[List[ShieldListMiniV2025R0]] = None, **kwargs
    ):
        """
        :param entries: A list of shield list objects., defaults to None
        :type entries: Optional[List[ShieldListMiniV2025R0]], optional
        """
        super().__init__(**kwargs)
        self.entries = entries
