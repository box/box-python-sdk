from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.internal.utils import DateTime

from box_sdk_gen.schemas.file_request import FileRequest

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.file_request_update_request import FileRequestUpdateRequest

from box_sdk_gen.schemas.file_request_copy_request import FileRequestCopyRequest

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData


class UpdateFileRequestByIdStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class CreateFileRequestCopyFolderTypeField(str, Enum):
    FOLDER = 'folder'


class CreateFileRequestCopyFolder(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        id: str,
        *,
        type: Optional[CreateFileRequestCopyFolderTypeField] = None,
        **kwargs
    ):
        """
                :param id: The ID of the folder to associate the new
        file request to.
                :type id: str
                :param type: The value will always be `folder`., defaults to None
                :type type: Optional[CreateFileRequestCopyFolderTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class CreateFileRequestCopyStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class FileRequestsManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_file_request_by_id(
        self,
        file_request_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FileRequest:
        """
                Retrieves the information about a file request.
                :param file_request_id: The unique identifier that represent a file request.

        The ID for any file request can be determined
        by visiting a file request builder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/filerequest/123`
        the `file_request_id` is `123`.
        Example: "123"
                :type file_request_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/file_requests/',
                        to_string(file_request_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, FileRequest)

    def update_file_request_by_id(
        self,
        file_request_id: str,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[UpdateFileRequestByIdStatus] = None,
        is_email_required: Optional[bool] = None,
        is_description_required: Optional[bool] = None,
        expires_at: Optional[DateTime] = None,
        if_match: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FileRequest:
        """
                Updates a file request. This can be used to activate or

                deactivate a file request.

                :param file_request_id: The unique identifier that represent a file request.

        The ID for any file request can be determined
        by visiting a file request builder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/filerequest/123`
        the `file_request_id` is `123`.
        Example: "123"
                :type file_request_id: str
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
                :type status: Optional[UpdateFileRequestByIdStatus], optional
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
                :param if_match: Ensures this item hasn't recently changed before
        making changes.

        Pass in the item's last observed `etag` value
        into this header and the endpoint will fail
        with a `412 Precondition Failed` if it
        has changed since., defaults to None
                :type if_match: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'title': title,
            'description': description,
            'status': status,
            'is_email_required': is_email_required,
            'is_description_required': is_description_required,
            'expires_at': expires_at,
        }
        headers_map: Dict[str, str] = prepare_params(
            {'if-match': to_string(if_match), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/file_requests/',
                        to_string(file_request_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, FileRequest)

    def delete_file_request_by_id(
        self,
        file_request_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a file request permanently.
                :param file_request_id: The unique identifier that represent a file request.

        The ID for any file request can be determined
        by visiting a file request builder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/filerequest/123`
        the `file_request_id` is `123`.
        Example: "123"
                :type file_request_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/file_requests/',
                        to_string(file_request_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def create_file_request_copy(
        self,
        file_request_id: str,
        folder: CreateFileRequestCopyFolder,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[CreateFileRequestCopyStatus] = None,
        is_email_required: Optional[bool] = None,
        is_description_required: Optional[bool] = None,
        expires_at: Optional[DateTime] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> FileRequest:
        """
                Copies an existing file request that is already present on one folder,

                and applies it to another folder.

                :param file_request_id: The unique identifier that represent a file request.

        The ID for any file request can be determined
        by visiting a file request builder in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/filerequest/123`
        the `file_request_id` is `123`.
        Example: "123"
                :type file_request_id: str
                :param folder: The folder to associate the new file request to.
                :type folder: CreateFileRequestCopyFolder
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
                :type status: Optional[CreateFileRequestCopyStatus], optional
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
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'folder': folder,
            'title': title,
            'description': description,
            'status': status,
            'is_email_required': is_email_required,
            'is_description_required': is_description_required,
            'expires_at': expires_at,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/file_requests/',
                        to_string(file_request_id),
                        '/copy',
                    ]
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, FileRequest)
