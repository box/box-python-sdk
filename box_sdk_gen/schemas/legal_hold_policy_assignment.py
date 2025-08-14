from typing import Optional

from box_sdk_gen.schemas.legal_hold_policy_assignment_base import (
    LegalHoldPolicyAssignmentBaseTypeField,
)

from box_sdk_gen.schemas.file import File

from box_sdk_gen.schemas.folder import Folder

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.schemas.legal_hold_policy_assignment_base import (
    LegalHoldPolicyAssignmentBase,
)

from box_sdk_gen.schemas.legal_hold_policy_mini import LegalHoldPolicyMini

from box_sdk_gen.schemas.legal_hold_policy_assigned_item import (
    LegalHoldPolicyAssignedItem,
)

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class LegalHoldPolicyAssignment(LegalHoldPolicyAssignmentBase):
    def __init__(
        self,
        *,
        legal_hold_policy: Optional[LegalHoldPolicyMini] = None,
        assigned_to: Optional[LegalHoldPolicyAssignedItem] = None,
        assigned_by: Optional[UserMini] = None,
        assigned_at: Optional[DateTime] = None,
        deleted_at: Optional[DateTime] = None,
        id: Optional[str] = None,
        type: Optional[LegalHoldPolicyAssignmentBaseTypeField] = None,
        **kwargs
    ):
        """
                :param assigned_at: When the legal hold policy assignment object was
        created., defaults to None
                :type assigned_at: Optional[DateTime], optional
                :param deleted_at: When the assignment release request was sent.
        (Because it can take time for an assignment to fully
        delete, this isn't quite the same time that the
        assignment is fully deleted). If null, Assignment
        was not deleted., defaults to None
                :type deleted_at: Optional[DateTime], optional
                :param id: The unique identifier for this legal hold assignment., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `legal_hold_policy_assignment`., defaults to None
                :type type: Optional[LegalHoldPolicyAssignmentBaseTypeField], optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.legal_hold_policy = legal_hold_policy
        self.assigned_to = assigned_to
        self.assigned_by = assigned_by
        self.assigned_at = assigned_at
        self.deleted_at = deleted_at
