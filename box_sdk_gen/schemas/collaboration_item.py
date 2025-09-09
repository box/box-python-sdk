from typing import Union

from box_sdk_gen.schemas.file import File

from box_sdk_gen.schemas.folder import Folder

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.box.errors import BoxSDKError

CollaborationItem = Union[File, Folder, WebLink]
