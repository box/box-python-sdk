from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.v2025_r0.hub_v2025_r0 import HubV2025R0

from box_sdk_gen.schemas.v2025_r0.hubs_v2025_r0 import HubsV2025R0

from box_sdk_gen.managers.hubs import GetHubsV2025R0Direction

from box_sdk_gen.managers.hubs import GetEnterpriseHubsV2025R0Direction

from test.commons import get_default_client_with_user_subject

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))


def testCreateUpdateGetAndDeleteHubs():
    hub_title: str = get_uuid()
    hub_description: str = 'new Hub description'
    created_hub: HubV2025R0 = client.hubs.create_hub_v2025_r0(
        hub_title, description=hub_description
    )
    assert created_hub.title == hub_title
    assert created_hub.description == hub_description
    assert to_string(created_hub.type) == 'hubs'
    hub_id: str = created_hub.id
    users_hubs: HubsV2025R0 = client.hubs.get_hubs_v2025_r0(
        scope='all', sort='name', direction=GetHubsV2025R0Direction.ASC
    )
    assert len(users_hubs.entries) > 0
    enterprise_hubs: HubsV2025R0 = client.hubs.get_enterprise_hubs_v2025_r0(
        sort='name', direction=GetEnterpriseHubsV2025R0Direction.ASC
    )
    assert len(enterprise_hubs.entries) > 0
    hub_by_id: HubV2025R0 = client.hubs.get_hub_by_id_v2025_r0(hub_id)
    assert hub_by_id.id == hub_id
    assert hub_by_id.title == hub_title
    assert hub_by_id.description == hub_description
    assert to_string(hub_by_id.type) == 'hubs'
    new_hub_title: str = get_uuid()
    new_hub_description: str = 'updated Hub description'
    updated_hub: HubV2025R0 = client.hubs.update_hub_by_id_v2025_r0(
        hub_id, title=new_hub_title, description=new_hub_description
    )
    assert updated_hub.title == new_hub_title
    assert updated_hub.description == new_hub_description
    client.hubs.delete_hub_by_id_v2025_r0(hub_id)
    with pytest.raises(Exception):
        client.hubs.delete_hub_by_id_v2025_r0(hub_id)


def copyHub():
    hub_title: str = get_uuid()
    hub_description: str = 'new Hub description'
    created_hub: HubV2025R0 = client.hubs.create_hub_v2025_r0(
        hub_title, description=hub_description
    )
    copied_hub_title: str = get_uuid()
    copied_hub_description: str = 'copied Hub description'
    copied_hub: HubV2025R0 = client.hubs.copy_hub_v2025_r0(
        created_hub.id, title=copied_hub_title, description=copied_hub_description
    )
    assert not copied_hub.id == created_hub.id
    assert copied_hub.title == copied_hub_title
    assert copied_hub.description == copied_hub_description
    client.hubs.delete_hub_by_id_v2025_r0(created_hub.id)
    client.hubs.delete_hub_by_id_v2025_r0(copied_hub.id)
