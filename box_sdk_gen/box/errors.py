import pprint
from datetime import datetime
from typing import Any, Dict, Optional

from ..internal.logging import DataSanitizer
from ..internal.errors import GeneratedCodeError


class BoxSDKError(GeneratedCodeError):
    def __init__(
        self,
        message: str,
        timestamp: Optional[datetime] = None,
        error: Optional[Exception] = None,
        **kwargs,
    ):
        super().__init__(message, **kwargs)
        self.name = 'BoxSDKError'
        self.message = message
        self.timestamp = timestamp if timestamp is not None else datetime.now()
        self.error = error

    def __str__(self):
        return ''.join(
            (
                f'\nTimestamp: {self.timestamp}',
                f'\nUnderlying error: {self.error}',
                f'\nMessage: {self.message}',
            )
        )


class RequestInfo:
    def __init__(
        self,
        method: str,
        url: str,
        query_params: Dict[str, str],
        headers: Dict[str, str],
        body: Optional[str] = None,
    ):
        self.method = method
        self.url = url
        self.query_params = query_params
        self.headers = headers
        self.body = body

    def print(self, data_sanitizer: DataSanitizer):
        return ''.join(
            (
                f'\n\tMethod: {self.method}',
                f'\n\tURL: {self.url}',
                f'\n\tQuery params: \n{pprint.pformat(self.query_params, indent=8)}',
                f'\n\tHeaders: \n{pprint.pformat(data_sanitizer.sanitize_headers(self.headers), indent=8)}',
                ''.join(
                    [
                        '\n\tBody: ',
                        '\n' if self.body else '',
                        pprint.pformat(self.body, indent=8),
                    ]
                ),
            )
        )


class ResponseInfo:
    def __init__(
        self,
        status_code: int,
        headers: Dict[str, str],
        body: Dict = None,
        raw_body: Optional[str] = None,
        code: Optional[str] = None,
        context_info: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
        help_url: Optional[str] = None,
    ):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.raw_body = raw_body
        self.code = code
        self.context_info = context_info
        self.request_id = request_id
        self.help_url = help_url

    def print(self, data_sanitizer: DataSanitizer):
        return ''.join(
            (
                f'\n\tStatus code: {self.status_code}',
                f'\n\tHeaders: \n{pprint.pformat(data_sanitizer.sanitize_headers(self.headers), indent=8)}',
                f'\n\tCode: {self.code}',
                f'\n\tContext Info: \n{pprint.pformat(self.context_info, indent=8)}',
                f'\n\tRequest Id: {self.request_id}',
                f'\n\tHelp Url: {self.help_url}',
                ''.join(
                    [
                        '\n\tBody: ',
                        '\n' if self.body else '',
                        pprint.pformat(
                            data_sanitizer.sanitize_body(self.body), indent=8
                        ),
                    ]
                ),
            )
        )


class BoxAPIError(BoxSDKError):
    def __init__(
        self,
        request_info: RequestInfo,
        response_info: ResponseInfo,
        message: str,
        timestamp: Optional[datetime] = None,
        error: Optional[str] = None,
        *,
        data_sanitizer: DataSanitizer = None,
        **kwargs,
    ):
        super().__init__(message=message, timestamp=timestamp, error=error, **kwargs)
        if data_sanitizer is None:
            data_sanitizer = DataSanitizer()
        self.name = 'BoxAPIError'
        self.request_info = request_info
        self.response_info = response_info
        self.data_sanitizer = data_sanitizer

    def __str__(self):
        return ''.join(
            [
                f'\t{super(BoxAPIError, self).__str__()}',
                f'\nRequest: {self.request_info.print(self.data_sanitizer)}',
                f'\nResponse: {self.response_info.print(self.data_sanitizer)}',
            ]
        )
