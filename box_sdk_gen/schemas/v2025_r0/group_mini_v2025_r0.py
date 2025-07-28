from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.v2025_r0.group_base_v2025_r0 import GroupBaseV2025R0TypeField

from box_sdk_gen.schemas.v2025_r0.group_base_v2025_r0 import GroupBaseV2025R0

from box_sdk_gen.box.errors import BoxSDKError


class GroupMiniV2025R0GroupTypeField(str, Enum):
    MANAGED_GROUP = 'managed_group'
    ALL_USERS_GROUP = 'all_users_group'


class GroupMiniV2025R0(GroupBaseV2025R0):
    def __init__(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        group_type: Optional[GroupMiniV2025R0GroupTypeField] = None,
        type: GroupBaseV2025R0TypeField = GroupBaseV2025R0TypeField.GROUP,
        **kwargs
    ):
        """
        :param id: The unique identifier for this object.
        :type id: str
        :param name: The name of the group., defaults to None
        :type name: Optional[str], optional
        :param group_type: The type of the group., defaults to None
        :type group_type: Optional[GroupMiniV2025R0GroupTypeField], optional
        :param type: The value will always be `group`., defaults to GroupBaseV2025R0TypeField.GROUP
        :type type: GroupBaseV2025R0TypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.name = name
        self.group_type = group_type
