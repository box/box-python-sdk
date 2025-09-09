from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class FileRequestTypeField(str, Enum):
    FILE_REQUEST = 'file_request'


class FileRequestStatusField(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class FileRequest(BaseObject):
    _discriminator = 'type', {'file_request'}

    def __init__(
        self,
        id: str,
        folder: FolderMini,
        created_at: DateTime,
        updated_at: DateTime,
        *,
        type: FileRequestTypeField = FileRequestTypeField.FILE_REQUEST,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[FileRequestStatusField] = None,
        is_email_required: Optional[bool] = None,
        is_description_required: Optional[bool] = None,
        expires_at: Optional[DateTime] = None,
        url: Optional[str] = None,
        etag: Optional[str] = None,
        created_by: Optional[UserMini] = None,
        updated_by: Optional[UserMini] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this file request.
                :type id: str
                :param created_at: The date and time when the file request was created.
                :type created_at: DateTime
                :param updated_at: The date and time when the file request was last updated.
                :type updated_at: DateTime
                :param type: The value will always be `file_request`., defaults to FileRequestTypeField.FILE_REQUEST
                :type type: FileRequestTypeField, optional
                :param title: The title of file request. This is shown
        in the Box UI to users uploading files.

        This defaults to title of the file request that was
        copied to create this file request., defaults to None
                :type title: Optional[str], optional
                :param description: The optional description of this file request. This is
        shown in the Box UI to users uploading files.

        This defaults to description of the file request that was
        copied to create this file request., defaults to None
                :type description: Optional[str], optional
                :param status: The status of the file request. This defaults
        to `active`.

        When the status is set to `inactive`, the file request
        will no longer accept new submissions, and any visitor
        to the file request URL will receive a `HTTP 404` status
        code.

        This defaults to status of file request that was
        copied to create this file request., defaults to None
                :type status: Optional[FileRequestStatusField], optional
                :param is_email_required: Whether a file request submitter is required to provide
        their email address.

        When this setting is set to true, the Box UI will show
        an email field on the file request form.

        This defaults to setting of file request that was
        copied to create this file request., defaults to None
                :type is_email_required: Optional[bool], optional
                :param is_description_required: Whether a file request submitter is required to provide
        a description of the files they are submitting.

        When this setting is set to true, the Box UI will show
        a description field on the file request form.

        This defaults to setting of file request that was
        copied to create this file request., defaults to None
                :type is_description_required: Optional[bool], optional
                :param expires_at: The date after which a file request will no longer accept new
        submissions.

        After this date, the `status` will automatically be set to
        `inactive`., defaults to None
                :type expires_at: Optional[DateTime], optional
                :param url: The generated URL for this file request. This URL can be shared
        with users to let them upload files to the associated folder., defaults to None
                :type url: Optional[str], optional
                :param etag: The HTTP `etag` of this file. This can be used in combination with
        the `If-Match` header when updating a file request. By providing that
        header, a change will only be performed on the  file request if the `etag`
        on the file request still matches the `etag` provided in the `If-Match`
        header., defaults to None
                :type etag: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.folder = folder
        self.created_at = created_at
        self.updated_at = updated_at
        self.type = type
        self.title = title
        self.description = description
        self.status = status
        self.is_email_required = is_email_required
        self.is_description_required = is_description_required
        self.expires_at = expires_at
        self.url = url
        self.etag = etag
        self.created_by = created_by
        self.updated_by = updated_by
