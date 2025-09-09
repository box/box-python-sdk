from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.internal.utils import write_input_stream_to_output_stream

from box_sdk_gen.internal.utils import OutputStream


class DownloadsManager:
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

    def get_download_file_url(
        self,
        file_id: str,
        *,
        version: Optional[str] = None,
        access_token: Optional[str] = None,
        range: Optional[str] = None,
        boxapi: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> str:
        """
                Returns the contents of a file in binary format.
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param version: The file version to download., defaults to None
                :type version: Optional[str], optional
                :param access_token: An optional access token that can be used to pre-authenticate this request, which means that a download link can be shared with a browser or a third party service without them needing to know how to handle the authentication.
        When using this parameter, please make sure that the access token is sufficiently scoped down to only allow read access to that file and no other files or folders., defaults to None
                :type access_token: Optional[str], optional
                :param range: The byte range of the content to download.

        The format `bytes={start_byte}-{end_byte}` can be used to specify
        what section of the file to download., defaults to None
                :type range: Optional[str], optional
                :param boxapi: The URL, and optional password, for the shared link of this item.

        This header can be used to access items that have not been
        explicitly shared with a user.

        Use the format `shared_link=[link]` or if a password is required then
        use `shared_link=[link]&shared_link_password=[password]`.

        This header can be used on the file or folder shared, as well as on any files
        or folders nested within the item., defaults to None
                :type boxapi: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'version': to_string(version), 'access_token': to_string(access_token)}
        )
        headers_map: Dict[str, str] = prepare_params(
            {'range': to_string(range), 'boxapi': to_string(boxapi), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/files/',
                        to_string(file_id),
                        '/content',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
                follow_redirects=False,
            )
        )
        if 'location' in response.headers:
            return response.headers.get('location')
        if 'Location' in response.headers:
            return response.headers.get('Location')
        raise BoxSDKError(message='No location header in response')

    def download_file(
        self,
        file_id: str,
        *,
        version: Optional[str] = None,
        access_token: Optional[str] = None,
        range: Optional[str] = None,
        boxapi: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Optional[ByteStream]:
        """
                Returns the contents of a file in binary format.
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param version: The file version to download., defaults to None
                :type version: Optional[str], optional
                :param access_token: An optional access token that can be used to pre-authenticate this request, which means that a download link can be shared with a browser or a third party service without them needing to know how to handle the authentication.
        When using this parameter, please make sure that the access token is sufficiently scoped down to only allow read access to that file and no other files or folders., defaults to None
                :type access_token: Optional[str], optional
                :param range: The byte range of the content to download.

        The format `bytes={start_byte}-{end_byte}` can be used to specify
        what section of the file to download., defaults to None
                :type range: Optional[str], optional
                :param boxapi: The URL, and optional password, for the shared link of this item.

        This header can be used to access items that have not been
        explicitly shared with a user.

        Use the format `shared_link=[link]` or if a password is required then
        use `shared_link=[link]&shared_link_password=[password]`.

        This header can be used on the file or folder shared, as well as on any files
        or folders nested within the item., defaults to None
                :type boxapi: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        query_params_map: Dict[str, str] = prepare_params(
            {'version': to_string(version), 'access_token': to_string(access_token)}
        )
        headers_map: Dict[str, str] = prepare_params(
            {'range': to_string(range), 'boxapi': to_string(boxapi), **extra_headers}
        )
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/files/',
                        to_string(file_id),
                        '/content',
                    ]
                ),
                method='GET',
                params=query_params_map,
                headers=headers_map,
                response_format=ResponseFormat.BINARY,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        if to_string(response.status) == '202':
            return None
        return response.content

    def download_file_to_output_stream(
        self,
        file_id: str,
        output_stream: OutputStream,
        *,
        version: Optional[str] = None,
        access_token: Optional[str] = None,
        range: Optional[str] = None,
        boxapi: Optional[str] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param output_stream: Download file to a given output stream
                :type output_stream: OutputStream
                :param version: The file version to download., defaults to None
                :type version: Optional[str], optional
                :param access_token: An optional access token that can be used to pre-authenticate this request, which means that a download link can be shared with a browser or a third party service without them needing to know how to handle the authentication.
        When using this parameter, please make sure that the access token is sufficiently scoped down to only allow read access to that file and no other files or folders., defaults to None
                :type access_token: Optional[str], optional
                :param range: The byte range of the content to download.

        The format `bytes={start_byte}-{end_byte}` can be used to specify
        what section of the file to download., defaults to None
                :type range: Optional[str], optional
                :param boxapi: The URL, and optional password, for the shared link of this item.

        This header can be used to access items that have not been
        explicitly shared with a user.

        Use the format `shared_link=[link]` or if a password is required then
        use `shared_link=[link]&shared_link_password=[password]`.

        This header can be used on the file or folder shared, as well as on any files
        or folders nested within the item., defaults to None
                :type boxapi: Optional[str], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        download_stream: ByteStream = self.download_file(
            file_id,
            version=version,
            access_token=access_token,
            range=range,
            boxapi=boxapi,
            extra_headers=extra_headers,
        )
        write_input_stream_to_output_stream(download_stream, output_stream)
