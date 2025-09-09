from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.group_base import GroupBaseTypeField

from box_sdk_gen.schemas.group_base import GroupBase

from box_sdk_gen.box.errors import BoxSDKError


class GroupMiniGroupTypeField(str, Enum):
    MANAGED_GROUP = 'managed_group'
    ALL_USERS_GROUP = 'all_users_group'


class GroupMini(GroupBase):
    def __init__(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        group_type: Optional[GroupMiniGroupTypeField] = None,
        type: GroupBaseTypeField = GroupBaseTypeField.GROUP,
        **kwargs
    ):
        """
        :param id: The unique identifier for this object.
        :type id: str
        :param name: The name of the group., defaults to None
        :type name: Optional[str], optional
        :param group_type: The type of the group., defaults to None
        :type group_type: Optional[GroupMiniGroupTypeField], optional
        :param type: The value will always be `group`., defaults to GroupBaseTypeField.GROUP
        :type type: GroupBaseTypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.name = name
        self.group_type = group_type
