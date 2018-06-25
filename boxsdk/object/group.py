# coding: utf-8

from __future__ import unicode_literals, absolute_import
import json

from .base_object import BaseObject
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..util.api_call_decorator import api_call


class Group(BaseObject):
    """Represents a Box group."""

    _item_type = 'group'

    @api_call
    def get_memberships(self, offset=0, limit=None, fields=None):
        """
        Get the membership records for the group, which indicate which users are included in the group.

        :param offset:
            The index at which to begin.
        :type offset:
            `int`
        :param limit:
            The maximum number of items to return in a page.
        :type limit:
            `int` or None
        :returns:
            The collection of membership objects for the group.
        :rtype:
            `Iterable` of :class:`GroupMembership`
        """
        url = self.get_url('memberships')
        return LimitOffsetBasedObjectCollection(
            self._session,
            url,
            limit=limit,
            offset=offset,
            fields=fields,
            return_full_pages=False
        )

    @api_call
    def add_member(self, user, role):
        """
        Add the given user to this group under the given role

        :param user:
            The User to add to the group.
        :type user:
            :class:`User`
        :param role:
            The role for the user. TODO: determine valid options and create an Enum.
        :type role:
            `unicode`
        :returns:
            The new GroupMembership instance.
        :rtype:
            :class:`GroupMembership`
        """
        url = self._session.get_url('group_memberships')
        body_attributes = {
            'user': {'id': user.object_id},
            'group': {'id': self.object_id},
            'role': role,
        }
        box_response = self._session.post(url, data=json.dumps(body_attributes))
        response = box_response.json()

        return self.translator.translate(response['type'])(self._session, response['id'], response, user=user, group=self)
