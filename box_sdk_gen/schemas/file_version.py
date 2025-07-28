from typing import Optional

from box_sdk_gen.schemas.file_version_base import FileVersionBaseTypeField

from box_sdk_gen.schemas.file_version_base import FileVersionBase

from box_sdk_gen.schemas.file_version_mini import FileVersionMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class FileVersion(FileVersionMini):
    def __init__(
        self,
        id: str,
        *,
        name: Optional[str] = None,
        size: Optional[int] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        modified_by: Optional[UserMini] = None,
        trashed_at: Optional[DateTime] = None,
        trashed_by: Optional[UserMini] = None,
        restored_at: Optional[DateTime] = None,
        restored_by: Optional[UserMini] = None,
        purged_at: Optional[DateTime] = None,
        uploader_display_name: Optional[str] = None,
        sha_1: Optional[str] = None,
        type: FileVersionBaseTypeField = FileVersionBaseTypeField.FILE_VERSION,
        **kwargs
    ):
        """
        :param id: The unique identifier that represent a file version.
        :type id: str
        :param name: The name of the file version., defaults to None
        :type name: Optional[str], optional
        :param size: Size of the file version in bytes., defaults to None
        :type size: Optional[int], optional
        :param created_at: When the file version object was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_at: When the file version object was last updated., defaults to None
        :type modified_at: Optional[DateTime], optional
        :param trashed_at: When the file version object was trashed., defaults to None
        :type trashed_at: Optional[DateTime], optional
        :param restored_at: When the file version was restored from the trash., defaults to None
        :type restored_at: Optional[DateTime], optional
        :param purged_at: When the file version object will be permanently deleted., defaults to None
        :type purged_at: Optional[DateTime], optional
        :param sha_1: The SHA1 hash of this version of the file., defaults to None
        :type sha_1: Optional[str], optional
        :param type: The value will always be `file_version`., defaults to FileVersionBaseTypeField.FILE_VERSION
        :type type: FileVersionBaseTypeField, optional
        """
        super().__init__(id=id, sha_1=sha_1, type=type, **kwargs)
        self.name = name
        self.size = size
        self.created_at = created_at
        self.modified_at = modified_at
        self.modified_by = modified_by
        self.trashed_at = trashed_at
        self.trashed_by = trashed_by
        self.restored_at = restored_at
        self.restored_by = restored_by
        self.purged_at = purged_at
        self.uploader_display_name = uploader_display_name
