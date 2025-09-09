from typing import Optional

from typing import Dict

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.internal.utils import ByteStream


class FetchResponse:
    def __init__(
        self,
        status: int,
        headers: Dict[str, str],
        *,
        url: Optional[str] = None,
        data: Optional[SerializedData] = None,
        content: Optional[ByteStream] = None
    ):
        """
        :param status: HTTP status code of the response
        :type status: int
        :param headers: HTTP headers of the response
        :type headers: Dict[str, str]
        :param url: URL of the response, defaults to None
        :type url: Optional[str], optional
        :param data: Response body of the response, defaults to None
        :type data: Optional[SerializedData], optional
        :param content: Streamed content of the response, defaults to None
        :type content: Optional[ByteStream], optional
        """
        self.status = status
        self.headers = headers
        self.url = url
        self.data = data
        self.content = content
