from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathMappingAccountInputV2026R0(BaseObject):
    def __init__(
        self, *, id: Optional[str] = None, email: Optional[str] = None, **kwargs
    ):
        """
        :param id: The platform-native identifier of the account., defaults to None
        :type id: Optional[str], optional
        :param email: The email address of the account., defaults to None
        :type email: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.email = email
