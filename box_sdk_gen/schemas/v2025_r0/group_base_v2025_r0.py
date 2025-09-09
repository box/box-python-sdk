from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class GroupBaseV2025R0TypeField(str, Enum):
    GROUP = 'group'


class GroupBaseV2025R0(BaseObject):
    _discriminator = 'type', {'group'}

    def __init__(
        self,
        id: str,
        *,
        type: GroupBaseV2025R0TypeField = GroupBaseV2025R0TypeField.GROUP,
        **kwargs
    ):
        """
        :param id: The unique identifier for this object.
        :type id: str
        :param type: The value will always be `group`., defaults to GroupBaseV2025R0TypeField.GROUP
        :type type: GroupBaseV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
