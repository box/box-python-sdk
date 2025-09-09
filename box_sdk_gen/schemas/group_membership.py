from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.schemas.group_mini import GroupMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class GroupMembershipTypeField(str, Enum):
    GROUP_MEMBERSHIP = 'group_membership'


class GroupMembershipRoleField(str, Enum):
    MEMBER = 'member'
    ADMIN = 'admin'


class GroupMembership(BaseObject):
    _discriminator = 'type', {'group_membership'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[GroupMembershipTypeField] = None,
        user: Optional[UserMini] = None,
        group: Optional[GroupMini] = None,
        role: Optional[GroupMembershipRoleField] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this group membership., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `group_membership`., defaults to None
        :type type: Optional[GroupMembershipTypeField], optional
        :param role: The role of the user in the group., defaults to None
        :type role: Optional[GroupMembershipRoleField], optional
        :param created_at: The time this membership was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_at: The time this membership was last modified., defaults to None
        :type modified_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.user = user
        self.group = group
        self.role = role
        self.created_at = created_at
        self.modified_at = modified_at
