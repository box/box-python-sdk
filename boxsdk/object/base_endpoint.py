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

    def as_user(self, user):
        """
        Returns a new endpoint object with default headers set up to make requests as the specified user.

        :param user:
            The user to impersonate when making API requests.
        :type user:
            :class:`User`
        """
        return self.clone(self._session.as_user(user))

    def with_shared_link(self, shared_link, shared_link_password):
        """
        Returns a new endpoint object with default headers set up to make requests using the shared link for auth.

        :param shared_link:
            The shared link.
        :type shared_link:
            `unicode`
        :param shared_link_password:
            The password for the shared link.
        :type shared_link_password:
            `unicode`
        """
        return self.clone(self._session.with_shared_link(shared_link, shared_link_password))

    def clone(self, session=None):
        """
        Returns a copy of this cloneable object using the specified session.

        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        """
        return self.__class__(session or self._session)

