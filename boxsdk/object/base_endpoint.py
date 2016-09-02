# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .cloneable import Cloneable


class BaseEndpoint(Cloneable):
    """A Box API endpoint."""

    def __init__(self, session, **kwargs):
        """
        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        :param kwargs:
            Keyword arguments for base class constructors.
        :type kwargs:
            `dict`
        """
        super(BaseEndpoint, self).__init__(**kwargs)
        self._session = session

    @property
    def session(self):
        """
        Get the :class:`BoxSession` instance the object is using.

        :rtype:
            :class:`BoxSession`
        """
        return self._session

    @property
    def translator(self):
        """The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.

        :rtype:   :class:`Translator`
        """
        return self._session.translator

    def get_url(self, endpoint, *args):
        """
        Return the URL used to access the endpoint.

        :param endpoint:
            The name of the endpoint.
        :type endpoint:
            `url`
        :param args:
            Additional parts of the endpoint URL.
        :type args:
            `Iterable`
        :rtype:
            `unicode`
        """
        # pylint:disable=no-self-use
        return self._session.get_url(endpoint, *args)

    def clone(self, session=None):
        """
        Returns a copy of this cloneable object using the specified session.

        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        """
        return self.__class__(session or self._session)
