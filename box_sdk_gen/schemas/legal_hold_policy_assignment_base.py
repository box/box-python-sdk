from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class LegalHoldPolicyAssignmentBaseTypeField(str, Enum):
    LEGAL_HOLD_POLICY_ASSIGNMENT = 'legal_hold_policy_assignment'


class LegalHoldPolicyAssignmentBase(BaseObject):
    _discriminator = 'type', {'legal_hold_policy_assignment'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[LegalHoldPolicyAssignmentBaseTypeField] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this legal hold assignment., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `legal_hold_policy_assignment`., defaults to None
        :type type: Optional[LegalHoldPolicyAssignmentBaseTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
