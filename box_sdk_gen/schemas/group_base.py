from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class GroupBaseTypeField(str, Enum):
    GROUP = 'group'


class GroupBase(BaseObject):
    _discriminator = 'type', {'group'}

    def __init__(
        self, id: str, *, type: GroupBaseTypeField = GroupBaseTypeField.GROUP, **kwargs
    ):
        """
        :param id: The unique identifier for this object.
        :type id: str
        :param type: The value will always be `group`., defaults to GroupBaseTypeField.GROUP
        :type type: GroupBaseTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
