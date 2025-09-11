from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class UploadSessionTypeField(str, Enum):
    UPLOAD_SESSION = 'upload_session'


class UploadSessionSessionEndpointsField(BaseObject):
    def __init__(
        self,
        *,
        upload_part: Optional[str] = None,
        commit: Optional[str] = None,
        abort: Optional[str] = None,
        list_parts: Optional[str] = None,
        status: Optional[str] = None,
        log_event: Optional[str] = None,
        **kwargs
    ):
        """
        :param upload_part: The URL to upload parts to., defaults to None
        :type upload_part: Optional[str], optional
        :param commit: The URL used to commit the file., defaults to None
        :type commit: Optional[str], optional
        :param abort: The URL for used to abort the session., defaults to None
        :type abort: Optional[str], optional
        :param list_parts: The URL users to list all parts., defaults to None
        :type list_parts: Optional[str], optional
        :param status: The URL used to get the status of the upload., defaults to None
        :type status: Optional[str], optional
        :param log_event: The URL used to get the upload log from., defaults to None
        :type log_event: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.upload_part = upload_part
        self.commit = commit
        self.abort = abort
        self.list_parts = list_parts
        self.status = status
        self.log_event = log_event


class UploadSession(BaseObject):
    _discriminator = 'type', {'upload_session'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[UploadSessionTypeField] = None,
        session_expires_at: Optional[DateTime] = None,
        part_size: Optional[int] = None,
        total_parts: Optional[int] = None,
        num_parts_processed: Optional[int] = None,
        session_endpoints: Optional[UploadSessionSessionEndpointsField] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this session., defaults to None
                :type id: Optional[str], optional
                :param type: The value will always be `upload_session`., defaults to None
                :type type: Optional[UploadSessionTypeField], optional
                :param session_expires_at: The date and time when this session expires., defaults to None
                :type session_expires_at: Optional[DateTime], optional
                :param part_size: The  size in bytes that must be used for all parts of of the
        upload.

        Only the last part is allowed to be of a smaller size., defaults to None
                :type part_size: Optional[int], optional
                :param total_parts: The total number of parts expected in this upload session,
        as determined by the file size and part size., defaults to None
                :type total_parts: Optional[int], optional
                :param num_parts_processed: The number of parts that have been uploaded and processed
        by the server. This starts at `0`.

        When committing a file files, inspecting this property can
        provide insight if all parts have been uploaded correctly., defaults to None
                :type num_parts_processed: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.session_expires_at = session_expires_at
        self.part_size = part_size
        self.total_parts = total_parts
        self.num_parts_processed = num_parts_processed
        self.session_endpoints = session_endpoints
