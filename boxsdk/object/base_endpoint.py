# coding: utf-8

from __future__ import unicode_literals, absolute_import


class Cloneable(object):
    """
    Cloneable interface to be implemented by endpoint objects that should have ability to be cloned, but with a
    different session member if desired.
    """

    def __init__(self, *args, **kwargs):
        super(Cloneable, self).__init__(*args, **kwargs)

    def as_user(self, user):
        """
        Returns a new endpoint object with default headers set up to make requests as the specified user.
        :param user:
            The user to impersonate when making API requests.
        :type user:
            :class:`User`
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def clone(self, session=None):
        """
        Returns a copy of this cloneable object using the specified session.
        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        """
        raise NotImplementedError


class BaseEndpoint(object):
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
        return self.__class__(self._session.as_user(user))

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
        return self.__class__(self._session.with_shared_link(shared_link, shared_link_password))
