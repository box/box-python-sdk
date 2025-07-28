from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.v2025_r0.hubs_v2025_r0 import HubsV2025R0

from box_sdk_gen.managers.hubs import GetHubsV2025R0Direction

from box_sdk_gen.schemas.v2025_r0.hub_v2025_r0 import HubV2025R0

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.v2025_r0.hub_collaboration_v2025_r0 import (
    HubCollaborationV2025R0,
)

from box_sdk_gen.managers.hub_collaborations import CreateHubCollaborationV2025R0Hub

from box_sdk_gen.managers.hub_collaborations import (
    CreateHubCollaborationV2025R0AccessibleBy,
)

from box_sdk_gen.schemas.v2025_r0.hub_collaborations_v2025_r0 import (
    HubCollaborationsV2025R0,
)

from test.commons import get_default_client_with_user_subject

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))


def testCRUDHubCollaboration():
    hubs: HubsV2025R0 = client.hubs.get_hubs_v2025_r0(
        scope='all', sort='name', direction=GetHubsV2025R0Direction.ASC
    )
    hub: HubV2025R0 = hubs.entries[0]
    user_name: str = get_uuid()
    user_login: str = ''.join([get_uuid(), '@gmail.com'])
    user: UserFull = client.users.create_user(
        user_name, login=user_login, is_platform_access_only=True
    )
    created_collaboration: HubCollaborationV2025R0 = (
        client.hub_collaborations.create_hub_collaboration_v2025_r0(
            CreateHubCollaborationV2025R0Hub(id=hub.id),
            CreateHubCollaborationV2025R0AccessibleBy(type='user', id=user.id),
            'viewer',
        )
    )
    assert not created_collaboration.id == ''
    assert to_string(created_collaboration.type) == 'hub_collaboration'
    assert created_collaboration.hub.id == hub.id
    assert to_string(created_collaboration.accessible_by.type) == 'user'
    assert created_collaboration.accessible_by.id == user.id
    assert created_collaboration.role == 'viewer'
    updated_collaboration: HubCollaborationV2025R0 = (
        client.hub_collaborations.update_hub_collaboration_by_id_v2025_r0(
            created_collaboration.id, role='editor'
        )
    )
    assert not updated_collaboration.id == ''
    assert to_string(updated_collaboration.type) == 'hub_collaboration'
    assert updated_collaboration.hub.id == hub.id
    assert to_string(updated_collaboration.accessible_by.type) == 'user'
    assert updated_collaboration.accessible_by.id == user.id
    assert updated_collaboration.role == 'editor'
    collaborations: HubCollaborationsV2025R0 = (
        client.hub_collaborations.get_hub_collaborations_v2025_r0(hub.id)
    )
    assert len(collaborations.entries) >= 1
    retrieved_collaboration: HubCollaborationV2025R0 = (
        client.hub_collaborations.get_hub_collaboration_by_id_v2025_r0(
            created_collaboration.id
        )
    )
    assert retrieved_collaboration.id == created_collaboration.id
    assert to_string(retrieved_collaboration.type) == 'hub_collaboration'
    assert retrieved_collaboration.hub.id == hub.id
    assert to_string(retrieved_collaboration.accessible_by.type) == 'user'
    assert retrieved_collaboration.accessible_by.id == user.id
    assert retrieved_collaboration.role == 'editor'
    client.hub_collaborations.delete_hub_collaboration_by_id_v2025_r0(
        created_collaboration.id
    )
    client.users.delete_user_by_id(user.id)
