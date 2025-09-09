from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.legal_hold_policy_mini import LegalHoldPolicyMiniTypeField

from box_sdk_gen.schemas.legal_hold_policy_mini import LegalHoldPolicyMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class LegalHoldPolicyStatusField(str, Enum):
    ACTIVE = 'active'
    APPLYING = 'applying'
    RELEASING = 'releasing'
    RELEASED = 'released'


class LegalHoldPolicyAssignmentCountsField(BaseObject):
    def __init__(
        self,
        *,
        user: Optional[int] = None,
        folder: Optional[int] = None,
        file: Optional[int] = None,
        file_version: Optional[int] = None,
        **kwargs
    ):
        """
        :param user: The number of users this policy is applied to., defaults to None
        :type user: Optional[int], optional
        :param folder: The number of folders this policy is applied to., defaults to None
        :type folder: Optional[int], optional
        :param file: The number of files this policy is applied to., defaults to None
        :type file: Optional[int], optional
        :param file_version: The number of file versions this policy is applied to., defaults to None
        :type file_version: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.user = user
        self.folder = folder
        self.file = file
        self.file_version = file_version


class LegalHoldPolicy(LegalHoldPolicyMini):
    def __init__(
        self,
        id: str,
        *,
        policy_name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[LegalHoldPolicyStatusField] = None,
        assignment_counts: Optional[LegalHoldPolicyAssignmentCountsField] = None,
        created_by: Optional[UserMini] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        deleted_at: Optional[DateTime] = None,
        filter_started_at: Optional[DateTime] = None,
        filter_ended_at: Optional[DateTime] = None,
        release_notes: Optional[str] = None,
        type: LegalHoldPolicyMiniTypeField = LegalHoldPolicyMiniTypeField.LEGAL_HOLD_POLICY,
        **kwargs
    ):
        """
                :param id: The unique identifier for this legal hold policy.
                :type id: str
                :param policy_name: Name of the legal hold policy., defaults to None
                :type policy_name: Optional[str], optional
                :param description: Description of the legal hold policy. Optional
        property with a 500 character limit., defaults to None
                :type description: Optional[str], optional
                :param status: Possible values:
        * 'active' - the policy is not in a transition state.
        * 'applying' - that the policy is in the process of
          being applied.
        * 'releasing' - that the process is in the process
          of being released.
        * 'released' - the policy is no longer active., defaults to None
                :type status: Optional[LegalHoldPolicyStatusField], optional
                :param assignment_counts: Counts of assignments within this a legal hold policy by item type., defaults to None
                :type assignment_counts: Optional[LegalHoldPolicyAssignmentCountsField], optional
                :param created_at: When the legal hold policy object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: When the legal hold policy object was modified.
        Does not update when assignments are added or removed., defaults to None
                :type modified_at: Optional[DateTime], optional
                :param deleted_at: When the policy release request was sent. (Because
        it can take time for a policy to fully delete, this
        isn't quite the same time that the policy is fully deleted).

        If `null`, the policy was not deleted., defaults to None
                :type deleted_at: Optional[DateTime], optional
                :param filter_started_at: User-specified, optional date filter applies to
        Custodian assignments only., defaults to None
                :type filter_started_at: Optional[DateTime], optional
                :param filter_ended_at: User-specified, optional date filter applies to
        Custodian assignments only., defaults to None
                :type filter_ended_at: Optional[DateTime], optional
                :param release_notes: Optional notes about why the policy was created., defaults to None
                :type release_notes: Optional[str], optional
                :param type: The value will always be `legal_hold_policy`., defaults to LegalHoldPolicyMiniTypeField.LEGAL_HOLD_POLICY
                :type type: LegalHoldPolicyMiniTypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.policy_name = policy_name
        self.description = description
        self.status = status
        self.assignment_counts = assignment_counts
        self.created_by = created_by
        self.created_at = created_at
        self.modified_at = modified_at
        self.deleted_at = deleted_at
        self.filter_started_at = filter_started_at
        self.filter_ended_at = filter_ended_at
        self.release_notes = release_notes
