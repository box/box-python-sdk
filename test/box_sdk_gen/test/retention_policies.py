from box_sdk_gen.schemas.retention_policy import RetentionPolicy

from box_sdk_gen.managers.retention_policies import CreateRetentionPolicyPolicyType

from box_sdk_gen.managers.retention_policies import (
    CreateRetentionPolicyDispositionAction,
)

from box_sdk_gen.managers.retention_policies import CreateRetentionPolicyRetentionType

from box_sdk_gen.schemas.retention_policies import RetentionPolicies

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.client import BoxClient

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testCreateUpdateGetDeleteRetentionPolicy():
    retention_policy_name: str = get_uuid()
    retention_description: str = 'test description'
    retention_policy: RetentionPolicy = (
        client.retention_policies.create_retention_policy(
            retention_policy_name,
            CreateRetentionPolicyPolicyType.FINITE,
            CreateRetentionPolicyDispositionAction.REMOVE_RETENTION,
            description=retention_description,
            retention_length='1',
            retention_type=CreateRetentionPolicyRetentionType.MODIFIABLE,
            can_owner_extend_retention=True,
            are_owners_notified=True,
        )
    )
    assert retention_policy.policy_name == retention_policy_name
    assert retention_policy.description == retention_description
    retention_policy_by_id: RetentionPolicy = (
        client.retention_policies.get_retention_policy_by_id(retention_policy.id)
    )
    assert retention_policy_by_id.id == retention_policy.id
    retention_policies: RetentionPolicies = (
        client.retention_policies.get_retention_policies()
    )
    assert len(retention_policies.entries) > 0
    updated_retention_policy_name: str = get_uuid()
    updated_retention_policy: RetentionPolicy = (
        client.retention_policies.update_retention_policy_by_id(
            retention_policy.id, policy_name=updated_retention_policy_name
        )
    )
    assert updated_retention_policy.policy_name == updated_retention_policy_name
    client.retention_policies.delete_retention_policy_by_id(retention_policy.id)
