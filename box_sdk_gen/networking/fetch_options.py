from __future__ import annotations

from typing import TYPE_CHECKING

from enum import Enum

from typing import Optional

from typing import Dict

from typing import List

if TYPE_CHECKING:
    from box_sdk_gen.networking.auth import Authentication

if TYPE_CHECKING:
    from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.internal.utils import ByteStream


class ResponseFormat(str, Enum):
    JSON = 'json'
    BINARY = 'binary'
    NO_CONTENT = 'no_content'


class MultipartItem:
    def __init__(
        self,
        part_name: str,
        *,
        data: Optional[SerializedData] = None,
        file_stream: Optional[ByteStream] = None,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ):
        """
        :param part_name: Name of the part
        :type part_name: str
        :param data: Data of the part, defaults to None
        :type data: Optional[SerializedData], optional
        :param file_stream: File stream of the part, defaults to None
        :type file_stream: Optional[ByteStream], optional
        :param file_name: File name of the part, defaults to None
        :type file_name: Optional[str], optional
        :param content_type: Content type of the part, defaults to None
        :type content_type: Optional[str], optional
        """
        self.part_name = part_name
        self.data = data
        self.file_stream = file_stream
        self.file_name = file_name
        self.content_type = content_type


class FetchOptions:
    def __init__(
        self,
        url: str,
        method: str,
        *,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[SerializedData] = None,
        file_stream: Optional[ByteStream] = None,
        multipart_data: Optional[List[MultipartItem]] = None,
        content_type: str = 'application/json',
        response_format: ResponseFormat = ResponseFormat.JSON,
        auth: Optional[Authentication] = None,
        network_session: Optional[NetworkSession] = None,
        follow_redirects: Optional[bool] = True,
    ):
        """
        :param url: URL of the request
        :type url: str
        :param method: HTTP verb of the request
        :type method: str
        :param params: HTTP query parameters, defaults to None
        :type params: Optional[Dict[str, str]], optional
        :param headers: HTTP headers, defaults to None
        :type headers: Optional[Dict[str, str]], optional
        :param data: Request body of the request, defaults to None
        :type data: Optional[SerializedData], optional
        :param file_stream: Stream data of the request, defaults to None
        :type file_stream: Optional[ByteStream], optional
        :param multipart_data: Multipart data of the request, defaults to None
        :type multipart_data: Optional[List[MultipartItem]], optional
        :param content_type: Content type of the request body, defaults to 'application/json'
        :type content_type: str, optional
        :param response_format: Expected response format, defaults to ResponseFormat.JSON
        :type response_format: ResponseFormat, optional
        :param auth: Authentication object, defaults to None
        :type auth: Optional[Authentication], optional
        :param network_session: Network session object, defaults to None
        :type network_session: Optional[NetworkSession], optional
        :param follow_redirects: A boolean value indicate if the request should follow redirects. Defaults to True. Not supported in Browser environment., defaults to True
        :type follow_redirects: Optional[bool], optional
        """
        self.url = url
        self.method = method
        self.params = params
        self.headers = headers
        self.data = data
        self.file_stream = file_stream
        self.multipart_data = multipart_data
        self.content_type = content_type
        self.response_format = response_format
        self.auth = auth
        self.network_session = network_session
        self.follow_redirects = follow_redirects
