from typing import Optional

import attr

from ..util.log import sanitize_dictionary


@attr.s(slots=True)
class BoxRequest:
    """Represents a Box API request.

    :param url:                     The URL being requested.
    :param method:                  The HTTP method to use for the request.
    :param headers:                 HTTP headers to include with the request.
    :param auto_session_renewal:    Whether or not the session can be automatically renewed if the request fails.
    :param expect_json_response:    Whether or not the API response must be JSON.
    """
    url: str = attr.ib()
    method: Optional[str] = attr.ib(default='GET')
    headers: Optional[dict] = attr.ib(default=attr.Factory(dict))
    auto_session_renewal: Optional[bool] = attr.ib(default=True)
    expect_json_response: Optional[bool] = attr.ib(default=True)
    access_token: Optional[str] = attr.ib(default=None)

    def __repr__(self) -> str:
        return f'<BoxRequest for {self.method} {self.url} with headers {sanitize_dictionary(self.headers)}'
