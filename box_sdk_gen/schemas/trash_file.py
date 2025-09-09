from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Dict

from box_sdk_gen.schemas.file_version_mini import FileVersionMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TrashFileTypeField(str, Enum):
    FILE = 'file'


class TrashFilePathCollectionEntriesTypeField(str, Enum):
    FOLDER = 'folder'


class TrashFilePathCollectionEntriesField(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        *,
        type: Optional[TrashFilePathCollectionEntriesTypeField] = None,
        id: Optional[str] = None,
        sequence_id: Optional[str] = None,
        etag: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The value will always be `folder`., defaults to None
        :type type: Optional[TrashFilePathCollectionEntriesTypeField], optional
        :param id: The unique identifier that represent a folder., defaults to None
        :type id: Optional[str], optional
        :param sequence_id: This field is null for the Trash folder., defaults to None
        :type sequence_id: Optional[str], optional
        :param etag: This field is null for the Trash folder., defaults to None
        :type etag: Optional[str], optional
        :param name: The name of the Trash folder., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.sequence_id = sequence_id
        self.etag = etag
        self.name = name


class TrashFilePathCollectionField(BaseObject):
    def __init__(
        self,
        total_count: int,
        entries: List[TrashFilePathCollectionEntriesField],
        **kwargs
    ):
        """
        :param total_count: The number of folders in this list.
        :type total_count: int
        :param entries: Array of folders for this item's path collection.
        :type entries: List[TrashFilePathCollectionEntriesField]
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.entries = entries


class TrashFileItemStatusField(str, Enum):
    ACTIVE = 'active'
    TRASHED = 'trashed'
    DELETED = 'deleted'


class TrashFile(BaseObject):
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
        path_collection: TrashFilePathCollectionField,
        created_at: DateTime,
        modified_at: DateTime,
        modified_by: UserMini,
        owned_by: UserMini,
        item_status: TrashFileItemStatusField,
        *,
        etag: Optional[str] = None,
        type: TrashFileTypeField = TrashFileTypeField.FILE,
        name: Optional[str] = None,
        file_version: Optional[FileVersionMini] = None,
        trashed_at: Optional[DateTime] = None,
        purged_at: Optional[DateTime] = None,
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
                :type item_status: TrashFileItemStatusField
                :param etag: The HTTP `etag` of this file. This can be used within some API
        endpoints in the `If-Match` and `If-None-Match` headers to only
        perform changes on the file if (no) changes have happened., defaults to None
                :type etag: Optional[str], optional
                :param type: The value will always be `file`., defaults to TrashFileTypeField.FILE
                :type type: TrashFileTypeField, optional
                :param name: The name of the file., defaults to None
                :type name: Optional[str], optional
                :param trashed_at: The time at which this file was put in the trash., defaults to None
                :type trashed_at: Optional[DateTime], optional
                :param purged_at: The time at which this file is expected to be purged
        from the trash., defaults to None
                :type purged_at: Optional[DateTime], optional
                :param content_created_at: The date and time at which this file was originally
        created, which might be before it was uploaded to Box., defaults to None
                :type content_created_at: Optional[DateTime], optional
                :param content_modified_at: The date and time at which this file was last updated,
        which might be before it was uploaded to Box., defaults to None
                :type content_modified_at: Optional[DateTime], optional
                :param shared_link: The shared link for this file. This will
        be `null` if a file has been trashed, since the link will no longer
        be active., defaults to None
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
