# coding: utf-8

from __future__ import unicode_literals, absolute_import


class Cloneable(object):
    """
    Cloneable interface to be implemented by endpoint objects that should have ability to be cloned, but with a
    different session member if desired.
    """

    def as_user(self, user):
        """
        Returns a new endpoint object with default headers set up to make requests as the specified user.

        :param user:
            The user to impersonate when making API requests.
        :type user:
            :class:`User`
        """
        return self.clone(self.session.as_user(user))

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
        return self.clone(self.session.with_shared_link(shared_link, shared_link_password))

    def clone(self, session=None):
        """
        Returns a copy of this cloneable object using the specified session.

        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        """
        raise NotImplementedError

    @property
    def session(self):
        """
        Return the Box session being used to make requests.

        :rtype:
            :class:`BoxSession`
        """
        raise NotImplementedError
