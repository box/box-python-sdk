from typing import Any, Union

from boxsdk.object.retention_policy import RetentionPolicy
from test.integration_new import CLIENT


class BoxRetentionPolicy:

    DEFAULT_RETENTION_POLICY_NAME = "retention_policy_for_integration_tests"

    def __init__(
            self,
            *,
            name: str = DEFAULT_RETENTION_POLICY_NAME,
            disposition_action: str = 'permanently_delete',
            retention_length: Union[float, int] = 1
    ):

        policy_type = 'finite' if retention_length < float('inf') else 'infinite'
        policies_found = list(CLIENT.get_retention_policies(policy_name=name, policy_type=policy_type))

        if policies_found and policies_found[0].get().status == 'active':
            self._retention_policy = policies_found[0]
        else:
            self._retention_policy: RetentionPolicy = CLIENT.create_retention_policy(
                policy_name=name,
                disposition_action=disposition_action,
                retention_length=retention_length
            )

    def __enter__(self) -> RetentionPolicy:
        return self._retention_policy

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass
