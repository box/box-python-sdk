from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_request_update_request import (
    FileRequestUpdateRequestStatusField,
)

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.file_request_update_request import FileRequestUpdateRequest

from box_sdk_gen.box.errors import BoxSDKError


class FileRequestCopyRequestFolderTypeField(str, Enum):
    FOLDER = 'folder'


class FileRequestCopyRequestFolderField(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        id: str,
        *,
        type: Optional[FileRequestCopyRequestFolderTypeField] = None,
        **kwargs
    ):
        """
                :param id: The ID of the folder to associate the new
        file request to.
                :type id: str
                :param type: The value will always be `folder`., defaults to None
                :type type: Optional[FileRequestCopyRequestFolderTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class FileRequestCopyRequest(FileRequestUpdateRequest):
    def __init__(
        self,
        folder: FileRequestCopyRequestFolderField,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[FileRequestUpdateRequestStatusField] = None,
        is_email_required: Optional[bool] = None,
        is_description_required: Optional[bool] = None,
        expires_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
                :param folder: The folder to associate the new file request to.
                :type folder: FileRequestCopyRequestFolderField
                :param title: An optional new title for the file request. This can be
        used to change the title of the file request.

        This will default to the value on the existing file request., defaults to None
                :type title: Optional[str], optional
                :param description: An optional new description for the file request. This can be
        used to change the description of the file request.

        This will default to the value on the existing file request., defaults to None
                :type description: Optional[str], optional
                :param status: An optional new status of the file request.

        When the status is set to `inactive`, the file request
        will no longer accept new submissions, and any visitor
        to the file request URL will receive a `HTTP 404` status
        code.

        This will default to the value on the existing file request., defaults to None
                :type status: Optional[FileRequestUpdateRequestStatusField], optional
                :param is_email_required: Whether a file request submitter is required to provide
        their email address.

        When this setting is set to true, the Box UI will show
        an email field on the file request form.

        This will default to the value on the existing file request., defaults to None
                :type is_email_required: Optional[bool], optional
                :param is_description_required: Whether a file request submitter is required to provide
        a description of the files they are submitting.

        When this setting is set to true, the Box UI will show
        a description field on the file request form.

        This will default to the value on the existing file request., defaults to None
                :type is_description_required: Optional[bool], optional
                :param expires_at: The date after which a file request will no longer accept new
        submissions.

        After this date, the `status` will automatically be set to
        `inactive`.

        This will default to the value on the existing file request., defaults to None
                :type expires_at: Optional[DateTime], optional
        """
        super().__init__(
            title=title,
            description=description,
            status=status,
            is_email_required=is_email_required,
            is_description_required=is_description_required,
            expires_at=expires_at,
            **kwargs
        )
        self.folder = folder
