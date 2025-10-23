from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class UserOrGroupReferenceV2025R0TypeField(str, Enum):
    USER = 'user'
    GROUP = 'group'


class UserOrGroupReferenceV2025R0(BaseObject):
    _discriminator = 'type', {'user', 'group'}

    def __init__(
        self,
        *,
        type: Optional[UserOrGroupReferenceV2025R0TypeField] = None,
        id: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The type `user` or `group`., defaults to None
        :type type: Optional[UserOrGroupReferenceV2025R0TypeField], optional
        :param id: The identifier of the user or group., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
