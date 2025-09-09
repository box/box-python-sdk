from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from typing import Optional

from box_sdk_gen.box.errors import BoxSDKError


class ZipDownloadRequestItemsTypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'


class ZipDownloadRequestItemsField(BaseObject):
    _discriminator = 'type', {'file', 'folder'}

    def __init__(self, type: ZipDownloadRequestItemsTypeField, id: str, **kwargs):
        """
                :param type: The type of the item to add to the archive.
                :type type: ZipDownloadRequestItemsTypeField
                :param id: The identifier of the item to add to the archive. When this item is
        a folder then this can not be the root folder with ID `0`.
                :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id


class ZipDownloadRequest(BaseObject):
    def __init__(
        self,
        items: List[ZipDownloadRequestItemsField],
        *,
        download_file_name: Optional[str] = None,
        **kwargs
    ):
        """
                :param items: A list of items to add to the `zip` archive. These can
        be folders or files.
                :type items: List[ZipDownloadRequestItemsField]
                :param download_file_name: The optional name of the `zip` archive. This name will be appended by the
        `.zip` file extension, for example `January Financials.zip`., defaults to None
                :type download_file_name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.items = items
        self.download_file_name = download_file_name
