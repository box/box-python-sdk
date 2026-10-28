from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleSystemUpdateRequestV2026R0(BaseObject):
    def __init__(self, *, name: Optional[str] = None, **kwargs):
        """
        :param name: The updated display name for the shuttle system., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.name = name
