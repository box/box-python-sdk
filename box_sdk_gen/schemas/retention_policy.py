from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.retention_policy_base import RetentionPolicyBaseTypeField

from box_sdk_gen.schemas.retention_policy_base import RetentionPolicyBase

from box_sdk_gen.schemas.retention_policy_mini import (
    RetentionPolicyMiniDispositionActionField,
)

from box_sdk_gen.schemas.retention_policy_mini import RetentionPolicyMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class RetentionPolicyPolicyTypeField(str, Enum):
    FINITE = 'finite'
    INDEFINITE = 'indefinite'


class RetentionPolicyRetentionTypeField(str, Enum):
    MODIFIABLE = 'modifiable'
    NON_MODIFIABLE = 'non_modifiable'


class RetentionPolicyStatusField(str, Enum):
    ACTIVE = 'active'
    RETIRED = 'retired'


class RetentionPolicyAssignmentCountsField(BaseObject):
    def __init__(
        self,
        *,
        enterprise: Optional[int] = None,
        folder: Optional[int] = None,
        metadata_template: Optional[int] = None,
        **kwargs
    ):
        """
        :param enterprise: The number of enterprise assignments this policy has. The maximum value is 1., defaults to None
        :type enterprise: Optional[int], optional
        :param folder: The number of folder assignments this policy has., defaults to None
        :type folder: Optional[int], optional
        :param metadata_template: The number of metadata template assignments this policy has., defaults to None
        :type metadata_template: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.enterprise = enterprise
        self.folder = folder
        self.metadata_template = metadata_template


class RetentionPolicy(RetentionPolicyMini):
    def __init__(
        self,
        id: str,
        *,
        description: Optional[str] = None,
        policy_type: Optional[RetentionPolicyPolicyTypeField] = None,
        retention_type: Optional[RetentionPolicyRetentionTypeField] = None,
        status: Optional[RetentionPolicyStatusField] = None,
        created_by: Optional[UserMini] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        can_owner_extend_retention: Optional[bool] = None,
        are_owners_notified: Optional[bool] = None,
        custom_notification_recipients: Optional[List[UserMini]] = None,
        assignment_counts: Optional[RetentionPolicyAssignmentCountsField] = None,
        policy_name: Optional[str] = None,
        retention_length: Optional[str] = None,
        disposition_action: Optional[RetentionPolicyMiniDispositionActionField] = None,
        type: RetentionPolicyBaseTypeField = RetentionPolicyBaseTypeField.RETENTION_POLICY,
        **kwargs
    ):
        """
                :param id: The unique identifier that represents a retention policy.
                :type id: str
                :param description: The additional text description of the retention policy., defaults to None
                :type description: Optional[str], optional
                :param policy_type: The type of the retention policy. A retention
        policy type can either be `finite`, where a
        specific amount of time to retain the content is known
        upfront, or `indefinite`, where the amount of time
        to retain the content is still unknown., defaults to None
                :type policy_type: Optional[RetentionPolicyPolicyTypeField], optional
                :param retention_type: Specifies the retention type:

        * `modifiable`: You can modify the retention policy. For example,
         you can add or remove folders, shorten or lengthen
         the policy duration, or delete the assignment.
         Use this type if your retention policy
         is not related to any regulatory purposes.

        * `non-modifiable`: You can modify the retention policy
         only in a limited way: add a folder, lengthen the duration,
         retire the policy, change the disposition action
         or notification settings. You cannot perform other actions,
         such as deleting the assignment or shortening the
         policy duration. Use this type to ensure
         compliance with regulatory retention policies., defaults to None
                :type retention_type: Optional[RetentionPolicyRetentionTypeField], optional
                :param status: The status of the retention policy. The status of
        a policy will be `active`, unless explicitly retired by an
        administrator, in which case the status will be `retired`.
        Once a policy has been retired, it cannot become
        active again., defaults to None
                :type status: Optional[RetentionPolicyStatusField], optional
                :param created_at: When the retention policy object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: When the retention policy object was last modified., defaults to None
                :type modified_at: Optional[DateTime], optional
                :param can_owner_extend_retention: Determines if the owner of items under the policy
        can extend the retention when the original
        retention duration is about to end., defaults to None
                :type can_owner_extend_retention: Optional[bool], optional
                :param are_owners_notified: Determines if owners and co-owners of items
        under the policy are notified when
        the retention duration is about to end., defaults to None
                :type are_owners_notified: Optional[bool], optional
                :param custom_notification_recipients: A list of users notified when the retention policy duration is about to end., defaults to None
                :type custom_notification_recipients: Optional[List[UserMini]], optional
                :param assignment_counts: Counts the retention policy assignments for each item type., defaults to None
                :type assignment_counts: Optional[RetentionPolicyAssignmentCountsField], optional
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
        super().__init__(
            id=id,
            policy_name=policy_name,
            retention_length=retention_length,
            disposition_action=disposition_action,
            type=type,
            **kwargs
        )
        self.description = description
        self.policy_type = policy_type
        self.retention_type = retention_type
        self.status = status
        self.created_by = created_by
        self.created_at = created_at
        self.modified_at = modified_at
        self.can_owner_extend_retention = can_owner_extend_retention
        self.are_owners_notified = are_owners_notified
        self.custom_notification_recipients = custom_notification_recipients
        self.assignment_counts = assignment_counts
