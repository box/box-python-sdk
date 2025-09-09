from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.file_base import FileBaseTypeField

from box_sdk_gen.schemas.file_base import FileBase

from box_sdk_gen.schemas.file_version_mini import FileVersionMini

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class FilePathCollectionField(BaseObject):
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


class FileSharedLinkAccessField(str, Enum):
    OPEN = 'open'
    COMPANY = 'company'
    COLLABORATORS = 'collaborators'


class FileSharedLinkEffectiveAccessField(str, Enum):
    OPEN = 'open'
    COMPANY = 'company'
    COLLABORATORS = 'collaborators'


class FileSharedLinkEffectivePermissionField(str, Enum):
    CAN_EDIT = 'can_edit'
    CAN_DOWNLOAD = 'can_download'
    CAN_PREVIEW = 'can_preview'
    NO_ACCESS = 'no_access'


class FileSharedLinkPermissionsField(BaseObject):
    def __init__(self, can_download: bool, can_preview: bool, can_edit: bool, **kwargs):
        """
                :param can_download: Defines if the shared link allows for the item to be downloaded. For
        shared links on folders, this also applies to any items in the folder.

        This value can be set to `true` when the effective access level is
        set to `open` or `company`, not `collaborators`.
                :type can_download: bool
                :param can_preview: Defines if the shared link allows for the item to be previewed.

        This value is always `true`. For shared links on folders this also
        applies to any items in the folder.
                :type can_preview: bool
                :param can_edit: Defines if the shared link allows for the item to be edited.

        This value can only be `true` if `can_download` is also `true` and if
        the item has a type of `file`.
                :type can_edit: bool
        """
        super().__init__(**kwargs)
        self.can_download = can_download
        self.can_preview = can_preview
        self.can_edit = can_edit


class FileSharedLinkField(BaseObject):
    def __init__(
        self,
        url: str,
        effective_access: FileSharedLinkEffectiveAccessField,
        effective_permission: FileSharedLinkEffectivePermissionField,
        is_password_enabled: bool,
        download_count: int,
        preview_count: int,
        *,
        download_url: Optional[str] = None,
        vanity_url: Optional[str] = None,
        vanity_name: Optional[str] = None,
        access: Optional[FileSharedLinkAccessField] = None,
        unshared_at: Optional[DateTime] = None,
        permissions: Optional[FileSharedLinkPermissionsField] = None,
        **kwargs
    ):
        """
                :param url: The URL that can be used to access the item on Box.

        This URL will display the item in Box's preview UI where the file
        can be downloaded if allowed.

        This URL will continue to work even when a custom `vanity_url`
        has been set for this shared link.
                :type url: str
                :param effective_access: The effective access level for the shared link. This can be a more
        restrictive access level than the value in the `access` field when the
        enterprise settings restrict the allowed access levels.
                :type effective_access: FileSharedLinkEffectiveAccessField
                :param effective_permission: The effective permissions for this shared link.
        These result in the more restrictive combination of
        the share link permissions and the item permissions set
        by the administrator, the owner, and any ancestor item
        such as a folder.
                :type effective_permission: FileSharedLinkEffectivePermissionField
                :param is_password_enabled: Defines if the shared link requires a password to access the item.
                :type is_password_enabled: bool
                :param download_count: The number of times this item has been downloaded.
                :type download_count: int
                :param preview_count: The number of times this item has been previewed.
                :type preview_count: int
                :param download_url: A URL that can be used to download the file. This URL can be used in
        a browser to download the file. This URL includes the file
        extension so that the file will be saved with the right file type.

        This property will be `null` for folders., defaults to None
                :type download_url: Optional[str], optional
                :param vanity_url: The "Custom URL" that can also be used to preview the item on Box.  Custom
        URLs can only be created or modified in the Box Web application., defaults to None
                :type vanity_url: Optional[str], optional
                :param vanity_name: The custom name of a shared link, as used in the `vanity_url` field., defaults to None
                :type vanity_name: Optional[str], optional
                :param access: The access level for this shared link.

        * `open` - provides access to this item to anyone with this link
        * `company` - only provides access to this item to people the same company
        * `collaborators` - only provides access to this item to people who are
           collaborators on this item

        If this field is omitted when creating the shared link, the access level
        will be set to the default access level specified by the enterprise admin., defaults to None
                :type access: Optional[FileSharedLinkAccessField], optional
                :param unshared_at: The date and time when this link will be unshared. This field can only be
        set by users with paid accounts., defaults to None
                :type unshared_at: Optional[DateTime], optional
                :param permissions: Defines if this link allows a user to preview, edit, and download an item.
        These permissions refer to the shared link only and
        do not supersede permissions applied to the item itself., defaults to None
                :type permissions: Optional[FileSharedLinkPermissionsField], optional
        """
        super().__init__(**kwargs)
        self.url = url
        self.effective_access = effective_access
        self.effective_permission = effective_permission
        self.is_password_enabled = is_password_enabled
        self.download_count = download_count
        self.preview_count = preview_count
        self.download_url = download_url
        self.vanity_url = vanity_url
        self.vanity_name = vanity_name
        self.access = access
        self.unshared_at = unshared_at
        self.permissions = permissions


class FileItemStatusField(str, Enum):
    ACTIVE = 'active'
    TRASHED = 'trashed'
    DELETED = 'deleted'


class File(FileMini):
    def __init__(
        self,
        id: str,
        *,
        description: Optional[str] = None,
        size: Optional[int] = None,
        path_collection: Optional[FilePathCollectionField] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        trashed_at: Optional[DateTime] = None,
        purged_at: Optional[DateTime] = None,
        content_created_at: Optional[DateTime] = None,
        content_modified_at: Optional[DateTime] = None,
        created_by: Optional[UserMini] = None,
        modified_by: Optional[UserMini] = None,
        owned_by: Optional[UserMini] = None,
        shared_link: Optional[FileSharedLinkField] = None,
        parent: Optional[FolderMini] = None,
        item_status: Optional[FileItemStatusField] = None,
        sequence_id: Optional[str] = None,
        name: Optional[str] = None,
        sha_1: Optional[str] = None,
        file_version: Optional[FileVersionMini] = None,
        etag: Optional[str] = None,
        type: FileBaseTypeField = FileBaseTypeField.FILE,
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
                :param description: The optional description of this file.
        If the description exceeds 255 characters, the first 255 characters
        are set as a file description and the rest of it is ignored., defaults to None
                :type description: Optional[str], optional
                :param size: The file size in bytes. Be careful parsing this integer as it can
        get very large and cause an integer overflow., defaults to None
                :type size: Optional[int], optional
                :param created_at: The date and time when the file was created on Box., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: The date and time when the file was last updated on Box., defaults to None
                :type modified_at: Optional[DateTime], optional
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
                :param item_status: Defines if this item has been deleted or not.

        * `active` when the item has is not in the trash
        * `trashed` when the item has been moved to the trash but not deleted
        * `deleted` when the item has been permanently deleted., defaults to None
                :type item_status: Optional[FileItemStatusField], optional
                :param name: The name of the file., defaults to None
                :type name: Optional[str], optional
                :param sha_1: The SHA1 hash of the file. This can be used to compare the contents
        of a file on Box with a local file., defaults to None
                :type sha_1: Optional[str], optional
                :param etag: The HTTP `etag` of this file. This can be used within some API
        endpoints in the `If-Match` and `If-None-Match` headers to only
        perform changes on the file if (no) changes have happened., defaults to None
                :type etag: Optional[str], optional
                :param type: The value will always be `file`., defaults to FileBaseTypeField.FILE
                :type type: FileBaseTypeField, optional
        """
        super().__init__(
            id=id,
            sequence_id=sequence_id,
            name=name,
            sha_1=sha_1,
            file_version=file_version,
            etag=etag,
            type=type,
            **kwargs
        )
        self.description = description
        self.size = size
        self.path_collection = path_collection
        self.created_at = created_at
        self.modified_at = modified_at
        self.trashed_at = trashed_at
        self.purged_at = purged_at
        self.content_created_at = content_created_at
        self.content_modified_at = content_modified_at
        self.created_by = created_by
        self.modified_by = modified_by
        self.owned_by = owned_by
        self.shared_link = shared_link
        self.parent = parent
        self.item_status = item_status
