from enum import Enum

from typing import Optional

from typing import Union

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.box.errors import BoxSDKError


class FileOrFolderScopeScopeField(str, Enum):
    ANNOTATION_EDIT = 'annotation_edit'
    ANNOTATION_VIEW_ALL = 'annotation_view_all'
    ANNOTATION_VIEW_SELF = 'annotation_view_self'
    BASE_EXPLORER = 'base_explorer'
    BASE_PICKER = 'base_picker'
    BASE_PREVIEW = 'base_preview'
    BASE_UPLOAD = 'base_upload'
    ITEM_DELETE = 'item_delete'
    ITEM_DOWNLOAD = 'item_download'
    ITEM_PREVIEW = 'item_preview'
    ITEM_RENAME = 'item_rename'
    ITEM_SHARE = 'item_share'
    ITEM_UPLOAD = 'item_upload'
    ITEM_READ = 'item_read'


class FileOrFolderScope(BaseObject):
    def __init__(
        self,
        *,
        scope: Optional[FileOrFolderScopeScopeField] = None,
        object: Optional[Union[FolderMini, FileMini]] = None,
        **kwargs
    ):
        """
        :param scope: The scopes for the resource access., defaults to None
        :type scope: Optional[FileOrFolderScopeScopeField], optional
        """
        super().__init__(**kwargs)
        self.scope = scope
        self.object = object
