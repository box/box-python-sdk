# coding: utf-8
from __future__ import unicode_literals

import json

from .base_object import BaseObject
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'

    def add_email_alias(self, email):
        """
        Adds a new email alias to th given user's account.

        :param email:
            The email alias to add to the uer.
        :type email:
            `unicode`
        :returns:
            A :class:`EmailAlias` object.
        :rtype:
            :class:`EmailAlias`
        """
        url = self.get_url('email_aliases')
        body = {
            'email': email
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(response['type'])(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )

    def email_aliases(self, limit=None, marker=None, fields=None):
        """
        Gets an list of email aliases for a user.

        :param limit:
            The maximum number of users to return. If not specified, the Box API will determine an appropriate limit.
        :type limit:
            `int` or None
        :param marker:
            The index at which to start returning items.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries email alias
        :rtype:
            :class:`MarkerBasedObjectCollection`
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('email_aliases'),
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    def move_owned_items(self, owned_by_id, notify=None):
        """
        Move all of the items owned by a user into a new folder in another users account.

        :param owned_by_id:
            The id of the user to transfer content to.
        :type owned_by_id:
            `unicode`
        :param notify:
            Whether the destination user should receive email notification of the transfer.
        :type notify:
            `bool` or None
        :returns:
            A :class:`Folder` object that was transferred to another user.
        :rtype:
            :class:`Folder`
        """
        url = self.get_url('folders/0')
        body = {
            'owned_by': {
                'id': owned_by_id,
            }
        }
        response = self._session.put(url, data=json.dumps(body)).json()
        return self.translator.translate(response['type'])(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )

    def get_group_memberships(self, limit=None, offset=None, fields=None):
        """
        Get the entries in the user group membership using limit-offset paging.

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
            An iterator of the entries in the groups
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {}
        if fields is not None:
            additional_params['fields'] = ','.join(fields)
        return LimitOffsetBasedObjectCollection(
            session=self._session,
            url=self.get_url('memberships'),
            additional_params=additional_params,
            limit=limit,
            offset=offset,
            return_full_pages=False,
        )
