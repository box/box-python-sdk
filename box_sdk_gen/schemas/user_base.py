from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class UserBaseTypeField(str, Enum):
    USER = 'user'


class UserBase(BaseObject):
    _discriminator = 'type', {'user'}

    def __init__(
        self, id: str, *, type: UserBaseTypeField = UserBaseTypeField.USER, **kwargs
    ):
        """
        :param id: The unique identifier for this user.
        :type id: str
        :param type: The value will always be `user`., defaults to UserBaseTypeField.USER
        :type type: UserBaseTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
