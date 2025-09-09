from typing import List

from typing import Optional

from typing import Dict

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.internal.utils import Buffer

from box_sdk_gen.internal.utils import HashName

from box_sdk_gen.internal.utils import Iterator

from box_sdk_gen.schemas.upload_session import UploadSession

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.uploaded_part import UploadedPart

from box_sdk_gen.schemas.upload_parts import UploadParts

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.schemas.upload_part import UploadPart

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.internal.utils import generate_byte_stream_from_buffer

from box_sdk_gen.internal.utils import hex_to_base_64

from box_sdk_gen.internal.utils import iterate_chunks

from box_sdk_gen.internal.utils import read_byte_stream

from box_sdk_gen.internal.utils import reduce_iterator

from box_sdk_gen.internal.utils import Hash

from box_sdk_gen.internal.utils import buffer_length

from box_sdk_gen.schemas.file_full import FileFull


class _PartAccumulator:
    def __init__(
        self,
        last_index: int,
        parts: List[UploadPart],
        file_size: int,
        upload_part_url: str,
        file_hash: Hash,
    ):
        self.last_index = last_index
        self.parts = parts
        self.file_size = file_size
        self.upload_part_url = upload_part_url
        self.file_hash = file_hash


class ChunkedUploadsManager:
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

    def create_file_upload_session(
        self,
        folder_id: str,
        file_size: int,
        file_name: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UploadSession:
        """
        Creates an upload session for a new file.
        :param folder_id: The ID of the folder to upload the new file to.
        :type folder_id: str
        :param file_size: The total number of bytes of the file to be uploaded.
        :type file_size: int
        :param file_name: The name of new file.
        :type file_name: str
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'folder_id': folder_id,
            'file_size': file_size,
            'file_name': file_name,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.upload_url,
                        '/2.0/files/upload_sessions',
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
        return deserialize(response.data, UploadSession)

    def create_file_upload_session_for_existing_file(
        self,
        file_id: str,
        file_size: int,
        *,
        file_name: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UploadSession:
        """
                Creates an upload session for an existing file.
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param file_size: The total number of bytes of the file to be uploaded.
                :type file_size: int
                :param file_name: The optional new name of new file., defaults to None
                :type file_name: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'file_size': file_size, 'file_name': file_name}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.upload_url,
                        '/2.0/files/',
                        to_string(file_id),
                        '/upload_sessions',
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
        return deserialize(response.data, UploadSession)

    def get_file_upload_session_by_url(
        self, url: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UploadSession:
        """
        Using this method with urls provided in response when creating a new upload session is preferred to use over GetFileUploadSessionById method.

        This allows to always upload your content to the closest Box data center and can significantly improve upload speed.


         Return information about an upload session.


        The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions) endpoint.

        :param url: URL of getFileUploadSessionById method
        :type url: str
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=url,
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, UploadSession)

    def get_file_upload_session_by_id(
        self,
        upload_session_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UploadSession:
        """
                Return information about an upload session.

                The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions) endpoint.

                :param upload_session_id: The ID of the upload session.
        Example: "D5E3F7A"
                :type upload_session_id: str
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
                        self.network_session.base_urls.upload_url,
                        '/2.0/files/upload_sessions/',
                        to_string(upload_session_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, UploadSession)

    def upload_file_part_by_url(
        self,
        url: str,
        request_body: ByteStream,
        digest: str,
        content_range: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UploadedPart:
        """
                Using this method with urls provided in response when creating a new upload session is preferred to use over UploadFilePart method.

                This allows to always upload your content to the closest Box data center and can significantly improve upload speed.


                 Uploads a chunk of a file for an upload session.


                The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions)


                and [`Get upload session`](e://get-files-upload-sessions-id) endpoints.

                :param url: URL of uploadFilePart method
                :type url: str
                :param request_body: Request body of uploadFilePart method
                :type request_body: ByteStream
                :param digest: The [RFC3230][1] message digest of the chunk uploaded.

        Only SHA1 is supported. The SHA1 digest must be base64
        encoded. The format of this header is as
        `sha=BASE64_ENCODED_DIGEST`.

        To get the value for the `SHA` digest, use the
        openSSL command to encode the file part:
        `openssl sha1 -binary <FILE_PART_NAME> | base64`.

        [1]: https://tools.ietf.org/html/rfc3230
                :type digest: str
                :param content_range: The byte range of the chunk.

        Must not overlap with the range of a part already
        uploaded this session. Each part’s size must be
        exactly equal in size to the part size specified
        in the upload session that you created.
        One exception is the last part of the file, as this can be smaller.

        When providing the value for `content-range`, remember that:

        * The lower bound of each part's byte range
          must be a multiple of the part size.
        * The higher bound must be a multiple of the part size - 1.
                :type content_range: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {
                'digest': to_string(digest),
                'content-range': to_string(content_range),
                **extra_headers,
            }
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=url,
                method='PUT',
                headers=headers_map,
                file_stream=request_body,
                content_type='application/octet-stream',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, UploadedPart)

    def upload_file_part(
        self,
        upload_session_id: str,
        request_body: ByteStream,
        digest: str,
        content_range: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UploadedPart:
        """
                Uploads a chunk of a file for an upload session.

                The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions)


                and [`Get upload session`](e://get-files-upload-sessions-id) endpoints.

                :param upload_session_id: The ID of the upload session.
        Example: "D5E3F7A"
                :type upload_session_id: str
                :param request_body: Request body of uploadFilePart method
                :type request_body: ByteStream
                :param digest: The [RFC3230][1] message digest of the chunk uploaded.

        Only SHA1 is supported. The SHA1 digest must be base64
        encoded. The format of this header is as
        `sha=BASE64_ENCODED_DIGEST`.

        To get the value for the `SHA` digest, use the
        openSSL command to encode the file part:
        `openssl sha1 -binary <FILE_PART_NAME> | base64`.

        [1]: https://tools.ietf.org/html/rfc3230
                :type digest: str
                :param content_range: The byte range of the chunk.

        Must not overlap with the range of a part already
        uploaded this session. Each part’s size must be
        exactly equal in size to the part size specified
        in the upload session that you created.
        One exception is the last part of the file, as this can be smaller.

        When providing the value for `content-range`, remember that:

        * The lower bound of each part's byte range
          must be a multiple of the part size.
        * The higher bound must be a multiple of the part size - 1.
                :type content_range: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params(
            {
                'digest': to_string(digest),
                'content-range': to_string(content_range),
                **extra_headers,
            }
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.upload_url,
                        '/2.0/files/upload_sessions/',
                        to_string(upload_session_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                file_stream=request_body,
                content_type='application/octet-stream',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, UploadedPart)

    def delete_file_upload_session_by_url(
        self, url: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
        Using this method with urls provided in response when creating a new upload session is preferred to use over DeleteFileUploadSessionById method.

        This allows to always upload your content to the closest Box data center and can significantly improve upload speed.


         Abort an upload session and discard all data uploaded.


        This cannot be reversed.


        The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions)


        and [`Get upload session`](e://get-files-upload-sessions-id) endpoints.

        :param url: URL of deleteFileUploadSessionById method
        :type url: str
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=url,
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None

    def delete_file_upload_session_by_id(
        self,
        upload_session_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Abort an upload session and discard all data uploaded.

                This cannot be reversed.


                The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions)


                and [`Get upload session`](e://get-files-upload-sessions-id) endpoints.

                :param upload_session_id: The ID of the upload session.
        Example: "D5E3F7A"
                :type upload_session_id: str
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
                        self.network_session.base_urls.upload_url,
                        '/2.0/files/upload_sessions/',
                        to_string(upload_session_id),
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

    def get_file_upload_session_parts_by_url(
        self,
        url: str,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UploadParts:
        """
                Using this method with urls provided in response when creating a new upload session is preferred to use over GetFileUploadSessionParts method.

                This allows to always upload your content to the closest Box data center and can significantly improve upload speed.


                 Return a list of the chunks uploaded to the upload session so far.


                The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions)


                and [`Get upload session`](e://get-files-upload-sessions-id) endpoints.

                :param url: URL of getFileUploadSessionParts method
                :type url: str
                :param offset: The offset of the item at which to begin the response.

        Queries with offset parameter value
        exceeding 10000 will be rejected
        with a 400 response., defaults to None
                :type offset: Optional[int], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'offset': to_string(offset), 'limit': to_string(limit)}
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=url,
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, UploadParts)

    def get_file_upload_session_parts(
        self,
        upload_session_id: str,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> UploadParts:
        """
                Return a list of the chunks uploaded to the upload session so far.

                The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions)


                and [`Get upload session`](e://get-files-upload-sessions-id) endpoints.

                :param upload_session_id: The ID of the upload session.
        Example: "D5E3F7A"
                :type upload_session_id: str
                :param offset: The offset of the item at which to begin the response.

        Queries with offset parameter value
        exceeding 10000 will be rejected
        with a 400 response., defaults to None
                :type offset: Optional[int], optional
                :param limit: The maximum number of items to return per page., defaults to None
                :type limit: Optional[int], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'offset': to_string(offset), 'limit': to_string(limit)}
        )
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.upload_url,
                        '/2.0/files/upload_sessions/',
                        to_string(upload_session_id),
                        '/parts',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, UploadParts)

    def create_file_upload_session_commit_by_url(
        self,
        url: str,
        parts: List[UploadPart],
        digest: str,
        *,
        if_match: Optional[str] = None,
        if_none_match: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Optional[Files]:
        """
                Using this method with urls provided in response when creating a new upload session is preferred to use over CreateFileUploadSessionCommit method.

                This allows to always upload your content to the closest Box data center and can significantly improve upload speed.


                 Close an upload session and create a file from the uploaded chunks.


                The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions)


                and [`Get upload session`](e://get-files-upload-sessions-id) endpoints.

                :param url: URL of createFileUploadSessionCommit method
                :type url: str
                :param parts: The list details for the uploaded parts.
                :type parts: List[UploadPart]
                :param digest: The [RFC3230][1] message digest of the whole file.

        Only SHA1 is supported. The SHA1 digest must be Base64
        encoded. The format of this header is as
        `sha=BASE64_ENCODED_DIGEST`.

        [1]: https://tools.ietf.org/html/rfc3230
                :type digest: str
                :param if_match: Ensures this item hasn't recently changed before
        making changes.

        Pass in the item's last observed `etag` value
        into this header and the endpoint will fail
        with a `412 Precondition Failed` if it
        has changed since., defaults to None
                :type if_match: Optional[str], optional
                :param if_none_match: Ensures an item is only returned if it has changed.

        Pass in the item's last observed `etag` value
        into this header and the endpoint will fail
        with a `304 Not Modified` if the item has not
        changed since., defaults to None
                :type if_none_match: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'parts': parts}
        headers_map: Dict[str, str] = prepare_params(
            {
                'digest': to_string(digest),
                'if-match': to_string(if_match),
                'if-none-match': to_string(if_none_match),
                **extra_headers,
            }
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=url,
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        if to_string(response.status) == '202':
            return None
        return deserialize(response.data, Files)

    def create_file_upload_session_commit(
        self,
        upload_session_id: str,
        parts: List[UploadPart],
        digest: str,
        *,
        if_match: Optional[str] = None,
        if_none_match: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Optional[Files]:
        """
                Close an upload session and create a file from the uploaded chunks.

                The actual endpoint URL is returned by the [`Create upload session`](e://post-files-upload-sessions)


                and [`Get upload session`](e://get-files-upload-sessions-id) endpoints.

                :param upload_session_id: The ID of the upload session.
        Example: "D5E3F7A"
                :type upload_session_id: str
                :param parts: The list details for the uploaded parts.
                :type parts: List[UploadPart]
                :param digest: The [RFC3230][1] message digest of the whole file.

        Only SHA1 is supported. The SHA1 digest must be Base64
        encoded. The format of this header is as
        `sha=BASE64_ENCODED_DIGEST`.

        [1]: https://tools.ietf.org/html/rfc3230
                :type digest: str
                :param if_match: Ensures this item hasn't recently changed before
        making changes.

        Pass in the item's last observed `etag` value
        into this header and the endpoint will fail
        with a `412 Precondition Failed` if it
        has changed since., defaults to None
                :type if_match: Optional[str], optional
                :param if_none_match: Ensures an item is only returned if it has changed.

        Pass in the item's last observed `etag` value
        into this header and the endpoint will fail
        with a `304 Not Modified` if the item has not
        changed since., defaults to None
                :type if_none_match: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'parts': parts}
        headers_map: Dict[str, str] = prepare_params(
            {
                'digest': to_string(digest),
                'if-match': to_string(if_match),
                'if-none-match': to_string(if_none_match),
                **extra_headers,
            }
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.upload_url,
                        '/2.0/files/upload_sessions/',
                        to_string(upload_session_id),
                        '/commit',
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
        if to_string(response.status) == '202':
            return None
        return deserialize(response.data, Files)

    def _reducer(self, acc: _PartAccumulator, chunk: ByteStream) -> _PartAccumulator:
        last_index: int = acc.last_index
        parts: List[UploadPart] = acc.parts
        chunk_buffer: Buffer = read_byte_stream(chunk)
        hash: Hash = Hash(algorithm=HashName.SHA1)
        hash.update_hash(chunk_buffer)
        sha_1: str = hash.digest_hash('base64')
        digest: str = ''.join(['sha=', sha_1])
        chunk_size: int = buffer_length(chunk_buffer)
        bytes_start: int = last_index + 1
        bytes_end: int = last_index + chunk_size
        content_range: str = ''.join(
            [
                'bytes ',
                to_string(bytes_start),
                '-',
                to_string(bytes_end),
                '/',
                to_string(acc.file_size),
            ]
        )
        uploaded_part: UploadedPart = self.upload_file_part_by_url(
            acc.upload_part_url,
            generate_byte_stream_from_buffer(chunk_buffer),
            digest,
            content_range,
        )
        part: UploadPart = uploaded_part.part
        part_sha_1: str = hex_to_base_64(part.sha_1)
        assert part_sha_1 == sha_1
        assert part.size == chunk_size
        assert part.offset == bytes_start
        acc.file_hash.update_hash(chunk_buffer)
        return _PartAccumulator(
            last_index=bytes_end,
            parts=parts + [part],
            file_size=acc.file_size,
            upload_part_url=acc.upload_part_url,
            file_hash=acc.file_hash,
        )

    def upload_big_file(
        self, file: ByteStream, file_name: str, file_size: int, parent_folder_id: str
    ) -> FileFull:
        """
        Starts the process of chunk uploading a big file. Should return a File object representing uploaded file.
        :param file: The stream of the file to upload.
        :type file: ByteStream
        :param file_name: The name of the file, which will be used for storage in Box.
        :type file_name: str
        :param file_size: The total size of the file for the chunked upload in bytes.
        :type file_size: int
        :param parent_folder_id: The ID of the folder where the file should be uploaded.
        :type parent_folder_id: str
        """
        upload_session: UploadSession = self.create_file_upload_session(
            parent_folder_id, file_size, file_name
        )
        upload_part_url: str = upload_session.session_endpoints.upload_part
        commit_url: str = upload_session.session_endpoints.commit
        list_parts_url: str = upload_session.session_endpoints.list_parts
        part_size: int = upload_session.part_size
        total_parts: int = upload_session.total_parts
        assert part_size * total_parts >= file_size
        assert upload_session.num_parts_processed == 0
        file_hash: Hash = Hash(algorithm=HashName.SHA1)
        chunks_iterator: Iterator = iterate_chunks(file, part_size, file_size)
        results: _PartAccumulator = reduce_iterator(
            chunks_iterator,
            self._reducer,
            _PartAccumulator(
                last_index=-1,
                parts=[],
                file_size=file_size,
                upload_part_url=upload_part_url,
                file_hash=file_hash,
            ),
        )
        parts: List[UploadPart] = results.parts
        processed_session_parts: UploadParts = (
            self.get_file_upload_session_parts_by_url(list_parts_url)
        )
        assert processed_session_parts.total_count == total_parts
        sha_1: str = file_hash.digest_hash('base64')
        digest: str = ''.join(['sha=', sha_1])
        committed_session: Optional[Files] = (
            self.create_file_upload_session_commit_by_url(commit_url, parts, digest)
        )
        return committed_session.entries[0]
