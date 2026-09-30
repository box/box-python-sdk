from typing import Union

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.web_link_mini import WebLinkMini

from box_sdk_gen.box.errors import BoxSDKError

CollaborationItem = Union[FileMini, FolderMini, WebLinkMini]
