from typing import Optional

from box_sdk_gen.schemas.storage_policy_mini import StoragePolicyMiniTypeField

from box_sdk_gen.schemas.storage_policy_mini import StoragePolicyMini

from box_sdk_gen.box.errors import BoxSDKError


class StoragePolicy(StoragePolicyMini):
    def __init__(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        type: StoragePolicyMiniTypeField = StoragePolicyMiniTypeField.STORAGE_POLICY,
        **kwargs
    ):
        """
        :param id: The unique identifier for this storage policy.
        :type id: str
        :param name: A descriptive name of the region., defaults to None
        :type name: Optional[str], optional
        :param type: The value will always be `storage_policy`., defaults to StoragePolicyMiniTypeField.STORAGE_POLICY
        :type type: StoragePolicyMiniTypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.name = name
