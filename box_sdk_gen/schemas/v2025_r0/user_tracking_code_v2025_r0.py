from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class UserTrackingCodeV2025R0(BaseObject):
    def __init__(
        self, *, id: Optional[int] = None, name: Optional[str] = None, **kwargs
    ):
        """
        :param id: The ID of the user tracking code., defaults to None
        :type id: Optional[int], optional
        :param name: The name of the user tracking code., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.name = name
