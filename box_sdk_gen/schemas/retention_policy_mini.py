from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.retention_policy_base import RetentionPolicyBaseTypeField

from box_sdk_gen.schemas.retention_policy_base import RetentionPolicyBase

from box_sdk_gen.box.errors import BoxSDKError


class RetentionPolicyMiniDispositionActionField(str, Enum):
    PERMANENTLY_DELETE = 'permanently_delete'
    REMOVE_RETENTION = 'remove_retention'


class RetentionPolicyMini(RetentionPolicyBase):
    def __init__(
        self,
        id: str,
        *,
        policy_name: Optional[str] = None,
        retention_length: Optional[str] = None,
        disposition_action: Optional[RetentionPolicyMiniDispositionActionField] = None,
        type: RetentionPolicyBaseTypeField = RetentionPolicyBaseTypeField.RETENTION_POLICY,
        **kwargs
    ):
        """
                :param id: The unique identifier that represents a retention policy.
                :type id: str
                :param policy_name: The name given to the retention policy., defaults to None
                :type policy_name: Optional[str], optional
                :param retention_length: The length of the retention policy. This value
        specifies the duration in days that the retention
        policy will be active for after being assigned to
        content.  If the policy has a `policy_type` of
        `indefinite`, the `retention_length` will also be
        `indefinite`., defaults to None
                :type retention_length: Optional[str], optional
                :param disposition_action: The disposition action of the retention policy.
        This action can be `permanently_delete`, which
        will cause the content retained by the policy
        to be permanently deleted, or `remove_retention`,
        which will lift the retention policy from the content,
        allowing it to be deleted by users,
        once the retention policy has expired., defaults to None
                :type disposition_action: Optional[RetentionPolicyMiniDispositionActionField], optional
                :param type: The value will always be `retention_policy`., defaults to RetentionPolicyBaseTypeField.RETENTION_POLICY
                :type type: RetentionPolicyBaseTypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.policy_name = policy_name
        self.retention_length = retention_length
        self.disposition_action = disposition_action
