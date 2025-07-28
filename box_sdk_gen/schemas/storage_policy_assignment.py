from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.storage_policy_mini import StoragePolicyMini

from box_sdk_gen.box.errors import BoxSDKError


class StoragePolicyAssignmentTypeField(str, Enum):
    STORAGE_POLICY_ASSIGNMENT = 'storage_policy_assignment'


class StoragePolicyAssignmentAssignedToField(BaseObject):
    def __init__(
        self, *, id: Optional[str] = None, type: Optional[str] = None, **kwargs
    ):
        """
        :param id: The unique identifier for this object., defaults to None
        :type id: Optional[str], optional
        :param type: The type for this object., defaults to None
        :type type: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class StoragePolicyAssignment(BaseObject):
    _discriminator = 'type', {'storage_policy_assignment'}

    def __init__(
        self,
        id: str,
        *,
        type: StoragePolicyAssignmentTypeField = StoragePolicyAssignmentTypeField.STORAGE_POLICY_ASSIGNMENT,
        storage_policy: Optional[StoragePolicyMini] = None,
        assigned_to: Optional[StoragePolicyAssignmentAssignedToField] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for a storage policy assignment.
        :type id: str
        :param type: The value will always be `storage_policy_assignment`., defaults to StoragePolicyAssignmentTypeField.STORAGE_POLICY_ASSIGNMENT
        :type type: StoragePolicyAssignmentTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.storage_policy = storage_policy
        self.assigned_to = assigned_to
