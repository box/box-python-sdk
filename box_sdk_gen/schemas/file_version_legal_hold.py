from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_version_mini import FileVersionMini

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.schemas.legal_hold_policy_assignment import LegalHoldPolicyAssignment

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class FileVersionLegalHoldTypeField(str, Enum):
    FILE_VERSION_LEGAL_HOLD = 'file_version_legal_hold'


class FileVersionLegalHold(BaseObject):
    _discriminator = 'type', {'file_version_legal_hold'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[FileVersionLegalHoldTypeField] = None,
        file_version: Optional[FileVersionMini] = None,
        file: Optional[FileMini] = None,
        legal_hold_policy_assignments: Optional[List[LegalHoldPolicyAssignment]] = None,
        deleted_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this file version legal hold., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `file_version_legal_hold`., defaults to None
                :type type: Optional[FileVersionLegalHoldTypeField], optional
                :param legal_hold_policy_assignments: List of assignments contributing to this Hold., defaults to None
                :type legal_hold_policy_assignments: Optional[List[LegalHoldPolicyAssignment]], optional
                :param deleted_at: Time that this File-Version-Legal-Hold was
        deleted., defaults to None
                :type deleted_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.file_version = file_version
        self.file = file
        self.legal_hold_policy_assignments = legal_hold_policy_assignments
        self.deleted_at = deleted_at
