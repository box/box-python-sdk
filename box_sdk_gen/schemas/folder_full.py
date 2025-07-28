from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import List

from box_sdk_gen.schemas.folder_base import FolderBaseTypeField

from box_sdk_gen.schemas.folder_base import FolderBase

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.folder import FolderPathCollectionField

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.schemas.folder import FolderSharedLinkField

from box_sdk_gen.schemas.folder import FolderFolderUploadEmailField

from box_sdk_gen.schemas.folder import FolderItemStatusField

from box_sdk_gen.schemas.items import Items

from box_sdk_gen.schemas.folder import Folder

from box_sdk_gen.schemas.metadata_full import MetadataFull

from box_sdk_gen.box.errors import BoxSDKError


class FolderFullSyncStateField(str, Enum):
    SYNCED = 'synced'
    NOT_SYNCED = 'not_synced'
    PARTIALLY_SYNCED = 'partially_synced'


class FolderFullPermissionsField(BaseObject):
    def __init__(
        self,
        can_delete: bool,
        can_download: bool,
        can_invite_collaborator: bool,
        can_rename: bool,
        can_set_share_access: bool,
        can_share: bool,
        can_upload: bool,
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
                :param can_upload: Specifies if the user can upload into this folder.
                :type can_upload: bool
        """
        super().__init__(**kwargs)
        self.can_delete = can_delete
        self.can_download = can_download
        self.can_invite_collaborator = can_invite_collaborator
        self.can_rename = can_rename
        self.can_set_share_access = can_set_share_access
        self.can_share = can_share
        self.can_upload = can_upload


class FolderFullMetadataField(BaseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extra_data = kwargs


class FolderFullAllowedSharedLinkAccessLevelsField(str, Enum):
    OPEN = 'open'
    COMPANY = 'company'
    COLLABORATORS = 'collaborators'


class FolderFullAllowedInviteeRolesField(str, Enum):
    EDITOR = 'editor'
    VIEWER = 'viewer'
    PREVIEWER = 'previewer'
    UPLOADER = 'uploader'
    PREVIEWER_UPLOADER = 'previewer uploader'
    VIEWER_UPLOADER = 'viewer uploader'
    CO_OWNER = 'co-owner'


class FolderFullWatermarkInfoField(BaseObject):
    def __init__(self, *, is_watermarked: Optional[bool] = None, **kwargs):
        """
        :param is_watermarked: Specifies if this item has a watermark applied., defaults to None
        :type is_watermarked: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.is_watermarked = is_watermarked


class FolderFullClassificationField(BaseObject):
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


class FolderFull(Folder):
    def __init__(
        self,
        id: str,
        *,
        sync_state: Optional[FolderFullSyncStateField] = None,
        has_collaborations: Optional[bool] = None,
        permissions: Optional[FolderFullPermissionsField] = None,
        tags: Optional[List[str]] = None,
        can_non_owners_invite: Optional[bool] = None,
        is_externally_owned: Optional[bool] = None,
        metadata: Optional[FolderFullMetadataField] = None,
        is_collaboration_restricted_to_enterprise: Optional[bool] = None,
        allowed_shared_link_access_levels: Optional[
            List[FolderFullAllowedSharedLinkAccessLevelsField]
        ] = None,
        allowed_invitee_roles: Optional[
            List[FolderFullAllowedInviteeRolesField]
        ] = None,
        watermark_info: Optional[FolderFullWatermarkInfoField] = None,
        is_accessible_via_shared_link: Optional[bool] = None,
        can_non_owners_view_collaborators: Optional[bool] = None,
        classification: Optional[FolderFullClassificationField] = None,
        is_associated_with_app_item: Optional[bool] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        description: Optional[str] = None,
        size: Optional[int] = None,
        path_collection: Optional[FolderPathCollectionField] = None,
        created_by: Optional[UserMini] = None,
        modified_by: Optional[UserMini] = None,
        trashed_at: Optional[DateTime] = None,
        purged_at: Optional[DateTime] = None,
        content_created_at: Optional[DateTime] = None,
        content_modified_at: Optional[DateTime] = None,
        owned_by: Optional[UserMini] = None,
        shared_link: Optional[FolderSharedLinkField] = None,
        folder_upload_email: Optional[FolderFolderUploadEmailField] = None,
        parent: Optional[FolderMini] = None,
        item_status: Optional[FolderItemStatusField] = None,
        item_collection: Optional[Items] = None,
        sequence_id: Optional[str] = None,
        name: Optional[str] = None,
        etag: Optional[str] = None,
        type: FolderBaseTypeField = FolderBaseTypeField.FOLDER,
        **kwargs
    ):
        """
                :param id: The unique identifier that represent a folder.

        The ID for any folder can be determined
        by visiting a folder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/folders/123`
        the `folder_id` is `123`.
                :type id: str
                :param has_collaborations: Specifies if this folder has any other collaborators., defaults to None
                :type has_collaborations: Optional[bool], optional
                :param is_externally_owned: Specifies if this folder is owned by a user outside of the
        authenticated enterprise., defaults to None
                :type is_externally_owned: Optional[bool], optional
                :param allowed_shared_link_access_levels: A list of access levels that are available
        for this folder.

        For some folders, like the root folder, this will always
        be an empty list as sharing is not allowed at that level., defaults to None
                :type allowed_shared_link_access_levels: Optional[List[FolderFullAllowedSharedLinkAccessLevelsField]], optional
                :param allowed_invitee_roles: A list of the types of roles that user can be invited at
        when sharing this folder., defaults to None
                :type allowed_invitee_roles: Optional[List[FolderFullAllowedInviteeRolesField]], optional
                :param is_accessible_via_shared_link: Specifies if the folder can be accessed
        with the direct shared link or a shared link
        to a parent folder., defaults to None
                :type is_accessible_via_shared_link: Optional[bool], optional
                :param can_non_owners_view_collaborators: Specifies if collaborators who are not owners
        of this folder are restricted from viewing other
        collaborations on this folder.

        It also restricts non-owners from inviting new
        collaborators., defaults to None
                :type can_non_owners_view_collaborators: Optional[bool], optional
                :param is_associated_with_app_item: This field will return true if the folder or any ancestor of the
        folder is associated with at least one app item. Note that this will
        return true even if the context user does not have access to the
        app item(s) associated with the folder., defaults to None
                :type is_associated_with_app_item: Optional[bool], optional
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
                :param trashed_at: The time at which this folder was put in the trash., defaults to None
                :type trashed_at: Optional[DateTime], optional
                :param purged_at: The time at which this folder is expected to be purged
        from the trash., defaults to None
                :type purged_at: Optional[DateTime], optional
                :param content_created_at: The date and time at which this folder was originally
        created., defaults to None
                :type content_created_at: Optional[DateTime], optional
                :param content_modified_at: The date and time at which this folder was last updated., defaults to None
                :type content_modified_at: Optional[DateTime], optional
                :param folder_upload_email: The `folder_upload_email` parameter is not `null` if one of the following options is **true**:

          * The **Allow uploads to this folder via email** and the **Only allow email uploads from collaborators in this folder** are [enabled for a folder in the Admin Console](https://support.box.com/hc/en-us/articles/360043697534-Upload-to-Box-Through-Email), and the user has at least **Upload** permissions granted.

          * The **Allow uploads to this folder via email** setting is enabled for a folder in the Admin Console, and the **Only allow email uploads from collaborators in this folder** setting is deactivated (unchecked).

        If the conditions are not met, the parameter will have the following value: `folder_upload_email: null`., defaults to None
                :type folder_upload_email: Optional[FolderFolderUploadEmailField], optional
                :param item_status: Defines if this item has been deleted or not.

        * `active` when the item has is not in the trash
        * `trashed` when the item has been moved to the trash but not deleted
        * `deleted` when the item has been permanently deleted., defaults to None
                :type item_status: Optional[FolderItemStatusField], optional
                :param name: The name of the folder., defaults to None
                :type name: Optional[str], optional
                :param etag: The HTTP `etag` of this folder. This can be used within some API
        endpoints in the `If-Match` and `If-None-Match` headers to only
        perform changes on the folder if (no) changes have happened., defaults to None
                :type etag: Optional[str], optional
                :param type: The value will always be `folder`., defaults to FolderBaseTypeField.FOLDER
                :type type: FolderBaseTypeField, optional
        """
        super().__init__(
            id=id,
            created_at=created_at,
            modified_at=modified_at,
            description=description,
            size=size,
            path_collection=path_collection,
            created_by=created_by,
            modified_by=modified_by,
            trashed_at=trashed_at,
            purged_at=purged_at,
            content_created_at=content_created_at,
            content_modified_at=content_modified_at,
            owned_by=owned_by,
            shared_link=shared_link,
            folder_upload_email=folder_upload_email,
            parent=parent,
            item_status=item_status,
            item_collection=item_collection,
            sequence_id=sequence_id,
            name=name,
            etag=etag,
            type=type,
            **kwargs
        )
        self.sync_state = sync_state
        self.has_collaborations = has_collaborations
        self.permissions = permissions
        self.tags = tags
        self.can_non_owners_invite = can_non_owners_invite
        self.is_externally_owned = is_externally_owned
        self.metadata = metadata
        self.is_collaboration_restricted_to_enterprise = (
            is_collaboration_restricted_to_enterprise
        )
        self.allowed_shared_link_access_levels = allowed_shared_link_access_levels
        self.allowed_invitee_roles = allowed_invitee_roles
        self.watermark_info = watermark_info
        self.is_accessible_via_shared_link = is_accessible_via_shared_link
        self.can_non_owners_view_collaborators = can_non_owners_view_collaborators
        self.classification = classification
        self.is_associated_with_app_item = is_associated_with_app_item
