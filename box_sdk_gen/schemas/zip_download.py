from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ZipDownloadNameConflictsTypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'


class ZipDownloadNameConflictsField(BaseObject):
    _discriminator = 'type', {'file', 'folder'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[ZipDownloadNameConflictsTypeField] = None,
        original_name: Optional[str] = None,
        download_name: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The identifier of the item., defaults to None
                :type id: Optional[str], optional
                :param type: The type of this item., defaults to None
                :type type: Optional[ZipDownloadNameConflictsTypeField], optional
                :param original_name: Box Developer Documentation., defaults to None
                :type original_name: Optional[str], optional
                :param download_name: The new name of this item as it will appear in the
        downloaded `zip` archive., defaults to None
                :type download_name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.original_name = original_name
        self.download_name = download_name


class ZipDownload(BaseObject):
    def __init__(
        self,
        *,
        download_url: Optional[str] = None,
        status_url: Optional[str] = None,
        expires_at: Optional[DateTime] = None,
        name_conflicts: Optional[List[List[ZipDownloadNameConflictsField]]] = None,
        **kwargs
    ):
        """
                :param download_url: The URL that can be used to download the `zip` archive. A `Get` request to
        this URL will start streaming the items requested. By default, this URL
        is only valid for a few seconds, until the `expires_at` time, unless a
        download is started after which it is valid for the duration of the
        download.

        It is important to note that the domain and path of this URL might change
        between API calls, and therefore it's important to use this URL as-is., defaults to None
                :type download_url: Optional[str], optional
                :param status_url: The URL that can be used to get the status of the `zip` archive being
        downloaded. A `Get` request to this URL will return the number of files
        in the archive as well as the number of items already downloaded or
        skipped. By default, this URL is only valid for a few seconds, until the
        `expires_at` time, unless a download is started after which the URL is
        valid for 12 hours from the start of the download.

        It is important to note that the domain and path of this URL might change
        between API calls, and therefore it's important to use this URL as-is., defaults to None
                :type status_url: Optional[str], optional
                :param expires_at: The time and date when this archive will expire. After this time the
        `status_url` and `download_url` will return an error.

        By default, these URLs are only valid for a few seconds, unless a download
        is started after which the `download_url` is valid for the duration of the
        download, and the `status_url` is valid for 12 hours from the start of the
        download., defaults to None
                :type expires_at: Optional[DateTime], optional
                :param name_conflicts: A list of conflicts that occurred when trying to create the archive. This
        would occur when multiple items have been requested with the
        same name.

        To solve these conflicts, the API will automatically rename an item
        and return a mapping between the original item's name and its new
        name.

        For every conflict, both files will be renamed and therefore this list
        will always be a multiple of 2., defaults to None
                :type name_conflicts: Optional[List[List[ZipDownloadNameConflictsField]]], optional
        """
        super().__init__(**kwargs)
        self.download_url = download_url
        self.status_url = status_url
        self.expires_at = expires_at
        self.name_conflicts = name_conflicts
