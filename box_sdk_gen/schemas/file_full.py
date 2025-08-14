from box_sdk_gen.internal.base_object import BaseObject

from enum import Enum

from typing import Optional

from typing import List

from box_sdk_gen.schemas.file_base import FileBaseTypeField

from box_sdk_gen.schemas.file_base import FileBase

from box_sdk_gen.schemas.file_version_mini import FileVersionMini

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.schemas.file import FilePathCollectionField

from box_sdk_gen.schemas.file import FileSharedLinkField

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.file import FileItemStatusField

from box_sdk_gen.schemas.file import File

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.schemas.resource_scope import ResourceScope

from box_sdk_gen.schemas.metadata_full import MetadataFull

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class FileFullPermissionsField(BaseObject):
    def __init__(
        self,
        can_delete: bool,
        can_download: bool,
        can_invite_collaborator: bool,
        can_rename: bool,
        can_set_share_access: bool,
        can_share: bool,
        can_annotate: bool,
        can_comment: bool,
        can_preview: bool,
        can_upload: bool,
        can_view_annotations_all: bool,
        can_view_annotations_self: bool,
        **kwargs
    ):
        """
                :param can_delete: Specifies if the current user can delete this item.
                :type can_delete: bool
                :param can_download: Specifies if the current user can download this item.
                :type can_download: bool
                :param can_invite_collaborator: Specifies if the current user can invite new
        users to collaborate on this item, and if the user can
        update the role of a user already collaborated on this
        item.
                :type can_invite_collaborator: bool
                :param can_rename: Specifies if the user can rename this item.
                :type can_rename: bool
                :param can_set_share_access: Specifies if the user can change the access level of an
        existing shared link on this item.
                :type can_set_share_access: bool
                :param can_share: Specifies if the user can create a shared link for this item.
                :type can_share: bool
                :param can_annotate: Specifies if the user can place annotations on this file.
                :type can_annotate: bool
                :param can_comment: Specifies if the user can place comments on this file.
                :type can_comment: bool
                :param can_preview: Specifies if the user can preview this file.
                :type can_preview: bool
                :param can_upload: Specifies if the user can upload a new version of this file.
                :type can_upload: bool
                :param can_view_annotations_all: Specifies if the user view all annotations placed on this file.
                :type can_view_annotations_all: bool
                :param can_view_annotations_self: Specifies if the user view annotations placed by themselves
        on this file.
                :type can_view_annotations_self: bool
        """
        super().__init__(**kwargs)
        self.can_delete = can_delete
        self.can_download = can_download
        self.can_invite_collaborator = can_invite_collaborator
        self.can_rename = can_rename
        self.can_set_share_access = can_set_share_access
        self.can_share = can_share
        self.can_annotate = can_annotate
        self.can_comment = can_comment
        self.can_preview = can_preview
        self.can_upload = can_upload
        self.can_view_annotations_all = can_view_annotations_all
        self.can_view_annotations_self = can_view_annotations_self


class FileFullLockTypeField(str, Enum):
    LOCK = 'lock'


class FileFullLockAppTypeField(str, Enum):
    GSUITE = 'gsuite'
    OFFICE_WOPI = 'office_wopi'
    OFFICE_WOPIPLUS = 'office_wopiplus'
    OTHER = 'other'


class FileFullLockField(BaseObject):
    _discriminator = 'type', {'lock'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[FileFullLockTypeField] = None,
        created_by: Optional[UserMini] = None,
        created_at: Optional[DateTime] = None,
        expired_at: Optional[DateTime] = None,
        is_download_prevented: Optional[bool] = None,
        app_type: Optional[FileFullLockAppTypeField] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this lock., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `lock`., defaults to None
                :type type: Optional[FileFullLockTypeField], optional
                :param created_at: The time this lock was created at., defaults to None
                :type created_at: Optional[DateTime], optional
                :param expired_at: The time this lock is to expire at, which might be in the past., defaults to None
                :type expired_at: Optional[DateTime], optional
                :param is_download_prevented: Whether or not the file can be downloaded while locked., defaults to None
                :type is_download_prevented: Optional[bool], optional
                :param app_type: If the lock is managed by an application rather than a user, this
        field identifies the type of the application that holds the lock.
        This is an open enum and may be extended with additional values in
        the future., defaults to None
                :type app_type: Optional[FileFullLockAppTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.created_by = created_by
        self.created_at = created_at
        self.expired_at = expired_at
        self.is_download_prevented = is_download_prevented
        self.app_type = app_type


class FileFullExpiringEmbedLinkTokenTypeField(str, Enum):
    BEARER = 'bearer'


class FileFullExpiringEmbedLinkField(BaseObject):
    def __init__(
        self,
        *,
        access_token: Optional[str] = None,
        expires_in: Optional[int] = None,
        token_type: Optional[FileFullExpiringEmbedLinkTokenTypeField] = None,
        restricted_to: Optional[List[ResourceScope]] = None,
        url: Optional[str] = None,
        **kwargs
    ):
        """
                :param access_token: The requested access token., defaults to None
                :type access_token: Optional[str], optional
                :param expires_in: The time in seconds by which this token will expire., defaults to None
                :type expires_in: Optional[int], optional
                :param token_type: The type of access token returned., defaults to None
                :type token_type: Optional[FileFullExpiringEmbedLinkTokenTypeField], optional
                :param restricted_to: The permissions that this access token permits,
        providing a list of resources (files, folders, etc)
        and the scopes permitted for each of those resources., defaults to None
                :type restricted_to: Optional[List[ResourceScope]], optional
                :param url: The actual expiring embed URL for this file, constructed
        from the file ID and access tokens specified in this object., defaults to None
                :type url: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.restricted_to = restricted_to
        self.url = url


class FileFullWatermarkInfoField(BaseObject):
    def __init__(self, *, is_watermarked: Optional[bool] = None, **kwargs):
        """
        :param is_watermarked: Specifies if this item has a watermark applied., defaults to None
        :type is_watermarked: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.is_watermarked = is_watermarked


class FileFullAllowedInviteeRolesField(str, Enum):
    EDITOR = 'editor'
    VIEWER = 'viewer'
    PREVIEWER = 'previewer'
    UPLOADER = 'uploader'
    PREVIEWER_UPLOADER = 'previewer uploader'
    VIEWER_UPLOADER = 'viewer uploader'
    CO_OWNER = 'co-owner'


class FileFullMetadataField(BaseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extra_data = kwargs


class FileFullRepresentationsEntriesContentField(BaseObject):
    def __init__(self, *, url_template: Optional[str] = None, **kwargs):
        """
                :param url_template: The download URL that can be used to fetch the representation.
        Make sure to make an authenticated API call to this endpoint.

        This URL is a template and will require the `{+asset_path}` to
        be replaced by a path. In general, for unpaged representations
        it can be replaced by an empty string.

        For paged representations, replace the `{+asset_path}` with the
        page to request plus the extension for the file, for example
        `1.pdf`.

        When requesting the download URL the following additional
        query params can be passed along.

        * `set_content_disposition_type` - Sets the
        `Content-Disposition` header in the API response with the
        specified disposition type of either `inline` or `attachment`.
        If not supplied, the `Content-Disposition` header is not
        included in the response.

        * `set_content_disposition_filename` - Allows the application to
          define the representation's file name used in the
          `Content-Disposition` header.  If not defined, the filename
          is derived from the source file name in Box combined with the
          extension of the representation., defaults to None
                :type url_template: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.url_template = url_template


class FileFullRepresentationsEntriesInfoField(BaseObject):
    def __init__(self, *, url: Optional[str] = None, **kwargs):
        """
                :param url: The API URL that can be used to get more info on this file
        representation. Make sure to make an authenticated API call
        to this endpoint., defaults to None
                :type url: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.url = url


class FileFullRepresentationsEntriesPropertiesField(BaseObject):
    def __init__(
        self,
        *,
        dimensions: Optional[str] = None,
        paged: Optional[str] = None,
        thumb: Optional[str] = None,
        **kwargs
    ):
        """
                :param dimensions: The width by height size of this representation in pixels., defaults to None
                :type dimensions: Optional[str], optional
                :param paged: Indicates if the representation is build up out of multiple
        pages., defaults to None
                :type paged: Optional[str], optional
                :param thumb: Indicates if the representation can be used as a thumbnail of
        the file., defaults to None
                :type thumb: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.dimensions = dimensions
        self.paged = paged
        self.thumb = thumb


class FileFullRepresentationsEntriesStatusStateField(str, Enum):
    SUCCESS = 'success'
    VIEWABLE = 'viewable'
    PENDING = 'pending'
    NONE = 'none'


class FileFullRepresentationsEntriesStatusField(BaseObject):
    def __init__(
        self,
        *,
        state: Optional[FileFullRepresentationsEntriesStatusStateField] = None,
        **kwargs
    ):
        """
                :param state: The status of the representation.

        * `success` defines the representation as ready to be viewed.
        * `viewable` defines a video to be ready for viewing.
        * `pending` defines the representation as to be generated. Retry
          this endpoint to re-check the status.
        * `none` defines that the representation will be created when
          requested. Request the URL defined in the `info` object to
          trigger this generation., defaults to None
                :type state: Optional[FileFullRepresentationsEntriesStatusStateField], optional
        """
        super().__init__(**kwargs)
        self.state = state


class FileFullRepresentationsEntriesField(BaseObject):
    def __init__(
        self,
        *,
        content: Optional[FileFullRepresentationsEntriesContentField] = None,
        info: Optional[FileFullRepresentationsEntriesInfoField] = None,
        properties: Optional[FileFullRepresentationsEntriesPropertiesField] = None,
        representation: Optional[str] = None,
        status: Optional[FileFullRepresentationsEntriesStatusField] = None,
        **kwargs
    ):
        """
                :param content: An object containing the URL that can be used to actually fetch
        the representation., defaults to None
                :type content: Optional[FileFullRepresentationsEntriesContentField], optional
                :param info: An object containing the URL that can be used to fetch more info
        on this representation., defaults to None
                :type info: Optional[FileFullRepresentationsEntriesInfoField], optional
                :param properties: An object containing the size and type of this presentation., defaults to None
                :type properties: Optional[FileFullRepresentationsEntriesPropertiesField], optional
                :param representation: Indicates the file type of the returned representation., defaults to None
                :type representation: Optional[str], optional
                :param status: An object containing the status of this representation., defaults to None
                :type status: Optional[FileFullRepresentationsEntriesStatusField], optional
        """
        super().__init__(**kwargs)
        self.content = content
        self.info = info
        self.properties = properties
        self.representation = representation
        self.status = status


class FileFullRepresentationsField(BaseObject):
    def __init__(
        self,
        *,
        entries: Optional[List[FileFullRepresentationsEntriesField]] = None,
        **kwargs
    ):
        """
        :param entries: A list of files., defaults to None
        :type entries: Optional[List[FileFullRepresentationsEntriesField]], optional
        """
        super().__init__(**kwargs)
        self.entries = entries


class FileFullClassificationField(BaseObject):
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        definition: Optional[str] = None,
        color: Optional[str] = None,
        **kwargs
    ):
        """
                :param name: The name of the classification., defaults to None
                :type name: Optional[str], optional
                :param definition: An explanation of the meaning of this classification., defaults to None
                :type definition: Optional[str], optional
                :param color: The color that is used to display the
        classification label in a user-interface. Colors are defined by the admin
        or co-admin who created the classification in the Box web app., defaults to None
                :type color: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.name = name
        self.definition = definition
        self.color = color


class FileFullSharedLinkPermissionOptionsField(str, Enum):
    CAN_PREVIEW = 'can_preview'
    CAN_DOWNLOAD = 'can_download'
    CAN_EDIT = 'can_edit'


class FileFull(File):
    def __init__(
        self,
        id: str,
        *,
        version_number: Optional[str] = None,
        comment_count: Optional[int] = None,
        permissions: Optional[FileFullPermissionsField] = None,
        tags: Optional[List[str]] = None,
        lock: Optional[FileFullLockField] = None,
        extension: Optional[str] = None,
        is_package: Optional[bool] = None,
        expiring_embed_link: Optional[FileFullExpiringEmbedLinkField] = None,
        watermark_info: Optional[FileFullWatermarkInfoField] = None,
        is_accessible_via_shared_link: Optional[bool] = None,
        allowed_invitee_roles: Optional[List[FileFullAllowedInviteeRolesField]] = None,
        is_externally_owned: Optional[bool] = None,
        has_collaborations: Optional[bool] = None,
        metadata: Optional[FileFullMetadataField] = None,
        expires_at: Optional[DateTime] = None,
        representations: Optional[FileFullRepresentationsField] = None,
        classification: Optional[FileFullClassificationField] = None,
        uploader_display_name: Optional[str] = None,
        disposition_at: Optional[DateTime] = None,
        shared_link_permission_options: Optional[
            List[FileFullSharedLinkPermissionOptionsField]
        ] = None,
        is_associated_with_app_item: Optional[bool] = None,
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
                :param version_number: The version number of this file., defaults to None
                :type version_number: Optional[str], optional
                :param comment_count: The number of comments on this file., defaults to None
                :type comment_count: Optional[int], optional
                :param extension: Indicates the (optional) file extension for this file. By default,
        this is set to an empty string., defaults to None
                :type extension: Optional[str], optional
                :param is_package: Indicates if the file is a package. Packages are commonly used
        by Mac Applications and can include iWork files., defaults to None
                :type is_package: Optional[bool], optional
                :param is_accessible_via_shared_link: Specifies if the file can be accessed
        via the direct shared link or a shared link
        to a parent folder., defaults to None
                :type is_accessible_via_shared_link: Optional[bool], optional
                :param allowed_invitee_roles: A list of the types of roles that user can be invited at
        when sharing this file., defaults to None
                :type allowed_invitee_roles: Optional[List[FileFullAllowedInviteeRolesField]], optional
                :param is_externally_owned: Specifies if this file is owned by a user outside of the
        authenticated enterprise., defaults to None
                :type is_externally_owned: Optional[bool], optional
                :param has_collaborations: Specifies if this file has any other collaborators., defaults to None
                :type has_collaborations: Optional[bool], optional
                :param expires_at: When the file will automatically be deleted., defaults to None
                :type expires_at: Optional[DateTime], optional
                :param disposition_at: The retention expiration timestamp for the given file., defaults to None
                :type disposition_at: Optional[DateTime], optional
                :param shared_link_permission_options: A list of the types of roles that user can be invited at
        when sharing this file., defaults to None
                :type shared_link_permission_options: Optional[List[FileFullSharedLinkPermissionOptionsField]], optional
                :param is_associated_with_app_item: This field will return true if the file or any ancestor of the file
        is associated with at least one app item. Note that this will return
        true even if the context user does not have access to the app item(s)
        associated with the file., defaults to None
                :type is_associated_with_app_item: Optional[bool], optional
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
            description=description,
            size=size,
            path_collection=path_collection,
            created_at=created_at,
            modified_at=modified_at,
            trashed_at=trashed_at,
            purged_at=purged_at,
            content_created_at=content_created_at,
            content_modified_at=content_modified_at,
            created_by=created_by,
            modified_by=modified_by,
            owned_by=owned_by,
            shared_link=shared_link,
            parent=parent,
            item_status=item_status,
            sequence_id=sequence_id,
            name=name,
            sha_1=sha_1,
            file_version=file_version,
            etag=etag,
            type=type,
            **kwargs
        )
        self.version_number = version_number
        self.comment_count = comment_count
        self.permissions = permissions
        self.tags = tags
        self.lock = lock
        self.extension = extension
        self.is_package = is_package
        self.expiring_embed_link = expiring_embed_link
        self.watermark_info = watermark_info
        self.is_accessible_via_shared_link = is_accessible_via_shared_link
        self.allowed_invitee_roles = allowed_invitee_roles
        self.is_externally_owned = is_externally_owned
        self.has_collaborations = has_collaborations
        self.metadata = metadata
        self.expires_at = expires_at
        self.representations = representations
        self.classification = classification
        self.uploader_display_name = uploader_display_name
        self.disposition_at = disposition_at
        self.shared_link_permission_options = shared_link_permission_options
        self.is_associated_with_app_item = is_associated_with_app_item
