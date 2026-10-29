from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttlePathMappingAccountV2026R0(BaseObject):
    def __init__(
        self,
        *,
        id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The platform-native identifier of the account. `null` when the system
        does not provide one., defaults to None
                :type id: Optional[str], optional
                :param email: The email address of the account. `null` when unknown., defaults to None
                :type email: Optional[str], optional
                :param name: The display name of the account. `null` when unknown., defaults to None
                :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.email = email
        self.name = name
