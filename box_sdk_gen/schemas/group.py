from typing import Optional

from box_sdk_gen.schemas.group_base import GroupBaseTypeField

from box_sdk_gen.schemas.group_base import GroupBase

from box_sdk_gen.schemas.group_mini import GroupMiniGroupTypeField

from box_sdk_gen.schemas.group_mini import GroupMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class Group(GroupMini):
    def __init__(
        self,
        id: str,
        *,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        name: Optional[str] = None,
        group_type: Optional[GroupMiniGroupTypeField] = None,
        type: GroupBaseTypeField = GroupBaseTypeField.GROUP,
        **kwargs
    ):
        """
        :param id: The unique identifier for this object.
        :type id: str
        :param created_at: When the group object was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_at: When the group object was last modified., defaults to None
        :type modified_at: Optional[DateTime], optional
        :param name: The name of the group., defaults to None
        :type name: Optional[str], optional
        :param group_type: The type of the group., defaults to None
        :type group_type: Optional[GroupMiniGroupTypeField], optional
        :param type: The value will always be `group`., defaults to GroupBaseTypeField.GROUP
        :type type: GroupBaseTypeField, optional
        """
        super().__init__(id=id, name=name, group_type=group_type, type=type, **kwargs)
        self.created_at = created_at
        self.modified_at = modified_at
