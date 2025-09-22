from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.group_memberships import GroupMemberships

from box_sdk_gen.schemas.group_full import GroupFull

from box_sdk_gen.schemas.group_membership import GroupMembership

from box_sdk_gen.managers.memberships import CreateGroupMembershipUser

from box_sdk_gen.managers.memberships import CreateGroupMembershipGroup

from box_sdk_gen.managers.memberships import UpdateGroupMembershipByIdRole

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testMemberships():
    user: UserFull = client.users.create_user(
        get_uuid(), login=''.join([get_uuid(), '@boxdemo.com'])
    )
    user_memberships: GroupMemberships = client.memberships.get_user_memberships(
        user.id
    )
    assert user_memberships.total_count == 0
    group: GroupFull = client.groups.create_group(get_uuid())
    group_memberships: GroupMemberships = client.memberships.get_group_memberships(
        group.id
    )
    assert group_memberships.total_count == 0
    group_membership: GroupMembership = client.memberships.create_group_membership(
        CreateGroupMembershipUser(id=user.id), CreateGroupMembershipGroup(id=group.id)
    )
    assert group_membership.user.id == user.id
    assert group_membership.group.id == group.id
    assert to_string(group_membership.role) == 'member'
    get_group_membership: GroupMembership = (
        client.memberships.get_group_membership_by_id(group_membership.id)
    )
    assert get_group_membership.id == group_membership.id
    updated_group_membership: GroupMembership = (
        client.memberships.update_group_membership_by_id(
            group_membership.id, role=UpdateGroupMembershipByIdRole.ADMIN
        )
    )
    assert updated_group_membership.id == group_membership.id
    assert to_string(updated_group_membership.role) == 'admin'
    client.memberships.delete_group_membership_by_id(group_membership.id)
    with pytest.raises(Exception):
        client.memberships.get_group_membership_by_id(group_membership.id)
    client.groups.delete_group_by_id(group.id)
    client.users.delete_user_by_id(user.id)
