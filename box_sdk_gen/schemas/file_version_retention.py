from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_version_mini import FileVersionMini

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.schemas.retention_policy_mini import RetentionPolicyMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class FileVersionRetentionTypeField(str, Enum):
    FILE_VERSION_RETENTION = 'file_version_retention'


class FileVersionRetention(BaseObject):
    _discriminator = 'type', {'file_version_retention'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[FileVersionRetentionTypeField] = None,
        file_version: Optional[FileVersionMini] = None,
        file: Optional[FileMini] = None,
        applied_at: Optional[DateTime] = None,
        disposition_at: Optional[DateTime] = None,
        winning_retention_policy: Optional[RetentionPolicyMini] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this file version retention., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `file_version_retention`., defaults to None
                :type type: Optional[FileVersionRetentionTypeField], optional
                :param applied_at: When this file version retention object was
        created., defaults to None
                :type applied_at: Optional[DateTime], optional
                :param disposition_at: When the retention expires on this file
        version retention., defaults to None
                :type disposition_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.file_version = file_version
        self.file = file
        self.applied_at = applied_at
        self.disposition_at = disposition_at
        self.winning_retention_policy = winning_retention_policy
