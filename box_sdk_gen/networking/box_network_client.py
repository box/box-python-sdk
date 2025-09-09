import io

import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Optional, Dict, Union
from sys import version_info as py_version

import requests
from requests import RequestException, Session, Response
from requests_toolbelt import MultipartEncoder

from ..internal.logging import DataSanitizer
from .retries import BoxRetryStrategy
from ..networking.fetch_options import FetchOptions
from ..networking.fetch_response import FetchResponse
from ..box.errors import BoxAPIError, BoxSDKError, RequestInfo, ResponseInfo
from ..internal.utils import ByteStream, ResponseByteStream
from ..networking.network_client import NetworkClient
from ..serialization.json import (
    sd_to_json,
    sd_to_url_params,
    json_to_serialized_data,
)
from ..networking.version import __version__

SDK_VERSION = __version__
USER_AGENT_HEADER = f'box-python-generated-sdk-{SDK_VERSION}'
X_BOX_UA_HEADER = (
    f'agent=box-python-generated-sdk/{SDK_VERSION}; '
    f'env=python/{py_version.major}.{py_version.minor}.{py_version.micro}'
)


@dataclass
class APIRequest:
    method: str
    url: str
    headers: Dict[str, str]
    params: Dict[str, str]
    data: Optional[Union[str, ByteStream, MultipartEncoder]]
    allow_redirects: bool = True


@dataclass
class APIResponse:
    network_response: Optional[Response] = None
    reauthentication_needed: Optional[bool] = False
    raised_exception: Optional[Exception] = None

    def get_header(
        self, header_name: str, default_value: Optional[str] = None
    ) -> Optional[str]:
        try:
            return self.network_response.headers[header_name]
        except (ValueError, KeyError, AttributeError):
            return default_value


class BoxNetworkClient(NetworkClient):
    def __init__(self, requests_session: Optional[Session] = None):
        super().__init__()
        self.requests_session = requests_session or requests.Session()

    def fetch(self, options: 'FetchOptions') -> FetchResponse:
        retry_strategy = (
            options.network_session.retry_strategy
            if options.network_session
            else BoxRetryStrategy()
        )
        data_sanitizer = (
            options.network_session.data_sanitizer
            if options.network_session
            else DataSanitizer()
        )

        attempt_nr = 1
        number_of_retries_on_exception = 0
        response = APIResponse()

        options_stream_position = self._get_options_stream_position(options)
        multipart_streams_positions = self._get_multipart_stream_positions(options)

        while True:
            request: APIRequest = self._prepare_request(
                options=options, reauthenticate=response.reauthentication_needed
            )
            response: APIResponse = self._make_request(request=request)
            if response.network_response is not None:
                attempt_for_retry = attempt_nr
                network_response = response.network_response

                if options.response_format == 'binary':
                    fetch_response = FetchResponse(
                        url=network_response.url,
                        status=network_response.status_code,
                        headers=dict(response.network_response.headers),
                        content=ResponseByteStream(
                            response.network_response.iter_content(chunk_size=1024)
                        ),
                    )
                else:
                    fetch_response = FetchResponse(
                        url=network_response.url,
                        status=network_response.status_code,
                        headers=dict(response.network_response.headers),
                        data=(self._read_json_body(network_response.text)),
                        content=io.BytesIO(network_response.content),
                    )
            else:
                number_of_retries_on_exception += 1
                attempt_for_retry = number_of_retries_on_exception
                fetch_response = FetchResponse(status=0, headers={})

            attempt_nr += 1
            should_retry = retry_strategy.should_retry(
                fetch_options=options,
                fetch_response=fetch_response,
                attempt_number=attempt_for_retry,
            )

            if should_retry:
                self._reset_options_stream(
                    options, options_stream_position, response.raised_exception
                )
                self._reset_multipart_streams(
                    options, multipart_streams_positions, response.raised_exception
                )
                time.sleep(
                    retry_strategy.retry_after(
                        fetch_options=options,
                        fetch_response=fetch_response,
                        attempt_number=attempt_for_retry,
                    )
                )
                continue

            if 200 <= fetch_response.status < 400:
                return fetch_response
            break
        self._raise_on_unsuccessful_request(
            request=request, response=response, data_sanitizer=data_sanitizer
        )

    def _prepare_request(
        self, options: 'FetchOptions', reauthenticate: bool = False
    ) -> APIRequest:
        headers = self._prepare_headers(options, reauthenticate)
        params = options.params or {}
        data = self._prepare_body(
            options.content_type, options.file_stream or options.data
        )
        allow_redirects = options.follow_redirects

        if options.content_type:
            if options.content_type == 'multipart/form-data':
                fields = OrderedDict()
                for part in options.multipart_data:
                    if part.data:
                        fields[part.part_name] = sd_to_json(part.data)
                    else:
                        fields[part.part_name] = (
                            part.file_name or '',
                            part.file_stream,
                            part.content_type,
                        )

                multipart_stream = MultipartEncoder(fields)
                data = multipart_stream
                headers['Content-Type'] = multipart_stream.content_type
            else:
                headers['Content-Type'] = options.content_type

        return APIRequest(
            method=options.method,
            url=options.url,
            headers=headers,
            params=params,
            data=data,
            allow_redirects=allow_redirects,
        )

    @staticmethod
    def _prepare_headers(
        options: 'FetchOptions', reauthenticate: bool = False
    ) -> Dict[str, str]:
        headers = {}
        if options.network_session:
            headers.update(options.network_session.additional_headers)
        if options.headers:
            headers.update(options.headers)
        if options.auth:
            if reauthenticate:
                options.auth.refresh_token(network_session=options.network_session)
            headers['Authorization'] = options.auth.retrieve_authorization_header(
                network_session=options.network_session
            )

        headers['User-Agent'] = USER_AGENT_HEADER
        headers['X-Box-UA'] = X_BOX_UA_HEADER
        return headers

    @staticmethod
    def _prepare_body(
        content_type: str, data: Union[dict, ByteStream]
    ) -> Optional[Union[str, ByteStream]]:
        if (
            content_type == 'application/json'
            or content_type == 'application/json-patch+json'
        ):
            return sd_to_json(data) if data else None
        if content_type == 'application/x-www-form-urlencoded':
            return sd_to_url_params(data)
        if (
            content_type == 'multipart/form-data'
            or content_type == 'application/octet-stream'
        ):
            return data
        raise

    def _make_request(self, request: APIRequest) -> APIResponse:
        raised_exception = None
        reauthentication_needed = False
        default_timeout = (5, 60)  # connect, read timeout
        try:
            network_response = self.requests_session.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                data=request.data,
                params=request.params,
                allow_redirects=request.allow_redirects,
                stream=True,
                timeout=default_timeout,
            )
        except RequestException as request_exc:
            raised_exception = request_exc
            network_response = None

            if 'EOF occurred in violation of protocol' in str(request_exc):
                reauthentication_needed = True

        return APIResponse(
            network_response=network_response,
            reauthentication_needed=reauthentication_needed,
            raised_exception=raised_exception,
        )

    @staticmethod
    def _raise_on_unsuccessful_request(
        request: APIRequest, response: APIResponse, data_sanitizer: DataSanitizer
    ) -> None:
        if response.raised_exception:
            raise BoxSDKError(
                message=str(response.raised_exception), error=response.raised_exception
            )

        network_response = response.network_response
        response_json = BoxNetworkClient._read_json_body(network_response.text)

        raise BoxAPIError(
            message=f'{network_response.status_code} {response_json.get("message", "")}; Request ID: {response_json.get("request_id", "")}',
            request_info=RequestInfo(
                method=request.method,
                url=request.url,
                query_params=request.params,
                headers=request.headers,
                body=request.data,
            ),
            response_info=ResponseInfo(
                status_code=network_response.status_code,
                headers=dict(network_response.headers),
                body=response_json,
                raw_body=network_response.text,
                code=response_json.get("code", None),
                context_info=response_json.get("context_info", {}),
                request_id=response_json.get("request_id", None),
                help_url=response_json.get("help_url", None),
            ),
            data_sanitizer=data_sanitizer,
        )

    @staticmethod
    def _get_multipart_stream_positions(options: 'FetchOptions') -> dict:
        multipart_streams_positions = {}
        if options.multipart_data:
            for part in options.multipart_data:
                if part.file_stream and part.file_stream.seekable():
                    multipart_streams_positions[part.part_name] = (
                        part.file_stream.tell()
                    )
        return multipart_streams_positions

    @staticmethod
    def _get_options_stream_position(options: 'FetchOptions') -> int:
        filestream_position = 0
        if options.file_stream and options.file_stream.seekable():
            filestream_position = options.file_stream.tell()
        return filestream_position

    @staticmethod
    def _validate_seekable(stream: ByteStream, raised_exception: Optional[Exception]):
        if not stream.seekable():
            raise BoxSDKError(
                message='Request with non-seekable stream cannot be retried',
                error=raised_exception,
            )

    @staticmethod
    def _read_json_body(response_body: str) -> dict:
        if not response_body:
            return {}
        try:
            return json_to_serialized_data(response_body)
        except (ValueError, TypeError):
            return {}

    def _reset_stream(
        self,
        stream: ByteStream,
        original_position: int,
        raised_exception: Optional[Exception],
    ):
        self._validate_seekable(stream, raised_exception)
        stream.seek(original_position)

    def _reset_options_stream(
        self,
        options: 'FetchOptions',
        filestream_position: int,
        raised_exception: Optional[Exception],
    ):
        if options.file_stream:
            self._reset_stream(
                options.file_stream, filestream_position, raised_exception
            )

    def _reset_multipart_streams(
        self,
        options: 'FetchOptions',
        multipart_streams_positions: dict,
        raised_exception: Optional[Exception],
    ):
        if not options.multipart_data:
            return

        for part in options.multipart_data:
            if not part.file_stream:
                continue

            position = multipart_streams_positions.get(part.part_name)
            # we didn't get position before sending request hence the stream must be non-seekable
            if position is None:
                raise BoxSDKError(
                    message='Request with non-seekable stream cannot be retried',
                    error=raised_exception,
                )

            self._reset_stream(
                part.file_stream,
                multipart_streams_positions[part.part_name],
                raised_exception,
            )
