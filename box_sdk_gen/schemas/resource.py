from typing import Union

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.file_mini import FileMini

from box_sdk_gen.box.errors import BoxSDKError

Resource = Union[FolderMini, FileMini]
