# coding: utf-8

from abc import ABC, abstractmethod
from typing import Any, Callable, Union


class Network(ABC):
    """
    Abstract base class specifying the interface of the network layer.
    """

    @abstractmethod
    def request(self, method: str, url: str, access_token: str, **kwargs: Any) -> 'NetworkResponse':
        """
        Make a network request to the given url with the given method.

        :param method:
            The HTTP verb that should be used to make the request.
        :param url:
            The URL for the request.
        :param access_token:
            The OAuth2 access token used to authorize the request.
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def retry_after(self, delay: float, request_method: Callable, *args: Any, **kwargs: Any) -> 'NetworkResponse':
        """
        Make a network request after a given delay.

        :param delay:
            How long until the request should be executed.
        :param request_method:
            A callable that will execute the request.
        """
        raise NotImplementedError  # pragma: no cover

    @property
    def network_response_constructor(self) -> Union[type, Callable]:
        """The constructor to use for creating NetworkResponse instances.

        This is not implemented by default, and is not a required part of the
        interface.

        It is recommended that implementations of `request()` call this to
        construct their responses, rather than hard-coding the construction.
        That way, subclasses of the implementation can easily extend the
        construction of :class:`NetworkResponse` instances, by overriding this
        property, instead of needing to override `request()`.

        :return:
            A callable that returns an instance of :class:`NetworkResponse`.
            Most commonly, this will be a subclass of :class:`NetworkResponse`.
        """
        return NetworkResponse


class NetworkResponse(ABC):
    """Abstract base class specifying the interface for a network response."""

    @abstractmethod
    def json(self) -> Union[dict, list, str, int, float]:
        """
        Return the parsed JSON response.
        """
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def content(self) -> Any:
        """
        Return the content of the response body.
        """
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def status_code(self) -> int:
        """
        Return the HTTP status code of the response.
        """
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def ok(self) -> bool:
        """
        Return whether or not the request was successful.
        """
        # pylint:disable=invalid-name
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def headers(self) -> dict:
        """
        Return the response headers.
        """
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def response_as_stream(self) -> Any:
        """
        Return a stream containing the raw network response.
        """
        raise NotImplementedError  # pragma: no cover

    @property
    @abstractmethod
    def access_token_used(self) -> str:
        """
        Return the access token used to make the request.
        """
        raise NotImplementedError  # pragma: no cover
