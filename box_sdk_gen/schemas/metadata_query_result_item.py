from typing import Union

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.box.errors import BoxSDKError

MetadataQueryResultItem = Union[FileFull, FolderFull]
