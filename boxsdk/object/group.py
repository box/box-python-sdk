# coding: utf-8

from __future__ import unicode_literals, absolute_import
import json

from boxsdk.util.text_enum import TextEnum
from .base_object import BaseObject
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..util.api_call_decorator import api_call
from ..util.default_arg_value import SDK_VALUE_NOT_SET


class GroupRole(TextEnum):
    """The role in the group."""
    ADMIN = 'admin'
    MEMBER = 'member'


class Group(BaseObject):
    """Represents a Box group."""

    _item_type = 'group'

    @api_call
    def get_memberships(self, limit=None, offset=None, fields=None):
        """
        Get the membership records for the group, which indicate which users are included in the group.

        :param offset:
            The index at which to begin.
        :type offset:
            `int` or None
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
            return_full_pages=False,
        )

    @api_call
    def add_member(self, user, role=GroupRole.MEMBER, configurable_permissions=SDK_VALUE_NOT_SET):
        """
        Add the given user to this group under the given role

        :param user:
            The User to add to the group.
        :type user:
            :class:`User`
        :param role:
            The role for the user.
        :type role:
            `unicode`
        :param configurable_permissions:
            This is a group level permission that is configured for Group members with
            admin role only.
        :type configurable_permissons:
            `unicode` or None
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
        if configurable_permissions is not SDK_VALUE_NOT_SET:
            body_attributes['configurable_permissions'] = configurable_permissions
        box_response = self._session.post(url, data=json.dumps(body_attributes))
        response = box_response.json()
        return self.translator.translate(self._session, response)

    @api_call
    def get_collaborations(self, limit=None, offset=None, fields=None):
        """
        Get the entries in the collaboration for the group using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param offset:
            The offset of the item at which to begin the response.
        :type offset:
            `int` or None
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
        if fields is not None:
            additional_params['fields'] = ','.join(fields)
        return LimitOffsetBasedObjectCollection(
            session=self._session,
            url=self.get_url('collaborations'),
            additional_params=additional_params,
            limit=limit,
            offset=offset,
            return_full_pages=False,
        )
