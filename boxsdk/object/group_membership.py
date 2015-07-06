# coding: utf-8

from __future__ import unicode_literals

from .base_object import BaseObject
from boxsdk.util.translator import Translator


class GroupMembership(BaseObject):
    """Represents a Box group_membership, which relates a user & group under a specific role."""

    _item_type = 'group_membership'

    def __init__(self, session, object_id, response_object=None, user=None, group=None):
        """
        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        :param object_id:
            The Box ID for the object.
        :type object_id:
            `unicode`
        :param response_object:
            The Box API response representing the object.
        :type response_object:
            :class:`BoxResponse`
        :param user:
            The User object, if any, associated with this group_membership instance.
        :type user:
            :class:`User`
        :param group:
            The Group object, if any, associated with this group_membership instance.
        :type group:
            :class:`Group`
        """
        user, group = self._init_user_and_group_instances(session, response_object, user, group)

        super(GroupMembership, self).__init__(session, object_id, response_object)

        self.user = user
        self.group = group

    @staticmethod
    def _init_user_and_group_instances(session, response_object, user, group):
        """
        Initialize User & Group instances based on the passed in parameters. This allows the GroupMembership
        instance to maintain a 'has-a' relationship with a corresponding User and Group instance.

        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        :param response_object:
            The Box API response representing the object.
        :type response_object:
            :class:`BoxResponse`
        :param user:
            The User object, if any, to associate with this group_membership instance.
        :type user:
            :class:`User`
        :param group:
            The Group object, if any, to associate with this group_membership instance.
        :type group:
            :class:`Group`
        """
        if not response_object:
            return user, group

        user_info = response_object.get('user')
        group_info = response_object.get('group')

        user = user or Translator().translate(user_info['type'])(session, user_info['id'], user_info)
        group = group or Translator().translate(group_info['type'])(session, group_info['id'], group_info)

        return user, group

    def as_user(self, user):
        """ Base class override. """
        return self.__class__(
            self._session.as_user(user),
            self._object_id,
            self._response_object,
            self.user,
            self.group,
        )

    def with_shared_link(self, shared_link, shared_link_password):
        """ Base class override. """
        return self.__class__(
            self._session.with_shared_link(shared_link, shared_link_password),
            self._object_id,
            self._response_object,
            self.user,
            self.group,
        )
