from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.managers.folders import CreateFolderParent

from box_sdk_gen.schemas.v2025_r0.hub_v2025_r0 import HubV2025R0

from box_sdk_gen.schemas.v2025_r0.hub_items_v2025_r0 import HubItemsV2025R0

from box_sdk_gen.schemas.v2025_r0.hub_items_manage_response_v2025_r0 import (
    HubItemsManageResponseV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_item_operation_v2025_r0 import (
    HubItemOperationV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_item_operation_v2025_r0 import (
    HubItemOperationV2025R0ActionField,
)

from box_sdk_gen.schemas.v2025_r0.hub_item_operation_result_v2025_r0 import (
    HubItemOperationResultV2025R0,
)

from test.commons import get_default_client_with_user_subject

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.schemas.v2025_r0.folder_reference_v2025_r0 import (
    FolderReferenceV2025R0,
)

client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))


def testCreateDeleteGetHubItems():
    hub_title: str = get_uuid()
    folder: FolderFull = client.folders.create_folder(
        get_uuid(), CreateFolderParent(id='0')
    )
    created_hub: HubV2025R0 = client.hubs.create_hub_v2025_r0(hub_title)
    hub_items_before_add: HubItemsV2025R0 = client.hub_items.get_hub_items_v2025_r0(
        created_hub.id
    )
    assert len(hub_items_before_add.entries) == 0
    added_hub_items: HubItemsManageResponseV2025R0 = (
        client.hub_items.manage_hub_items_v2025_r0(
            created_hub.id,
            operations=[
                HubItemOperationV2025R0(
                    action=HubItemOperationV2025R0ActionField.ADD,
                    item=FolderReferenceV2025R0(id=folder.id),
                )
            ],
        )
    )
    added_hub_item: HubItemOperationResultV2025R0 = added_hub_items.operations[0]
    assert to_string(added_hub_item.action) == 'add'
    assert added_hub_item.status == 200
    assert added_hub_item.item.id == folder.id
    assert added_hub_item.item.type == 'folder'
    hub_items_after_add: HubItemsV2025R0 = client.hub_items.get_hub_items_v2025_r0(
        created_hub.id
    )
    assert len(hub_items_after_add.entries) == 1
    removed_hub_items: HubItemsManageResponseV2025R0 = (
        client.hub_items.manage_hub_items_v2025_r0(
            created_hub.id,
            operations=[
                HubItemOperationV2025R0(
                    action=HubItemOperationV2025R0ActionField.REMOVE,
                    item=FolderReferenceV2025R0(id=folder.id),
                )
            ],
        )
    )
    removed_hub_item: HubItemOperationResultV2025R0 = removed_hub_items.operations[0]
    assert to_string(removed_hub_item.action) == 'remove'
    assert removed_hub_item.status == 200
    assert removed_hub_item.item.id == folder.id
    assert removed_hub_item.item.type == 'folder'
    hub_items_after_remove: HubItemsV2025R0 = client.hub_items.get_hub_items_v2025_r0(
        created_hub.id
    )
    assert len(hub_items_after_remove.entries) == 0
    client.hubs.delete_hub_by_id_v2025_r0(created_hub.id)
    client.folders.delete_folder_by_id(folder.id)
