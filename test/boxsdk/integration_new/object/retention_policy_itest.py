from test.boxsdk.integration_new import util
from test.boxsdk.integration_new import CLIENT


def test_create_metedata_template_with_fields():
    policy_name = 'Test Retention Policy ' + util.random_name()
    disposition_action = 'permanently_delete'
    retention_length = '1'
    retention_type = 'modifiable'
    policy_description = 'Test Retention Policy'

    retention_policy = CLIENT.create_retention_policy(
        policy_name=policy_name,
        disposition_action=disposition_action,
        retention_length=retention_length,
        retention_type=retention_type,
        description=policy_description,
    )

    try:
        assert retention_policy.policy_name == policy_name
        assert retention_policy.disposition_action == disposition_action
        assert retention_policy.retention_length == retention_length
        assert retention_policy.retention_type == retention_type
        assert retention_policy.description == policy_description

        new_policy_name = 'Test Retention Policy ' + util.random_name()
        new_policy_description = 'Test Retention Policy Updated'
        retention_policy.update_info(
            data={'policy_name': new_policy_name, 'description': new_policy_description}
        )

        retention_policy = CLIENT.retention_policy(
            retention_id=retention_policy.object_id
        ).get()
        assert retention_policy.policy_name == new_policy_name
        assert retention_policy.description == new_policy_description
    finally:
        retention_policy.update_info(data={'status': 'retired'})
