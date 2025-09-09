from enum import Enum

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from typing import List

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.metadatas import Metadatas

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.metadata_full import MetadataFull

from box_sdk_gen.schemas.metadata_error import MetadataError

from box_sdk_gen.schemas.metadata_instance_value import MetadataInstanceValue

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


class GetFileMetadataByIdScope(str, Enum):
    GLOBAL = 'global'
    ENTERPRISE = 'enterprise'


class CreateFileMetadataByIdScope(str, Enum):
    GLOBAL = 'global'
    ENTERPRISE = 'enterprise'


class UpdateFileMetadataByIdScope(str, Enum):
    GLOBAL = 'global'
    ENTERPRISE = 'enterprise'


class UpdateFileMetadataByIdRequestBodyOpField(str, Enum):
    ADD = 'add'
    REPLACE = 'replace'
    REMOVE = 'remove'
    TEST = 'test'
    MOVE = 'move'
    COPY = 'copy'


class UpdateFileMetadataByIdRequestBody(BaseObject):
    _fields_to_json_mapping: Dict[str, str] = {
        'from_': 'from',
        **BaseObject._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'from': 'from_',
        **BaseObject._json_to_fields_mapping,
    }

    def __init__(
        self,
        *,
        op: Optional[UpdateFileMetadataByIdRequestBodyOpField] = None,
        path: Optional[str] = None,
        value: Optional[MetadataInstanceValue] = None,
        from_: Optional[str] = None,
        **kwargs
    ):
        """
                :param op: The type of change to perform on the template. Some
        of these are hazardous as they will change existing templates., defaults to None
                :type op: Optional[UpdateFileMetadataByIdRequestBodyOpField], optional
                :param path: The location in the metadata JSON object
        to apply the changes to, in the format of a
        [JSON-Pointer](https://tools.ietf.org/html/rfc6901).

        The path must always be prefixed with a `/` to represent the root
        of the template. The characters `~` and `/` are reserved
        characters and must be escaped in the key., defaults to None
                :type path: Optional[str], optional
                :param from_: The location in the metadata JSON object to move or copy a value
        from. Required for `move` or `copy` operations and must be in the
        format of a [JSON-Pointer](https://tools.ietf.org/html/rfc6901)., defaults to None
                :type from_: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.op = op
        self.path = path
        self.value = value
        self.from_ = from_


class DeleteFileMetadataByIdScope(str, Enum):
    GLOBAL = 'global'
    ENTERPRISE = 'enterprise'


class FileMetadataManager:
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

    def get_file_metadata(
        self, file_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Metadatas:
        """
                Retrieves all metadata for a given file.
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
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
                        '/2.0/files/',
                        to_string(file_id),
                        '/metadata',
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Metadatas)

    def get_file_metadata_by_id(
        self,
        file_id: str,
        scope: GetFileMetadataByIdScope,
        template_key: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataFull:
        """
                Retrieves the instance of a metadata template that has been applied to a

                file.

                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param scope: The scope of the metadata template.
        Example: "global"
                :type scope: GetFileMetadataByIdScope
                :param template_key: The name of the metadata template.
        Example: "properties"
                :type template_key: str
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
                        '/2.0/files/',
                        to_string(file_id),
                        '/metadata/',
                        to_string(scope),
                        '/',
                        to_string(template_key),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataFull)

    def create_file_metadata_by_id(
        self,
        file_id: str,
        scope: CreateFileMetadataByIdScope,
        template_key: str,
        request_body: Dict,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataFull:
        """
                Applies an instance of a metadata template to a file.

                In most cases only values that are present in the metadata template


                will be accepted, except for the `global.properties` template which accepts


                any key-value pair.

                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param scope: The scope of the metadata template.
        Example: "global"
                :type scope: CreateFileMetadataByIdScope
                :param template_key: The name of the metadata template.
        Example: "properties"
                :type template_key: str
                :param request_body: Request body of createFileMetadataById method
                :type request_body: Dict
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
                        '/2.0/files/',
                        to_string(file_id),
                        '/metadata/',
                        to_string(scope),
                        '/',
                        to_string(template_key),
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
        return deserialize(response.data, MetadataFull)

    def update_file_metadata_by_id(
        self,
        file_id: str,
        scope: UpdateFileMetadataByIdScope,
        template_key: str,
        request_body: List[UpdateFileMetadataByIdRequestBody],
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> MetadataFull:
        """
                Updates a piece of metadata on a file.

                The metadata instance can only be updated if the template has already been


                applied to the file before. When editing metadata, only values that match


                the metadata template schema will be accepted.


                The update is applied atomically. If any errors occur during the


                application of the operations, the metadata instance will not be changed.

                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param scope: The scope of the metadata template.
        Example: "global"
                :type scope: UpdateFileMetadataByIdScope
                :param template_key: The name of the metadata template.
        Example: "properties"
                :type template_key: str
                :param request_body: Request body of updateFileMetadataById method
                :type request_body: List[UpdateFileMetadataByIdRequestBody]
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
                        '/2.0/files/',
                        to_string(file_id),
                        '/metadata/',
                        to_string(scope),
                        '/',
                        to_string(template_key),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json-patch+json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, MetadataFull)

    def delete_file_metadata_by_id(
        self,
        file_id: str,
        scope: DeleteFileMetadataByIdScope,
        template_key: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a piece of file metadata.
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param scope: The scope of the metadata template.
        Example: "global"
                :type scope: DeleteFileMetadataByIdScope
                :param template_key: The name of the metadata template.
        Example: "properties"
                :type template_key: str
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
                        '/2.0/files/',
                        to_string(file_id),
                        '/metadata/',
                        to_string(scope),
                        '/',
                        to_string(template_key),
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
