from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class LegalHoldPolicyAssignedItemTypeField(str, Enum):
    FILE = 'file'
    FILE_VERSION = 'file_version'
    FOLDER = 'folder'
    USER = 'user'
    OWNERSHIP = 'ownership'
    INTERACTIONS = 'interactions'


class LegalHoldPolicyAssignedItem(BaseObject):
    _discriminator = 'type', {
        'file',
        'file_version',
        'folder',
        'user',
        'ownership',
        'interactions',
    }

    def __init__(self, type: LegalHoldPolicyAssignedItemTypeField, id: str, **kwargs):
        """
        :param type: The type of item the policy is assigned to.
        :type type: LegalHoldPolicyAssignedItemTypeField
        :param id: The ID of the item the policy is assigned to.
        :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
