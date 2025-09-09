from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class UserBaseV2025R0TypeField(str, Enum):
    USER = 'user'


class UserBaseV2025R0(BaseObject):
    _discriminator = 'type', {'user'}

    def __init__(
        self,
        id: str,
        *,
        type: UserBaseV2025R0TypeField = UserBaseV2025R0TypeField.USER,
        **kwargs
    ):
        """
        :param id: The unique identifier for this user.
        :type id: str
        :param type: The value will always be `user`., defaults to UserBaseV2025R0TypeField.USER
        :type type: UserBaseV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
