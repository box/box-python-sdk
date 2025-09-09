from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ZipDownloadStatusStateField(str, Enum):
    IN_PROGRESS = 'in_progress'
    FAILED = 'failed'
    SUCCEEDED = 'succeeded'


class ZipDownloadStatus(BaseObject):
    def __init__(
        self,
        *,
        total_file_count: Optional[int] = None,
        downloaded_file_count: Optional[int] = None,
        skipped_file_count: Optional[int] = None,
        skipped_folder_count: Optional[int] = None,
        state: Optional[ZipDownloadStatusStateField] = None,
        **kwargs
    ):
        """
                :param total_file_count: The total number of files in the archive., defaults to None
                :type total_file_count: Optional[int], optional
                :param downloaded_file_count: The number of files that have already been downloaded., defaults to None
                :type downloaded_file_count: Optional[int], optional
                :param skipped_file_count: The number of files that have been skipped as they could not be
        downloaded. In many cases this is due to permission issues that have
        surfaced between the creation of the request for the archive and the
        archive being downloaded., defaults to None
                :type skipped_file_count: Optional[int], optional
                :param skipped_folder_count: The number of folders that have been skipped as they could not be
        downloaded. In many cases this is due to permission issues that have
        surfaced between the creation of the request for the archive and the
        archive being downloaded., defaults to None
                :type skipped_folder_count: Optional[int], optional
                :param state: The state of the archive being downloaded., defaults to None
                :type state: Optional[ZipDownloadStatusStateField], optional
        """
        super().__init__(**kwargs)
        self.total_file_count = total_file_count
        self.downloaded_file_count = downloaded_file_count
        self.skipped_file_count = skipped_file_count
        self.skipped_folder_count = skipped_folder_count
        self.state = state
