from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.schemas.storage_policy_assignment import StoragePolicyAssignment

from box_sdk_gen.schemas.storage_policy_assignments import StoragePolicyAssignments

from box_sdk_gen.managers.storage_policy_assignments import (
    GetStoragePolicyAssignmentsResolvedForType,
)

from box_sdk_gen.managers.storage_policy_assignments import (
    CreateStoragePolicyAssignmentStoragePolicy,
)

from box_sdk_gen.managers.storage_policy_assignments import (
    CreateStoragePolicyAssignmentAssignedTo,
)

from box_sdk_gen.managers.storage_policy_assignments import (
    CreateStoragePolicyAssignmentAssignedToTypeField,
)

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.storage_policies import StoragePolicies

from box_sdk_gen.schemas.storage_policy import StoragePolicy

from box_sdk_gen.managers.storage_policy_assignments import (
    UpdateStoragePolicyAssignmentByIdStoragePolicy,
)

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from box_sdk_gen.client import BoxClient

from box_sdk_gen.internal.utils import get_uuid

admin_user_id: str = get_env_var('USER_ID')


def get_or_create_storage_policy_assignment(
    client: BoxClient, policy_id: str, user_id: str
) -> StoragePolicyAssignment:
    storage_policy_assignments: StoragePolicyAssignments = (
        client.storage_policy_assignments.get_storage_policy_assignments(
            GetStoragePolicyAssignmentsResolvedForType.USER, user_id
        )
    )
    if len(storage_policy_assignments.entries) > 0:
        if to_string(storage_policy_assignments.entries[0].assigned_to.type) == 'user':
            return storage_policy_assignments.entries[0]
    storage_policy_assignment: StoragePolicyAssignment = (
        client.storage_policy_assignments.create_storage_policy_assignment(
            CreateStoragePolicyAssignmentStoragePolicy(id=policy_id),
            CreateStoragePolicyAssignmentAssignedTo(
                id=user_id, type=CreateStoragePolicyAssignmentAssignedToTypeField.USER
            ),
        )
    )
    return storage_policy_assignment


def testGetStoragePolicyAssignments():
    client: BoxClient = get_default_client_with_user_subject(admin_user_id)
    user_name: str = get_uuid()
    new_user: UserFull = client.users.create_user(
        user_name, is_platform_access_only=True
    )
    storage_policies: StoragePolicies = client.storage_policies.get_storage_policies()
    storage_policy_1: StoragePolicy = storage_policies.entries[0]
    storage_policy_2: StoragePolicy = storage_policies.entries[1]
    storage_policy_assignment: StoragePolicyAssignment = (
        get_or_create_storage_policy_assignment(
            client, storage_policy_1.id, new_user.id
        )
    )
    assert to_string(storage_policy_assignment.type) == 'storage_policy_assignment'
    assert to_string(storage_policy_assignment.assigned_to.type) == 'user'
    assert storage_policy_assignment.assigned_to.id == new_user.id
    get_storage_policy_assignment: StoragePolicyAssignment = (
        client.storage_policy_assignments.get_storage_policy_assignment_by_id(
            storage_policy_assignment.id
        )
    )
    assert get_storage_policy_assignment.id == storage_policy_assignment.id
    updated_storage_policy_assignment: StoragePolicyAssignment = (
        client.storage_policy_assignments.update_storage_policy_assignment_by_id(
            storage_policy_assignment.id,
            UpdateStoragePolicyAssignmentByIdStoragePolicy(id=storage_policy_2.id),
        )
    )
    assert updated_storage_policy_assignment.storage_policy.id == storage_policy_2.id
    client.storage_policy_assignments.delete_storage_policy_assignment_by_id(
        storage_policy_assignment.id
    )
    client.users.delete_user_by_id(new_user.id)
