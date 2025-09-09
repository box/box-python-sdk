from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.group_base import GroupBaseTypeField

from box_sdk_gen.schemas.group_base import GroupBase

from box_sdk_gen.schemas.group_mini import GroupMiniGroupTypeField

from box_sdk_gen.schemas.group_mini import GroupMini

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.group import Group

from box_sdk_gen.box.errors import BoxSDKError


class GroupFullInvitabilityLevelField(str, Enum):
    ADMINS_ONLY = 'admins_only'
    ADMINS_AND_MEMBERS = 'admins_and_members'
    ALL_MANAGED_USERS = 'all_managed_users'


class GroupFullMemberViewabilityLevelField(str, Enum):
    ADMINS_ONLY = 'admins_only'
    ADMINS_AND_MEMBERS = 'admins_and_members'
    ALL_MANAGED_USERS = 'all_managed_users'


class GroupFullPermissionsField(BaseObject):
    def __init__(self, *, can_invite_as_collaborator: Optional[bool] = None, **kwargs):
        """
        :param can_invite_as_collaborator: Specifies if the user can invite the group to collaborate on any items., defaults to None
        :type can_invite_as_collaborator: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.can_invite_as_collaborator = can_invite_as_collaborator


class GroupFull(Group):
    def __init__(
        self,
        id: str,
        *,
        provenance: Optional[str] = None,
        external_sync_identifier: Optional[str] = None,
        description: Optional[str] = None,
        invitability_level: Optional[GroupFullInvitabilityLevelField] = None,
        member_viewability_level: Optional[GroupFullMemberViewabilityLevelField] = None,
        permissions: Optional[GroupFullPermissionsField] = None,
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
                :param provenance: Keeps track of which external source this group is
        coming from (e.g. "Active Directory", "Google Groups",
        "Facebook Groups").  Setting this will
        also prevent Box users from editing the group name
        and its members directly via the Box web application.
        This is desirable for one-way syncing of groups., defaults to None
                :type provenance: Optional[str], optional
                :param external_sync_identifier: An arbitrary identifier that can be used by
        external group sync tools to link this Box Group to
        an external group. Example values of this field
        could be an Active Directory Object ID or a Google
        Group ID.  We recommend you use of this field in
        order to avoid issues when group names are updated in
        either Box or external systems., defaults to None
                :type external_sync_identifier: Optional[str], optional
                :param description: Human readable description of the group., defaults to None
                :type description: Optional[str], optional
                :param invitability_level: Specifies who can invite the group to collaborate
        on items.

        When set to `admins_only` the enterprise admin, co-admins,
        and the group's admin can invite the group.

        When set to `admins_and_members` all the admins listed
        above and group members can invite the group.

        When set to `all_managed_users` all managed users in the
        enterprise can invite the group., defaults to None
                :type invitability_level: Optional[GroupFullInvitabilityLevelField], optional
                :param member_viewability_level: Specifies who can view the members of the group
        (Get Memberships for Group).

        * `admins_only` - the enterprise admin, co-admins, group's
          group admin.
        * `admins_and_members` - all admins and group members.
        * `all_managed_users` - all managed users in the
          enterprise., defaults to None
                :type member_viewability_level: Optional[GroupFullMemberViewabilityLevelField], optional
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
        super().__init__(
            id=id,
            created_at=created_at,
            modified_at=modified_at,
            name=name,
            group_type=group_type,
            type=type,
            **kwargs
        )
        self.provenance = provenance
        self.external_sync_identifier = external_sync_identifier
        self.description = description
        self.invitability_level = invitability_level
        self.member_viewability_level = member_viewability_level
        self.permissions = permissions
