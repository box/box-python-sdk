from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShuttleTargetSubjectInputV2026R0TypeField(str, Enum):
    USER = 'user'
    GROUP = 'group'


class ShuttleTargetSubjectInputV2026R0(BaseObject):
    _discriminator = 'type', {'user', 'group'}

    def __init__(
        self, type: ShuttleTargetSubjectInputV2026R0TypeField, id: str, **kwargs
    ):
        """
        :param type: Whether the Box target is a user or a group.
        :type type: ShuttleTargetSubjectInputV2026R0TypeField
        :param id: The identifier of the target Box subject.
        :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
