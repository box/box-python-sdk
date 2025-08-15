from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class UserReferenceV2025R0TypeField(str, Enum):
    USER = 'user'


class UserReferenceV2025R0(BaseObject):
    _discriminator = 'type', {'user'}

    def __init__(
        self,
        id: str,
        *,
        type: UserReferenceV2025R0TypeField = UserReferenceV2025R0TypeField.USER,
        **kwargs
    ):
        """
        :param id: The unique identifier for the user.
        :type id: str
        :param type: The value is always `user`., defaults to UserReferenceV2025R0TypeField.USER
        :type type: UserReferenceV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
