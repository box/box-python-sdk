# coding: utf-8


import json
from typing import Optional, Iterable, TYPE_CHECKING

from boxsdk.util.text_enum import TextEnum
from .base_object import BaseObject
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..util.api_call_decorator import api_call
from ..util.default_arg_value import SDK_VALUE_NOT_SET

if TYPE_CHECKING:
    from boxsdk.object.group_membership import GroupMembership
    from boxsdk.object.user import User
    from boxsdk.pagination.box_object_collection import BoxObjectCollection


class GroupRole(TextEnum):
    """The role in the group."""
    ADMIN = 'admin'
    MEMBER = 'member'


class Group(BaseObject):
    """Represents a Box group."""

    _item_type = 'group'

    @api_call
    def get_memberships(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            fields: Optional[Iterable[str]] = None
    ) -> Iterable['GroupMembership']:
        """
        Get the membership records for the group, which indicate which users are included in the group.

        :param limit:
            The maximum number of items to return in a page.
        :param offset:
            The index at which to begin.
        :param fields:
            List of fields to request. If None, will return the default fields for the object.
        :returns:
            The collection of membership objects for the group.
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
    def add_member(
            self,
            user: 'User',
            role: GroupRole = GroupRole.MEMBER,
            configurable_permissions: Optional[str] = SDK_VALUE_NOT_SET
    ) -> 'GroupMembership':
        """
        Add the given user to this group under the given role

        :param user:
            The User to add to the group.
        :param role:
            The role for the user.
        :param configurable_permissions:
            This is a group level permission that is configured for Group members with
            admin role only.
        :returns:
            The new GroupMembership instance.
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
    def get_collaborations(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the collaboration for the group using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param offset:
            The offset of the item at which to begin the response.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the collaboration for the group.
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
