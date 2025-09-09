from typing import Any, Union

from boxsdk.object.enterprise import Enterprise
from boxsdk.object.folder import Folder
from boxsdk.object.metadata_template import MetadataTemplate
from boxsdk.object.retention_policy import RetentionPolicy
from boxsdk.object.retention_policy_assignment import RetentionPolicyAssignment


class BoxRetentionPolicyAssignment:

    def __init__(
        self,
        retention_policy: RetentionPolicy,
        assignee: Union['Folder', 'Enterprise', 'MetadataTemplate'],
    ):
        self._retention_policy_assignment = retention_policy.assign(assignee)

    def __enter__(self) -> RetentionPolicyAssignment:
        return self._retention_policy_assignment

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._retention_policy_assignment.delete()
