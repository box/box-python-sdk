import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.groups import Groups

from box_sdk_gen.schemas.group_full import GroupFull

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def test_get_groups():
    groups: Groups = client.groups.get_groups()
    assert groups.total_count >= 0


def test_create_get_delete_group():
    group_name: str = get_uuid()
    group_description: str = 'Group description'
    group: GroupFull = client.groups.create_group(
        group_name, description=group_description
    )
    assert group.name == group_name
    group_by_id: GroupFull = client.groups.get_group_by_id(
        group.id, fields=['id', 'name', 'description', 'group_type']
    )
    assert group_by_id.id == group.id
    assert group_by_id.description == group_description
    updated_group_name: str = get_uuid()
    updated_group: GroupFull = client.groups.update_group_by_id(
        group.id, name=updated_group_name
    )
    assert updated_group.name == updated_group_name
    client.groups.delete_group_by_id(group.id)
    with pytest.raises(Exception):
        client.groups.get_group_by_id(group.id)
