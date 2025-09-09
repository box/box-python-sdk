import pytest
import json
from collections import OrderedDict
from io import BytesIO, RawIOBase, UnsupportedOperation, SEEK_SET
from unittest import mock
from unittest.mock import Mock, patch
from requests import Session, Response, RequestException

from box_sdk_gen import (
    NetworkSession,
    BoxAPIError,
    Authentication,
    BoxSDKError,
    BoxClient,
    ResponseFormat,
    DataSanitizer,
)
from box_sdk_gen.networking.box_network_client import (
    BoxNetworkClient,
    USER_AGENT_HEADER,
    X_BOX_UA_HEADER,
    APIRequest,
    APIResponse,
)
from box_sdk_gen.networking import (
    FetchOptions,
    MultipartItem,
    FetchResponse,
    BoxRetryStrategy,
)
from box_sdk_gen.networking.proxy_config import ProxyConfig


@pytest.fixture
def mock_requests_session():
    return Mock(Session)


@pytest.fixture
def mock_byte_stream():
    return BytesIO(b"123")


@pytest.fixture
def mock_non_seekable_stream():
    return NonSeekableStream(b"123")


class NonSeekableStream(RawIOBase):
    def __init__(self, data: bytes):
        self._buffer = BytesIO(data)

    def read(self, size=-1):
        return self._buffer.read(size)

    def seekable(self) -> bool:
        return False

    def seek(self, offset, whence=SEEK_SET):
        raise UnsupportedOperation("Stream is not seekable")


@pytest.fixture
def response_202():
    response = Mock(Response)
    response.url = 'https://example.com'
    response.status_code = 202
    response.ok = True
    response.text = ""
    response.content = None
    response.headers = {
        "content-type": "text/html",
    }
    return response


@pytest.fixture
def response_202_with_retry_after():
    response = Mock(Response)
    response.url = 'https://example.com'
    response.status_code = 202
    response.ok = True
    response.text = ""
    response.content = b''
    response.headers = {"Retry-After": "0"}
    return response


@pytest.fixture
def response_500():
    response = Mock(Response)
    response.url = 'https://example.com'
    response.status_code = 500
    response.ok = False
    response.text = ""
    response.content = b''
    response.headers = {"Retry-After": "0"}
    return response


@pytest.fixture
def response_401():
    response = Mock(Response)
    response.url = 'https://example.com'
    response.status_code = 401
    response.ok = False
    response.text = ""
    response.content = b''
    response.headers = {}
    return response


@pytest.fixture
def response_429():
    response = Mock(Response)
    response.url = 'https://example.com'
    response.status_code = 429
    response.ok = False
    response.text = ""
    response.content = b''
    response.headers = {}
    return response


@pytest.fixture
def response_200():
    response = Mock(Response)
    response.url = 'https://example.com'
    response.status_code = 200
    response.ok = True
    response.headers = {}
    response.text = ""
    response.content = b''
    return response


@pytest.fixture
def response_302():
    response = Mock(Response)
    response.url = 'https://example.com'
    response.status_code = 302
    response.ok = True
    response.headers = {
        "location": "https://example.com/redirected",
        "content-length": "0",
    }
    response.text = ""
    response.content = b''
    return response


@pytest.fixture
def response_failure_no_status():
    response = Mock(Response)
    response.url = 'https://example.com'
    response.ok = False
    response.text = ""
    response.content = b''
    response.headers = {"Retry-After": "0"}
    return response


@pytest.fixture
def token_mock():
    return "token123"


@pytest.fixture
def token2_mock():
    return "new_token321"


@pytest.fixture
def network_session_mock():
    return NetworkSession()


@pytest.fixture
def network_client(mock_requests_session):
    return BoxNetworkClient(mock_requests_session)


@pytest.fixture
def data_sanitizer():
    return DataSanitizer()


def reauthenticate_mock(auth, token):
    auth.retrieve_authorization_header.return_value = f"Bearer {token}"


@pytest.fixture
def authentication_mock(token_mock, token2_mock):
    auth = Mock(Authentication)
    auth.retrieve_authorization_header.return_value = f"Bearer {token_mock}"
    auth.refresh_token = lambda network_session: reauthenticate_mock(auth, token2_mock)
    return auth


def test_use_session_and_max_attempts_from_network_session(
    network_client, mock_requests_session, response_500
):
    mock_requests_session.request.return_value = response_500

    network_session = NetworkSession(retry_strategy=BoxRetryStrategy(max_attempts=3))

    options = FetchOptions(
        url="https://example.com",
        method="GET",
        network_session=network_session,
    )

    with pytest.raises(BoxAPIError):
        network_client.fetch(options)

    assert mock_requests_session.request.call_count == 3


def test_use_default_session_and_max_attempts_when_network_session_not_provided(
    network_client, mock_requests_session, response_500, network_session_mock
):
    mock_requests_session.request.return_value = response_500
    with patch("requests.Session", return_value=mock_requests_session):
        options = FetchOptions(url="https://example.com", method="GET")

        with pytest.raises(BoxAPIError):
            network_client.fetch(options)

        assert mock_requests_session.request.call_count == 5


def test_prepare_headers(network_client, authentication_mock, token_mock):
    network_session = NetworkSession(additional_headers={"additional_header": "test"})
    options = FetchOptions(
        url="https://example.com",
        method="GET",
        network_session=network_session,
        headers={"header": "test"},
        auth=authentication_mock,
    )

    headers = network_client._prepare_headers(options)

    assert headers == {
        "Authorization": f"Bearer {token_mock}",
        "header": "test",
        "additional_header": "test",
        "User-Agent": USER_AGENT_HEADER,
        "X-Box-UA": X_BOX_UA_HEADER,
    }


def test_prepare_headers_reauthenticate(
    network_client, authentication_mock, token2_mock
):
    network_session = NetworkSession(additional_headers={"additional_header": "test"})
    options = FetchOptions(
        url="https://example.com",
        method="GET",
        network_session=network_session,
        headers={"header": "test"},
        auth=authentication_mock,
    )

    headers = network_client._prepare_headers(options, reauthenticate=True)

    assert headers == {
        "Authorization": f"Bearer {token2_mock}",
        "header": "test",
        "additional_header": "test",
        "User-Agent": USER_AGENT_HEADER,
        "X-Box-UA": X_BOX_UA_HEADER,
    }


@pytest.mark.parametrize(
    "content_type, data, expected_body",
    [
        ("application/json", {"key": "value"}, '{"key": "value"}'),
        ("application/json-patch+json", {"key": "value"}, '{"key": "value"}'),
        ("application/x-www-form-urlencoded", {"key": "value"}, "key=value"),
        ("multipart/form-data", mock_byte_stream, mock_byte_stream),
        ("application/octet-stream", mock_byte_stream, mock_byte_stream),
    ],
)
def test_prepare_body_valid_content_type(
    network_client, content_type, data, expected_body, mock_byte_stream
):
    body = network_client._prepare_body(content_type, data)
    assert body == expected_body


def test_prepare_body_invalid_content_type(network_client):
    with pytest.raises(Exception):
        network_client._prepare_body("invalid_content_type", {})


def test_prepare_json_request(network_client):
    options = FetchOptions(
        url="https://example.com",
        method="POST",
        data={"key": "value"},
        headers={"header": "test"},
        params={"param": "value"},
        content_type="application/json",
    )

    api_request = network_client._prepare_request(options=options)

    assert api_request == APIRequest(
        method="POST",
        url="https://example.com",
        headers={
            "header": "test",
            "User-Agent": USER_AGENT_HEADER,
            "X-Box-UA": X_BOX_UA_HEADER,
            "Content-Type": "application/json",
        },
        params={"param": "value"},
        data='{"key": "value"}',
    )


def test_prepare_multipart_request(network_client, mock_byte_stream):
    options = FetchOptions(
        url="https://example.com",
        method="POST",
        data={"key": "value"},
        content_type="multipart/form-data",
        multipart_data=[
            MultipartItem(part_name="attributes", data={"name": "file.pdf"}),
            MultipartItem(
                part_name="file", file_stream=mock_byte_stream, file_name="file.pdf"
            ),
        ],
    )

    api_request = network_client._prepare_request(options=options)

    assert api_request.method == "POST"
    assert api_request.url == "https://example.com"
    assert api_request.headers["User-Agent"] == USER_AGENT_HEADER
    assert api_request.headers["X-Box-UA"] == X_BOX_UA_HEADER
    assert api_request.headers["Content-Type"].startswith(
        "multipart/form-data; boundary="
    )
    assert api_request.params == {}
    assert api_request.data.fields == OrderedDict(
        [
            ("attributes", '{"name": "file.pdf"}'),
            ("file", ("file.pdf", mock_byte_stream, None)),
        ]
    )


def test_make_request(network_client, mock_requests_session, response_200):
    request_params = {
        "method": "POST",
        "url": "https://example.com",
        "headers": {
            "header": "test",
            "User-Agent": USER_AGENT_HEADER,
            "X-Box-UA": X_BOX_UA_HEADER,
            "Content-Type": "application/json",
        },
        "params": {"param": "value"},
        "data": '{"key": "value"}',
        "allow_redirects": True,
    }
    mock_requests_session.request.return_value = response_200
    api_request = APIRequest(**request_params)

    api_response = network_client._make_request(api_request)

    assert api_response == APIResponse(
        network_response=response_200,
        reauthentication_needed=False,
        raised_exception=None,
    )
    assert mock_requests_session.request.call_count == 1
    mock_requests_session.request.assert_called_once_with(
        **request_params, stream=True, timeout=(5, 60)
    )


def test_make_request_unauthorised(network_client, mock_requests_session, response_401):
    mock_requests_session.request.return_value = response_401
    api_request = APIRequest(
        "GET", "https://example.com", headers={}, params={}, data=""
    )
    api_response = network_client._make_request(api_request)

    assert api_response == APIResponse(
        network_response=response_401,
        reauthentication_needed=False,
        raised_exception=None,
    )
    assert mock_requests_session.request.call_count == 1


@pytest.mark.parametrize(
    "exc_message, expected_reauthentication_needed",
    [
        ("Connection cancelled", False),
        (
            "Connection broken: ConnectionResetError(54, 'Connection reset by peer')",
            False,
        ),
        (
            "SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:2396)')))",
            True,
        ),
    ],
)
def test_make_request_network_exception(
    network_client, mock_requests_session, exc_message, expected_reauthentication_needed
):
    requests_exception = RequestException(exc_message)
    mock_requests_session.request.side_effect = [requests_exception]
    api_request = APIRequest(
        "GET", "https://example.com", headers={}, params={}, data=""
    )
    api_response = network_client._make_request(api_request)

    assert api_response == APIResponse(
        network_response=None,
        reauthentication_needed=expected_reauthentication_needed,
        raised_exception=requests_exception,
    )


def test_fetch_successfully_retry_network_exception(
    network_client, mock_requests_session, network_session_mock, response_200
):
    requests_exception = RequestException("Connection cancelled")
    mock_requests_session.request.side_effect = [requests_exception, response_200]

    with patch("time.sleep"):
        response = network_client.fetch(
            FetchOptions(
                method="get",
                url="https://example.com",
                network_session=network_session_mock,
            )
        )
        assert response.status == 200


def test_fetch_retries_network_exception_max_attempts(
    network_client, mock_requests_session, network_session_mock
):
    requests_exception = RequestException("Connection cancelled")
    mock_requests_session.request.side_effect = [
        requests_exception,
        requests_exception,
        requests_exception,
    ]
    network_session_mock.retry_strategy = BoxRetryStrategy(max_retries_on_exception=2)

    with patch("time.sleep"):
        with pytest.raises(BoxSDKError, match="Connection cancelled"):
            network_client.fetch(
                FetchOptions(
                    method="get",
                    url="https://example.com",
                    network_session=network_session_mock,
                )
            )

    assert mock_requests_session.request.call_count == 3


def test_fetch_get_json_format_response_success(
    network_client, mock_requests_session, network_session_mock, response_200
):
    response_200.text = '{"id": "123456"}'
    mock_requests_session.request.return_value = response_200

    fetch_response = network_client.fetch(
        FetchOptions(
            method="get",
            url="https://example.com",
            network_session=network_session_mock,
            response_format=ResponseFormat.JSON,
        )
    )

    assert fetch_response.status == 200
    assert fetch_response.data == {"id": "123456"}
    assert fetch_response.headers == {}


def test_fetch_get_binary_format_response_success(
    network_client, mock_requests_session, network_session_mock, response_200
):
    content = b"binary data"
    response_200.iter_content.return_value = BytesIO(content)
    mock_requests_session.request.return_value = response_200

    fetch_response = network_client.fetch(
        FetchOptions(
            method="get",
            url="https://example.com",
            network_session=network_session_mock,
            response_format=ResponseFormat.BINARY,
        )
    )

    assert fetch_response.status == 200
    assert fetch_response.content.read() == content
    assert fetch_response.headers == {}


@pytest.mark.parametrize("retryable_status_code", [429, 500, 503])
def test_retryable_status_codes(
    network_client,
    mock_requests_session,
    network_session_mock,
    response_200,
    retryable_status_code,
    response_failure_no_status,
):
    response_failure_no_status.status_code = retryable_status_code
    response_200.text = '{"id": "123456"}'
    mock_requests_session.request.side_effect = [
        response_failure_no_status,
        response_failure_no_status,
        response_200,
    ]

    fetch_response = network_client.fetch(
        FetchOptions(
            method="get",
            url="https://example.com",
            network_session=network_session_mock,
        )
    )
    assert fetch_response.status == 200
    assert fetch_response.data == {"id": "123456"}
    assert mock_requests_session.request.call_count == 3


@pytest.mark.parametrize("retryable_status_code", [429, 500, 503])
def test_retryable_status_codes_with_invalid__response_body(
    network_client,
    mock_requests_session,
    network_session_mock,
    response_200,
    retryable_status_code,
    response_failure_no_status,
):
    response_failure_no_status.status_code = retryable_status_code
    response_failure_no_status.text = 'Invalid JSON'
    response_200.text = '{"id": "123456"}'
    mock_requests_session.request.side_effect = [
        response_failure_no_status,
        response_failure_no_status,
        response_200,
    ]

    fetch_response = network_client.fetch(
        FetchOptions(
            method="get",
            url="https://example.com",
            network_session=network_session_mock,
            response_format=ResponseFormat.JSON,
        )
    )
    assert fetch_response.status == 200
    assert fetch_response.data == {"id": "123456"}
    assert mock_requests_session.request.call_count == 3


def test_status_code_202_with_no_retry_after_header(
    network_client, mock_requests_session, network_session_mock, response_202
):
    mock_requests_session.request.return_value = response_202

    fetch_response = network_client.fetch(
        FetchOptions(
            method="get",
            url="https://example.com",
            network_session=network_session_mock,
        )
    )
    assert fetch_response.status == 202
    assert fetch_response.data == {}


def test_retryable_status_code_202(
    network_client,
    mock_requests_session,
    network_session_mock,
    response_202_with_retry_after,
    response_200,
):
    response_200.text = '{"id": "123456"}'
    response_200.headers = {"Retry-After": "0"}
    mock_requests_session.request.side_effect = [
        response_202_with_retry_after,
        response_202_with_retry_after,
        response_200,
    ]

    with patch("time.sleep"):
        fetch_response = network_client.fetch(
            FetchOptions(
                method="get",
                url="https://example.com",
                network_session=network_session_mock,
            )
        )

    assert fetch_response.status == 200
    assert fetch_response.data == {"id": "123456"}
    assert mock_requests_session.request.call_count == 3


def test_202_should_be_returned_if_retry_limit_is_reached(
    network_client,
    mock_requests_session,
    network_session_mock,
    response_202_with_retry_after,
):
    network_session_mock.MAX_ATTEMPTS = 5
    mock_requests_session.request.return_value = response_202_with_retry_after

    with patch("time.sleep"):
        fetch_response = network_client.fetch(
            FetchOptions(
                method="get",
                url="https://example.com",
                network_session=network_session_mock,
            )
        )

    assert fetch_response.status == 202
    assert fetch_response.data == {}


@pytest.mark.parametrize("not_retryable_status_code", [404, 403, 400])
def test_not_retryable_status_codes(
    network_client,
    mock_requests_session,
    network_session_mock,
    not_retryable_status_code,
    response_failure_no_status,
    response_200,
):
    response_failure_no_status.status_code = not_retryable_status_code
    mock_requests_session.request.side_effect = [
        response_failure_no_status,
        response_failure_no_status,
        response_200,
    ]

    with pytest.raises(BoxSDKError, match=f"Status code: {not_retryable_status_code}"):
        network_client.fetch(
            FetchOptions(
                method="get",
                url="https://example.com",
                network_session=network_session_mock,
            )
        )

    assert mock_requests_session.request.call_count == 1


def test_retrying_401_response_with_new_token_and_auth_provided(
    network_client,
    mock_requests_session,
    network_session_mock,
    response_401,
    response_200,
    authentication_mock,
    token_mock,
    token2_mock,
):
    response_200.text = '{"id": "123456"}'
    mock_requests_session.request.side_effect = [response_401, response_200]

    with patch("time.sleep"):
        fetch_response = network_client.fetch(
            FetchOptions(
                url="https://example.com",
                method="GET",
                network_session=network_session_mock,
                auth=authentication_mock,
            )
        )

    assert mock_requests_session.request.call_count == 2
    mock_requests_session.request.assert_has_calls(
        [
            mock.call(
                method="GET",
                url="https://example.com",
                headers={
                    "Authorization": f"Bearer {token_mock}",
                    "User-Agent": USER_AGENT_HEADER,
                    "X-Box-UA": X_BOX_UA_HEADER,
                    "Content-Type": "application/json",
                },
                params={},
                data=None,
                stream=True,
                allow_redirects=True,
                timeout=(5, 60),
            ),
            mock.call(
                method="GET",
                url="https://example.com",
                headers={
                    "Authorization": f"Bearer {token2_mock}",
                    "User-Agent": USER_AGENT_HEADER,
                    "X-Box-UA": X_BOX_UA_HEADER,
                    "Content-Type": "application/json",
                },
                params={},
                data=None,
                stream=True,
                allow_redirects=True,
                timeout=(5, 60),
            ),
        ],
    )
    assert fetch_response.status == 200
    assert fetch_response.data == {"id": "123456"}


def test_not_retrying_401_when_auth_not_provided(
    network_client,
    mock_requests_session,
    network_session_mock,
    response_401,
    response_200,
    authentication_mock,
):
    mock_requests_session.request.side_effect = [response_401, response_200]

    with pytest.raises(BoxSDKError, match="Status code: 401"):
        network_client.fetch(
            FetchOptions(
                url="https://example.com",
                method="GET",
                network_session=network_session_mock,
            )
        )

    assert mock_requests_session.request.call_count == 1
    mock_requests_session.request.assert_called_once_with(
        method="GET",
        url="https://example.com",
        headers={
            "User-Agent": USER_AGENT_HEADER,
            "X-Box-UA": X_BOX_UA_HEADER,
            "Content-Type": "application/json",
        },
        params={},
        data=None,
        stream=True,
        allow_redirects=True,
        timeout=(5, 60),
    )


def test_reaching_retry_limit(
    network_client,
    mock_requests_session,
    network_session_mock,
    response_202_with_retry_after,
):
    network_session_mock.MAX_ATTEMPTS = 5
    mock_requests_session.request.return_value = response_202_with_retry_after

    with pytest.raises(BoxSDKError, match="Status code: 202"):
        network_client.fetch(
            FetchOptions(
                method="get",
                url="https://example.com",
                network_session=network_session_mock,
            )
        )
    assert mock_requests_session.request.call_count == 5


def test_reaching_retry_limit(
    network_client, mock_requests_session, network_session_mock, response_500
):
    network_session_mock.MAX_ATTEMPTS = 5
    mock_requests_session.request.return_value = response_500

    with pytest.raises(BoxSDKError, match="Status code: 500"):
        network_client.fetch(
            FetchOptions(
                method="get",
                url="https://example.com",
                network_session=network_session_mock,
            )
        )
    assert mock_requests_session.request.call_count == 5


def test_get_retry_after_time_use_retry_after_header_value(network_session_mock):
    fetch_options = FetchOptions(
        url="example.com", method="GET", network_session=network_session_mock
    )
    fetch_response = FetchResponse(status=200, headers={'Retry-After': '213'})
    for attempt_number in range(1, 5):
        sleep_time = network_session_mock.retry_strategy.retry_after(
            fetch_options, fetch_response, attempt_number
        )
        assert sleep_time == 213


def test_get_retry_after_time_use_exponential_backoff(network_session_mock):
    fetch_options = FetchOptions(
        url="example.com", method="GET", network_session=network_session_mock
    )
    fetch_response = FetchResponse(status=200, headers={})
    for attempt_number in range(1, 5):
        sleep_time = network_session_mock.retry_strategy.retry_after(
            fetch_options, fetch_response, attempt_number
        )
        assert sleep_time > 0


def test_pass_retry_after_header_to_get_retry_after_time_method(
    network_client,
    mock_requests_session,
    network_session_mock,
    response_429,
    response_200,
):
    response_429.headers = {"Retry-After": "123"}
    mock_requests_session.request.side_effect = [response_429, response_200]

    with patch("time.sleep") as sleep_mock:
        network_client.fetch(
            FetchOptions(
                method="get",
                url="https://example.com",
                network_session=network_session_mock,
            )
        )
        assert mock_requests_session.request.call_count == 2
        sleep_mock.assert_called_once_with(123)


def test_raising_api_error_with_valid_json_body(network_client, data_sanitizer):
    client_error_response = Mock(Response)
    client_error_response.status_code = 400
    client_error_response.ok = False
    client_error_response.headers = {}
    client_error_response.text = """{
      "type": "error",
      "code": "item_name_invalid",
      "context_info": {
        "message": "Something went wrong."
      },
      "help_url": "https://developer.box.com/guides/api-calls/permissions-and-errors/common-errors/",
      "message": "Method Not Allowed",
      "request_id": "abcdef123456",
      "status": 400
    }"""
    client_error_response.json.return_value = json.loads(client_error_response.text)

    request = APIRequest(
        method="POST",
        url="https://example.com",
        headers={
            "header": "test",
            "User-Agent": USER_AGENT_HEADER,
            "X-Box-UA": X_BOX_UA_HEADER,
            "Content-Type": "application/json",
        },
        params={"param": "value"},
        data='{"key": "value"}',
    )

    response = APIResponse(
        network_response=client_error_response,
        reauthentication_needed=False,
        raised_exception=None,
    )
    try:
        network_client._raise_on_unsuccessful_request(request, response, data_sanitizer)
    except BoxAPIError as e:
        assert e.request_info.method == request.method
        assert e.request_info.url == request.url
        assert e.request_info.query_params == request.params
        assert e.request_info.headers == request.headers
        assert e.request_info.body == request.data

        assert e.response_info.status_code == client_error_response.status_code
        assert e.response_info.headers == client_error_response.headers
        assert e.response_info.body == {
            "type": "error",
            "code": "item_name_invalid",
            "context_info": {"message": "Something went wrong."},
            "help_url": (
                "https://developer.box.com/guides/api-calls/permissions-and-errors/common-errors/"
            ),
            "message": "Method Not Allowed",
            "request_id": "abcdef123456",
            "status": 400,
        }
        assert e.response_info.raw_body == client_error_response.text
        assert e.response_info.code == "item_name_invalid"
        assert e.response_info.context_info == {"message": "Something went wrong."}
        assert e.response_info.request_id == "abcdef123456"
        assert (
            e.response_info.help_url
            == "https://developer.box.com/guides/api-calls/permissions-and-errors/common-errors/"
        )

        assert e.message == "400 Method Not Allowed; Request ID: abcdef123456"
        assert e.error is None
        assert e.name == "BoxAPIError"


def test_sensitive_data_are_sanitized_from_box_api_error(
    network_client, data_sanitizer
):
    client_error_response = Mock(Response)
    client_error_response.status_code = 400
    client_error_response.ok = False
    client_error_response.headers = {'token': 'my_token'}
    client_error_response.text = """{
      "client_secret": "secret",
      "password": "change-me",
      "message": "Method Not Allowed",
      "request_id": "abcdef123456",
      "status": 400
    }"""
    client_error_response.json.return_value = json.loads(client_error_response.text)

    request = APIRequest(
        method="POST",
        url="https://example.com",
        headers={
            "header": "test",
            "User-Agent": USER_AGENT_HEADER,
            "X-Box-UA": X_BOX_UA_HEADER,
            "Content-Type": "application/json",
            "Authorization": "Bearer acbdef123456",
        },
        params={"param": "value"},
        data='{"key": "value"}',
    )

    response = APIResponse(
        network_response=client_error_response,
        reauthentication_needed=False,
        raised_exception=None,
    )
    try:
        network_client._raise_on_unsuccessful_request(request, response, data_sanitizer)
    except BoxAPIError as e:
        exception_message = str(e)
        assert "Authorization': '---[redacted]---'" in exception_message
        assert "client_secret': '---[redacted]---'" in exception_message
        assert "password': '---[redacted]---'" in exception_message
        assert "token': '---[redacted]---'" in exception_message
        assert "message': 'Method Not Allowed'" in exception_message


@pytest.mark.parametrize('response_body', ['', 'Invalid json', 123])
def test_raising_api_error_without_valid_json_body(
    network_client, response_body, data_sanitizer
):
    client_error_response = Mock(Response)
    client_error_response.status_code = 400
    client_error_response.ok = False
    client_error_response.headers = {}
    client_error_response.text = response_body

    request = APIRequest(
        method="POST",
        url="https://example.com",
        headers={
            "header": "test",
            "User-Agent": USER_AGENT_HEADER,
            "X-Box-UA": X_BOX_UA_HEADER,
            "Content-Type": "application/json",
        },
        params={"param": "value"},
        data='{"key": "value"}',
    )

    response = APIResponse(
        network_response=client_error_response,
        reauthentication_needed=False,
        raised_exception=None,
    )
    try:
        network_client._raise_on_unsuccessful_request(request, response, data_sanitizer)
    except BoxAPIError as e:
        assert e.request_info.method == request.method
        assert e.request_info.url == request.url
        assert e.request_info.query_params == request.params
        assert e.request_info.headers == request.headers
        assert e.request_info.body == request.data

        assert e.response_info.status_code == client_error_response.status_code
        assert e.response_info.headers == client_error_response.headers
        assert e.response_info.body == {}
        assert e.response_info.raw_body == client_error_response.text
        assert e.response_info.code is None
        assert e.response_info.context_info == {}
        assert e.response_info.request_id is None
        assert e.response_info.help_url is None

        assert e.error is None
        assert e.name == "BoxAPIError"


def test_raising_exception_raised_by_network_layer(network_client, data_sanitizer):
    requests_exception = RequestException("Something went wrong")
    request = APIRequest(
        method="POST",
        url="https://example.com",
        headers={
            "header": "test",
            "User-Agent": USER_AGENT_HEADER,
            "X-Box-UA": X_BOX_UA_HEADER,
            "Content-Type": "application/json",
        },
        params={"param": "value"},
        data='{"key": "value"}',
    )

    response = APIResponse(
        network_response=None,
        reauthentication_needed=False,
        raised_exception=requests_exception,
    )

    try:
        network_client._raise_on_unsuccessful_request(request, response, data_sanitizer)
    except BoxSDKError as e:
        assert e.message == "Something went wrong"
        assert e.error == requests_exception
        assert e.name == "BoxSDKError"


def test_proxy_config():
    client = BoxClient(auth=None).with_proxy(
        ProxyConfig(url="http://127.0.0.1:3128/", username="user", password="pass")
    )
    assert client.network_session.proxy_url == "http://user:pass@127.0.0.1:3128/"
    requests_session = client.network_session.network_client.requests_session
    assert requests_session.proxies["http"] == "http://user:pass@127.0.0.1:3128/"
    assert requests_session.proxies["https"] == "http://user:pass@127.0.0.1:3128/"


@pytest.mark.parametrize(
    "response_body, expected_json",
    [
        ('', {}),
        ('Invalid json', {}),
        (123, {}),
        ('{"name": "John"}', {'name': 'John'}),
    ],
)
def test_read_json_body(response_body, expected_json):
    assert BoxNetworkClient._read_json_body(response_body) == expected_json


def test_get_options_stream_position(network_client, mock_byte_stream):
    mock_byte_stream.seek(1)
    options = FetchOptions(
        url="https://example.com",
        method="POST",
        data={"key": "value"},
        file_stream=mock_byte_stream,
    )

    assert network_client._get_options_stream_position(options) == 1


def test_get_multipart_stream_position(network_client, mock_byte_stream):
    mock_byte_stream.seek(1)
    options = FetchOptions(
        url="https://example.com",
        method="POST",
        data={"key": "value"},
        content_type="multipart/form-data",
        multipart_data=[
            MultipartItem(part_name="attributes", data={"name": "file.pdf"}),
            MultipartItem(
                part_name="file", file_stream=mock_byte_stream, file_name="file.pdf"
            ),
        ],
    )

    assert network_client._get_multipart_stream_positions(options) == {"file": 1}


def test_get_multipart_stream_position_empty(network_client):
    options = FetchOptions(
        url="https://example.com",
        method="POST",
        data={"key": "value"},
        content_type="multipart/form-data",
        multipart_data=[
            MultipartItem(part_name="attributes", data={"name": "file.pdf"}),
        ],
    )

    assert network_client._get_multipart_stream_positions(options) == {}


def test_reset_options_stream(network_client, mock_byte_stream):
    options = FetchOptions(
        url="https://example.com",
        method="POST",
        data={"key": "value"},
        content_type="multipart/form-data",
        file_stream=mock_byte_stream,
    )

    mock_byte_stream.seek(1)
    original_position = network_client._get_options_stream_position(options)
    mock_byte_stream.seek(2)

    network_client._reset_options_stream(options, original_position, None)

    assert options.file_stream.tell() == 1


def test_reset_options_stream_non_seekable_stream(
    network_client, mock_non_seekable_stream
):
    options = FetchOptions(
        url="https://example.com",
        method="POST",
        data={"key": "value"},
        content_type="multipart/form-data",
        file_stream=mock_non_seekable_stream,
    )

    original_position = network_client._get_options_stream_position(options)

    with pytest.raises(BoxSDKError):
        network_client._reset_options_stream(options, original_position, None)


def test_reset_multipart_stream(network_client, mock_byte_stream):
    options = FetchOptions(
        url="https://example.com",
        method="POST",
        data={"key": "value"},
        content_type="multipart/form-data",
        multipart_data=[
            MultipartItem(part_name="attributes", data={"name": "file.pdf"}),
            MultipartItem(
                part_name="file", file_stream=mock_byte_stream, file_name="file.pdf"
            ),
        ],
    )

    mock_byte_stream.seek(1)
    original_positions = network_client._get_multipart_stream_positions(options)
    mock_byte_stream.seek(2)

    network_client._reset_multipart_streams(options, original_positions, None)

    assert options.multipart_data[1].file_stream.tell() == 1


def test_reset_multipart_non_seekable_stream(network_client, mock_non_seekable_stream):
    options = FetchOptions(
        url="https://example.com",
        method="POST",
        data={"key": "value"},
        content_type="multipart/form-data",
        multipart_data=[
            MultipartItem(part_name="attributes", data={"name": "file.pdf"}),
            MultipartItem(
                part_name="file",
                file_stream=mock_non_seekable_stream,
                file_name="file.pdf",
            ),
        ],
    )

    original_positions = network_client._get_multipart_stream_positions(options)

    with pytest.raises(BoxSDKError):
        network_client._reset_multipart_streams(options, original_positions, None)


def test_disable_follow_redirects(
    network_client,
    mock_requests_session,
    network_session_mock,
    response_302,
    response_200,
):
    mock_requests_session.request.side_effect = [response_302, response_200]

    network_client.fetch(
        FetchOptions(
            url="https://example.com",
            method="GET",
            network_session=network_session_mock,
            follow_redirects=False,
        )
    )

    assert mock_requests_session.request.call_count == 1
    mock_requests_session.request.assert_called_once_with(
        method="GET",
        url="https://example.com",
        headers={
            "User-Agent": USER_AGENT_HEADER,
            "X-Box-UA": X_BOX_UA_HEADER,
            "Content-Type": "application/json",
        },
        params={},
        data=None,
        stream=True,
        allow_redirects=False,
        timeout=(5, 60),
    )
