# coding: utf-8
from typing import TYPE_CHECKING, Any
from .cloneable import Cloneable

if TYPE_CHECKING:
    from boxsdk.session.session import Session
    from boxsdk.util.translator import Translator


class BaseEndpoint(Cloneable):
    """A Box API endpoint."""

    def __init__(self, session: 'Session', **kwargs: Any):
        """
        :param session:
            The Box session used to make requests.
        :param kwargs:
            Keyword arguments for base class constructors.
        """
        super().__init__(**kwargs)
        self._session = session

    @property
    def session(self) -> 'Session':
        """
        Get the :class:`BoxSession` instance the object is using.
        """
        return self._session

    @property
    def translator(self) -> 'Translator':
        """
        The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.
        """
        return self._session.translator

    def get_url(self, *args: Any) -> str:
        """
        Return the URL used to access the endpoint.

        :param args:
            Parts of the endpoint URL.
        """
        return self._session.get_url(*args)

    def clone(self, session: 'Session' = None) -> 'BaseEndpoint':
        """
        Returns a copy of this cloneable object using the specified session.

        :param session:
            The Box session used to make requests.
        """
        return self.__class__(session or self._session)
