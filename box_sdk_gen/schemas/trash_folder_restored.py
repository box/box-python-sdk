from enum import Enum

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TrashFolderRestoredTypeField(str, Enum):
    FOLDER = 'folder'


class TrashFolderRestoredPathCollectionField(BaseObject):
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


class TrashFolderRestoredItemStatusField(str, Enum):
    ACTIVE = 'active'
    TRASHED = 'trashed'
    DELETED = 'deleted'


class TrashFolderRestored(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        etag: Optional[str] = None,
        type: Optional[TrashFolderRestoredTypeField] = None,
        sequence_id: Optional[str] = None,
        name: Optional[str] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        description: Optional[str] = None,
        size: Optional[int] = None,
        path_collection: Optional[TrashFolderRestoredPathCollectionField] = None,
        created_by: Optional[UserMini] = None,
        modified_by: Optional[UserMini] = None,
        trashed_at: Optional[str] = None,
        purged_at: Optional[str] = None,
        content_created_at: Optional[DateTime] = None,
        content_modified_at: Optional[DateTime] = None,
        owned_by: Optional[UserMini] = None,
        shared_link: Optional[str] = None,
        folder_upload_email: Optional[str] = None,
        parent: Optional[FolderMini] = None,
        item_status: Optional[TrashFolderRestoredItemStatusField] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier that represent a folder.

        The ID for any folder can be determined
        by visiting a folder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/folders/123`
        the `folder_id` is `123`., defaults to None
                :type id: Optional[str], optional
                :param etag: The HTTP `etag` of this folder. This can be used within some API
        endpoints in the `If-Match` and `If-None-Match` headers to only
        perform changes on the folder if (no) changes have happened., defaults to None
                :type etag: Optional[str], optional
                :param type: The value will always be `folder`., defaults to None
                :type type: Optional[TrashFolderRestoredTypeField], optional
                :param name: The name of the folder., defaults to None
                :type name: Optional[str], optional
                :param created_at: The date and time when the folder was created. This value may
        be `null` for some folders such as the root folder or the trash
        folder., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: The date and time when the folder was last updated. This value may
        be `null` for some folders such as the root folder or the trash
        folder., defaults to None
                :type modified_at: Optional[DateTime], optional
                :param size: The folder size in bytes.

        Be careful parsing this integer as its
        value can get very large., defaults to None
                :type size: Optional[int], optional
                :param trashed_at: The time at which this folder was put in the
        trash - becomes `null` after restore., defaults to None
                :type trashed_at: Optional[str], optional
                :param purged_at: The time at which this folder is expected to be purged
        from the trash  - becomes `null` after restore., defaults to None
                :type purged_at: Optional[str], optional
                :param content_created_at: The date and time at which this folder was originally
        created., defaults to None
                :type content_created_at: Optional[DateTime], optional
                :param content_modified_at: The date and time at which this folder was last updated., defaults to None
                :type content_modified_at: Optional[DateTime], optional
                :param shared_link: The shared link for this file. This will
        be `null` if a folder had been trashed, even though the original shared
        link does become active again., defaults to None
                :type shared_link: Optional[str], optional
                :param folder_upload_email: The folder upload email for this folder. This will
        be `null` if a folder has been trashed, even though the original upload
        email does become active again., defaults to None
                :type folder_upload_email: Optional[str], optional
                :param item_status: Defines if this item has been deleted or not.

        * `active` when the item has is not in the trash,
        * `trashed` when the item has been moved to the trash but not deleted,
        * `deleted` when the item has been permanently deleted., defaults to None
                :type item_status: Optional[TrashFolderRestoredItemStatusField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.etag = etag
        self.type = type
        self.sequence_id = sequence_id
        self.name = name
        self.created_at = created_at
        self.modified_at = modified_at
        self.description = description
        self.size = size
        self.path_collection = path_collection
        self.created_by = created_by
        self.modified_by = modified_by
        self.trashed_at = trashed_at
        self.purged_at = purged_at
        self.content_created_at = content_created_at
        self.content_modified_at = content_modified_at
        self.owned_by = owned_by
        self.shared_link = shared_link
        self.folder_upload_email = folder_upload_email
        self.parent = parent
        self.item_status = item_status
