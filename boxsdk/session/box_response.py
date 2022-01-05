# coding: utf-8
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from boxsdk import NetworkResponse


class BoxResponse:
    """Represents a response to a Box API request."""

    def __init__(self, network_response):
        self._network_response = network_response

    def json(self) -> Any:
        """
        Return the parsed JSON response.
        """
        return self._network_response.json()

    @property
    def content(self) -> Any:
        """
        Return the content of the response body.
        """
        return self._network_response.content

    @property
    def ok(self) -> bool:
        """
        Return whether or not the request was successful.
        """
        # pylint:disable=invalid-name
        return self._network_response.ok

    @property
    def status_code(self) -> int:
        """
        Return the HTTP status code of the response.
        """
        return self._network_response.status_code

    @property
    def headers(self) -> dict:
        """
        Get the response headers.
        """
        return self._network_response.headers

    @property
    def network_response(self) -> 'NetworkResponse':
        """
        Return the underlying network response.
        """
        return self._network_response

    def __repr__(self) -> str:
        return f'<Box Response[{self.status_code}]>'
