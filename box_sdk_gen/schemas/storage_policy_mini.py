from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class StoragePolicyMiniTypeField(str, Enum):
    STORAGE_POLICY = 'storage_policy'


class StoragePolicyMini(BaseObject):
    _discriminator = 'type', {'storage_policy'}

    def __init__(
        self,
        id: str,
        *,
        type: StoragePolicyMiniTypeField = StoragePolicyMiniTypeField.STORAGE_POLICY,
        **kwargs
    ):
        """
        :param id: The unique identifier for this storage policy.
        :type id: str
        :param type: The value will always be `storage_policy`., defaults to StoragePolicyMiniTypeField.STORAGE_POLICY
        :type type: StoragePolicyMiniTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
