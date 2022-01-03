# coding: utf-8
from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from boxsdk.object.user import User
    from boxsdk.session.session import Session


class Cloneable:
    """
    Cloneable interface to be implemented by endpoint objects that should have ability to be cloned, but with a
    different session member if desired.
    """

    def as_user(self, user: 'User') -> 'Cloneable':
        """
        Returns a new endpoint object with default headers set up to make requests as the specified user.

        :param user:
            The user to impersonate when making API requests.
        """
        return self.clone(self.session.as_user(user))

    def with_shared_link(self, shared_link: str, shared_link_password: str) -> 'Cloneable':
        """
        Returns a new endpoint object with default headers set up to make requests using the shared link for auth.

        :param shared_link:
            The shared link.
        :param shared_link_password:
            The password for the shared link.
        """
        return self.clone(self.session.with_shared_link(shared_link, shared_link_password))

    def clone(self, session: 'Session' = None) -> NoReturn:
        """
        Returns a copy of this cloneable object using the specified session.

        :param session:
            The Box session used to make requests.
        """
        raise NotImplementedError

    @property
    def session(self) -> NoReturn:
        """
        Return the Box session being used to make requests.
        """
        raise NotImplementedError
