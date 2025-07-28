from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class RetentionPolicyBaseTypeField(str, Enum):
    RETENTION_POLICY = 'retention_policy'


class RetentionPolicyBase(BaseObject):
    _discriminator = 'type', {'retention_policy'}

    def __init__(
        self,
        id: str,
        *,
        type: RetentionPolicyBaseTypeField = RetentionPolicyBaseTypeField.RETENTION_POLICY,
        **kwargs
    ):
        """
        :param id: The unique identifier that represents a retention policy.
        :type id: str
        :param type: The value will always be `retention_policy`., defaults to RetentionPolicyBaseTypeField.RETENTION_POLICY
        :type type: RetentionPolicyBaseTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
