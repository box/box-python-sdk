from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.web_link_base import WebLinkBaseTypeField

from box_sdk_gen.schemas.web_link_base import WebLinkBase

from box_sdk_gen.schemas.web_link_mini import WebLinkMini

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class WebLinkPathCollectionField(BaseObject):
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


class WebLinkSharedLinkAccessField(str, Enum):
    OPEN = 'open'
    COMPANY = 'company'
    COLLABORATORS = 'collaborators'


class WebLinkSharedLinkEffectiveAccessField(str, Enum):
    OPEN = 'open'
    COMPANY = 'company'
    COLLABORATORS = 'collaborators'


class WebLinkSharedLinkEffectivePermissionField(str, Enum):
    CAN_EDIT = 'can_edit'
    CAN_DOWNLOAD = 'can_download'
    CAN_PREVIEW = 'can_preview'
    NO_ACCESS = 'no_access'


class WebLinkSharedLinkPermissionsField(BaseObject):
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


class WebLinkSharedLinkField(BaseObject):
    def __init__(
        self,
        url: str,
        effective_access: WebLinkSharedLinkEffectiveAccessField,
        effective_permission: WebLinkSharedLinkEffectivePermissionField,
        is_password_enabled: bool,
        download_count: int,
        preview_count: int,
        *,
        download_url: Optional[str] = None,
        vanity_url: Optional[str] = None,
        vanity_name: Optional[str] = None,
        access: Optional[WebLinkSharedLinkAccessField] = None,
        unshared_at: Optional[DateTime] = None,
        permissions: Optional[WebLinkSharedLinkPermissionsField] = None,
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
                :type effective_access: WebLinkSharedLinkEffectiveAccessField
                :param effective_permission: The effective permissions for this shared link.
        These result in the more restrictive combination of
        the share link permissions and the item permissions set
        by the administrator, the owner, and any ancestor item
        such as a folder.
                :type effective_permission: WebLinkSharedLinkEffectivePermissionField
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
                :type access: Optional[WebLinkSharedLinkAccessField], optional
                :param unshared_at: The date and time when this link will be unshared. This field can only be
        set by users with paid accounts., defaults to None
                :type unshared_at: Optional[DateTime], optional
                :param permissions: Defines if this link allows a user to preview, edit, and download an item.
        These permissions refer to the shared link only and
        do not supersede permissions applied to the item itself., defaults to None
                :type permissions: Optional[WebLinkSharedLinkPermissionsField], optional
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


class WebLinkItemStatusField(str, Enum):
    ACTIVE = 'active'
    TRASHED = 'trashed'
    DELETED = 'deleted'


class WebLink(WebLinkMini):
    def __init__(
        self,
        id: str,
        *,
        parent: Optional[FolderMini] = None,
        description: Optional[str] = None,
        path_collection: Optional[WebLinkPathCollectionField] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        trashed_at: Optional[DateTime] = None,
        purged_at: Optional[DateTime] = None,
        created_by: Optional[UserMini] = None,
        modified_by: Optional[UserMini] = None,
        owned_by: Optional[UserMini] = None,
        shared_link: Optional[WebLinkSharedLinkField] = None,
        item_status: Optional[WebLinkItemStatusField] = None,
        url: Optional[str] = None,
        sequence_id: Optional[str] = None,
        name: Optional[str] = None,
        type: WebLinkBaseTypeField = WebLinkBaseTypeField.WEB_LINK,
        etag: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this web link.
                :type id: str
                :param description: The description accompanying the web link. This is
        visible within the Box web application., defaults to None
                :type description: Optional[str], optional
                :param created_at: When this file was created on Box’s servers., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: When this file was last updated on the Box
        servers., defaults to None
                :type modified_at: Optional[DateTime], optional
                :param trashed_at: When this file was moved to the trash., defaults to None
                :type trashed_at: Optional[DateTime], optional
                :param purged_at: When this file will be permanently deleted., defaults to None
                :type purged_at: Optional[DateTime], optional
                :param item_status: Whether this item is deleted or not. Values include `active`,
        `trashed` if the file has been moved to the trash, and `deleted` if
        the file has been permanently deleted., defaults to None
                :type item_status: Optional[WebLinkItemStatusField], optional
                :param url: The URL this web link points to., defaults to None
                :type url: Optional[str], optional
                :param name: The name of the web link., defaults to None
                :type name: Optional[str], optional
                :param type: The value will always be `web_link`., defaults to WebLinkBaseTypeField.WEB_LINK
                :type type: WebLinkBaseTypeField, optional
                :param etag: The entity tag of this web link. Used with `If-Match`
        headers., defaults to None
                :type etag: Optional[str], optional
        """
        super().__init__(
            id=id,
            url=url,
            sequence_id=sequence_id,
            name=name,
            type=type,
            etag=etag,
            **kwargs
        )
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
