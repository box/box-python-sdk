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
        return LimitOffsetBasedObjectCollection(
            self._session,
            url=self.get_url('memberships'),
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

    def collaborations(self, offset=None, limit=None, fields=None):
        """
        Get the entries in the collaboration for the group using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param offset:
            The offset of the item at which to begin the response.
        :type offset:
            `str` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the collaboration for the group.
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {}
        if fields:
            additional_params['fields'] = ','.join(fields)
        return LimitOffsetBasedObjectCollection(
            session=self._session,
            url=self.get_url('collaborations'),
            additional_params=additional_params,
            limit=limit,
            offset=offset,
            return_full_pages=False
        )
