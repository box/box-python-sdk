from typing import Union

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.box.errors import BoxSDKError

Item = Union[FileFull, FolderMini, WebLink]
