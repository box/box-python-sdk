# coding: utf-8

from __future__ import unicode_literals
from boxsdk.config import API


class BaseEndpoint(object):
    """A Box API endpoint."""

    def __init__(self, session):
        """

        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        """
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
        url = ['{0}/{1}'.format(API.BASE_API_URL, endpoint)]
        url.extend(['/{0}'.format(x) for x in args])
        return ''.join(url)

    def _get_kwargs_for_clone(self):
        """
        Returns a dictionary of arguments that can be passed to the constructor to create a clone of this object.

        :return:
            A dictionary that can be used as arguments when passed to this class's constructor.
        :rtype:
            {`unicode`: `unicode`}
        """
        return dict(session=self._session)

    def as_user(self, user):
        """
        Returns a new endpoint object with default headers set up to make requests as the specified user.

        :param user:
            The user to impersonate when making API requests.
        :type user:
            :class:`User`
        """
        kwargs = self._get_kwargs_for_clone()
        kwargs.update(session=self._session.as_user(user))
        return self.__class__(**kwargs)

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
        kwargs = self._get_kwargs_for_clone()
        kwargs.update(session=self._session.with_shared_link(shared_link, shared_link_password))
        return self.__class__(**kwargs)

    def async(self):
        """
        Returns a new endpoint object in non-blocking mode.
        """
        kwargs = self._get_kwargs_for_clone()
        kwargs.update(session=self._session.async())
        return self.__class__(**kwargs)
