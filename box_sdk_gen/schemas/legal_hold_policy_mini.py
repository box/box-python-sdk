from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class LegalHoldPolicyMiniTypeField(str, Enum):
    LEGAL_HOLD_POLICY = 'legal_hold_policy'


class LegalHoldPolicyMini(BaseObject):
    _discriminator = 'type', {'legal_hold_policy'}

    def __init__(
        self,
        id: str,
        *,
        type: LegalHoldPolicyMiniTypeField = LegalHoldPolicyMiniTypeField.LEGAL_HOLD_POLICY,
        **kwargs
    ):
        """
        :param id: The unique identifier for this legal hold policy.
        :type id: str
        :param type: The value will always be `legal_hold_policy`., defaults to LegalHoldPolicyMiniTypeField.LEGAL_HOLD_POLICY
        :type type: LegalHoldPolicyMiniTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
