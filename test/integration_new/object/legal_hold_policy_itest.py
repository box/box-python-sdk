from test.integration_new import util
from test.integration_new import CLIENT
from boxsdk.exception import BoxAPIException


def test_create_legal_hold_policy():
    policy_name = 'Test Legal Hold Policy ' + util.random_name()
    description = 'Test Legal Hold Policy Description'
    filter_started_at = '2021-12-12T10:53:43-08:00'
    filter_ended_at = '2022-12-18T10:53:43-08:00'

    legal_hold_policy = CLIENT.create_legal_hold_policy(
        policy_name=policy_name,
        description=description,
        filter_started_at=filter_started_at,
        filter_ended_at=filter_ended_at
    )

    try:
        assert legal_hold_policy.policy_name == policy_name
        assert legal_hold_policy.description == description
        assert legal_hold_policy.filter_started_at == filter_started_at
        assert legal_hold_policy.filter_ended_at == filter_ended_at

        new_policy_name = 'Test Legal Hold Policy ' + util.random_name()
        new_policy_description = 'Test Legal Hold Policy Description'
        legal_hold_policy.update_info(data={
            'policy_name': new_policy_name,
            'description': new_policy_description
        })

        legal_hold_policy = CLIENT.legal_hold_policy(policy_id=legal_hold_policy.object_id).get()
        assert legal_hold_policy.policy_name == new_policy_name
        assert legal_hold_policy.description == new_policy_description
    finally:
        legal_hold_policy.delete()
