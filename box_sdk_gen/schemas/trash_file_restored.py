from enum import Enum

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import Dict

from box_sdk_gen.schemas.file_version_mini import FileVersionMini

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TrashFileRestoredTypeField(str, Enum):
    FILE = 'file'


class TrashFileRestoredPathCollectionField(BaseObject):
    def __init__(self, total_count: int, entries: List[FolderMini], **kwargs):
        """
        :param total_count: The number of folders in this list.
        :type total_count: int
        :param entries: The parent folders for this item.
        :type entries: List[FolderMini]
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.entries = entries


class TrashFileRestoredItemStatusField(str, Enum):
    ACTIVE = 'active'
    TRASHED = 'trashed'
    DELETED = 'deleted'


class TrashFileRestored(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'sha_1': 'sha1',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'sha1': 'sha_1',
        **BaseObject._json_to_fields_mapping,
    }
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        id: str,
        sequence_id: str,
        sha_1: str,
        description: str,
        size: int,
        path_collection: TrashFileRestoredPathCollectionField,
        created_at: DateTime,
        modified_at: DateTime,
        modified_by: UserMini,
        owned_by: UserMini,
        item_status: TrashFileRestoredItemStatusField,
        *,
        etag: Optional[str] = None,
        type: TrashFileRestoredTypeField = TrashFileRestoredTypeField.FILE,
        name: Optional[str] = None,
        file_version: Optional[FileVersionMini] = None,
        trashed_at: Optional[str] = None,
        purged_at: Optional[str] = None,
        content_created_at: Optional[DateTime] = None,
        content_modified_at: Optional[DateTime] = None,
        created_by: Optional[UserMini] = None,
        shared_link: Optional[str] = None,
        parent: Optional[FolderMini] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier that represent a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
                :type id: str
                :param sha_1: The SHA1 hash of the file. This can be used to compare the contents
        of a file on Box with a local file.
                :type sha_1: str
                :param description: The optional description of this file.
                :type description: str
                :param size: The file size in bytes. Be careful parsing this integer as it can
        get very large and cause an integer overflow.
                :type size: int
                :param created_at: The date and time when the file was created on Box.
                :type created_at: DateTime
                :param modified_at: The date and time when the file was last updated on Box.
                :type modified_at: DateTime
                :param item_status: Defines if this item has been deleted or not.

        * `active` when the item has is not in the trash
        * `trashed` when the item has been moved to the trash but not deleted
        * `deleted` when the item has been permanently deleted.
                :type item_status: TrashFileRestoredItemStatusField
                :param etag: The HTTP `etag` of this file. This can be used within some API
        endpoints in the `If-Match` and `If-None-Match` headers to only
        perform changes on the file if (no) changes have happened., defaults to None
                :type etag: Optional[str], optional
                :param type: The value will always be `file`., defaults to TrashFileRestoredTypeField.FILE
                :type type: TrashFileRestoredTypeField, optional
                :param name: The name of the file., defaults to None
                :type name: Optional[str], optional
                :param trashed_at: The time at which this file was put in the
        trash - becomes `null` after restore., defaults to None
                :type trashed_at: Optional[str], optional
                :param purged_at: The time at which this file is expected to be purged
        from the trash  - becomes `null` after restore., defaults to None
                :type purged_at: Optional[str], optional
                :param content_created_at: The date and time at which this file was originally
        created, which might be before it was uploaded to Box., defaults to None
                :type content_created_at: Optional[DateTime], optional
                :param content_modified_at: The date and time at which this file was last updated,
        which might be before it was uploaded to Box., defaults to None
                :type content_modified_at: Optional[DateTime], optional
                :param shared_link: The shared link for this file. This will
        be `null` if a file had been trashed, even though the original shared
        link does become active again., defaults to None
                :type shared_link: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.sequence_id = sequence_id
        self.sha_1 = sha_1
        self.description = description
        self.size = size
        self.path_collection = path_collection
        self.created_at = created_at
        self.modified_at = modified_at
        self.modified_by = modified_by
        self.owned_by = owned_by
        self.item_status = item_status
        self.etag = etag
        self.type = type
        self.name = name
        self.file_version = file_version
        self.trashed_at = trashed_at
        self.purged_at = purged_at
        self.content_created_at = content_created_at
        self.content_modified_at = content_modified_at
        self.created_by = created_by
        self.shared_link = shared_link
        self.parent = parent
