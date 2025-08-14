from typing import Union

from box_sdk_gen.schemas.file_base import FileBase

from box_sdk_gen.schemas.folder_base import FolderBase

from box_sdk_gen.schemas.web_link_base import WebLinkBase

from box_sdk_gen.box.errors import BoxSDKError

AppItemAssociatedItem = Union[FileBase, FolderBase, WebLinkBase]
