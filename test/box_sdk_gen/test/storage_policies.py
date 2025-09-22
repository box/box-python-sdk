from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.storage_policies import StoragePolicies

from box_sdk_gen.schemas.storage_policy import StoragePolicy

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

user_id: str = get_env_var('USER_ID')


def testGetStoragePolicies():
    client: BoxClient = get_default_client_with_user_subject(user_id)
    storage_policies: StoragePolicies = client.storage_policies.get_storage_policies()
    storage_policy: StoragePolicy = storage_policies.entries[0]
    assert to_string(storage_policy.type) == 'storage_policy'
    get_storage_policy: StoragePolicy = (
        client.storage_policies.get_storage_policy_by_id(storage_policy.id)
    )
    assert get_storage_policy.id == storage_policy.id
