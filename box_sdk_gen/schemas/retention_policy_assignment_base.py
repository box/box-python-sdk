from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class RetentionPolicyAssignmentBaseTypeField(str, Enum):
    RETENTION_POLICY_ASSIGNMENT = 'retention_policy_assignment'


class RetentionPolicyAssignmentBase(BaseObject):
    _discriminator = 'type', {'retention_policy_assignment'}

    def __init__(
        self,
        id: str,
        *,
        type: RetentionPolicyAssignmentBaseTypeField = RetentionPolicyAssignmentBaseTypeField.RETENTION_POLICY_ASSIGNMENT,
        **kwargs
    ):
        """
        :param id: The unique identifier that represents a file version.
        :type id: str
        :param type: The value will always be `retention_policy_assignment`., defaults to RetentionPolicyAssignmentBaseTypeField.RETENTION_POLICY_ASSIGNMENT
        :type type: RetentionPolicyAssignmentBaseTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
