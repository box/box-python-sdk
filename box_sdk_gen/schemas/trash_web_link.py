from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TrashWebLinkTypeField(str, Enum):
    WEB_LINK = 'web_link'


class TrashWebLinkPathCollectionEntriesTypeField(str, Enum):
    FOLDER = 'folder'


class TrashWebLinkPathCollectionEntriesField(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        *,
        type: Optional[TrashWebLinkPathCollectionEntriesTypeField] = None,
        id: Optional[str] = None,
        sequence_id: Optional[str] = None,
        etag: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param type: The value will always be `folder`., defaults to None
        :type type: Optional[TrashWebLinkPathCollectionEntriesTypeField], optional
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


class TrashWebLinkPathCollectionField(BaseObject):
    def __init__(
        self,
        total_count: int,
        entries: List[TrashWebLinkPathCollectionEntriesField],
        **kwargs
    ):
        """
        :param total_count: The number of folders in this list.
        :type total_count: int
        :param entries: Array of folders for this item's path collection.
        :type entries: List[TrashWebLinkPathCollectionEntriesField]
        """
        super().__init__(**kwargs)
        self.total_count = total_count
        self.entries = entries


class TrashWebLinkItemStatusField(str, Enum):
    ACTIVE = 'active'
    TRASHED = 'trashed'
    DELETED = 'deleted'


class TrashWebLink(BaseObject):
    _discriminator = 'type', {'web_link'}

    def __init__(
        self,
        *,
        type: Optional[TrashWebLinkTypeField] = None,
        id: Optional[str] = None,
        sequence_id: Optional[str] = None,
        etag: Optional[str] = None,
        name: Optional[str] = None,
        url: Optional[str] = None,
        parent: Optional[FolderMini] = None,
        description: Optional[str] = None,
        path_collection: Optional[TrashWebLinkPathCollectionField] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        trashed_at: Optional[DateTime] = None,
        purged_at: Optional[DateTime] = None,
        created_by: Optional[UserMini] = None,
        modified_by: Optional[UserMini] = None,
        owned_by: Optional[UserMini] = None,
        shared_link: Optional[str] = None,
        item_status: Optional[TrashWebLinkItemStatusField] = None,
        **kwargs
    ):
        """
                :param type: The value will always be `web_link`., defaults to None
                :type type: Optional[TrashWebLinkTypeField], optional
                :param id: The unique identifier for this web link., defaults to None
                :type id: Optional[str], optional
                :param etag: The entity tag of this web link. Used with `If-Match`
        headers., defaults to None
                :type etag: Optional[str], optional
                :param name: The name of the web link., defaults to None
                :type name: Optional[str], optional
                :param url: The URL this web link points to., defaults to None
                :type url: Optional[str], optional
                :param description: The description accompanying the web link. This is
        visible within the Box web application., defaults to None
                :type description: Optional[str], optional
                :param created_at: When this file was created on Box’s servers., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: When this file was last updated on the Box
        servers., defaults to None
                :type modified_at: Optional[DateTime], optional
                :param trashed_at: When this file was last moved to the trash., defaults to None
                :type trashed_at: Optional[DateTime], optional
                :param purged_at: When this file will be permanently deleted., defaults to None
                :type purged_at: Optional[DateTime], optional
                :param shared_link: The shared link for this bookmark. This will
        be `null` if a bookmark has been trashed, since the link will no longer
        be active., defaults to None
                :type shared_link: Optional[str], optional
                :param item_status: Whether this item is deleted or not. Values include `active`,
        `trashed` if the file has been moved to the trash, and `deleted` if
        the file has been permanently deleted., defaults to None
                :type item_status: Optional[TrashWebLinkItemStatusField], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.sequence_id = sequence_id
        self.etag = etag
        self.name = name
        self.url = url
        self.parent = parent
        self.description = description
        self.path_collection = path_collection
        self.created_at = created_at
        self.modified_at = modified_at
        self.trashed_at = trashed_at
        self.purged_at = purged_at
        self.created_by = created_by
        self.modified_by = modified_by
        self.owned_by = owned_by
        self.shared_link = shared_link
        self.item_status = item_status
