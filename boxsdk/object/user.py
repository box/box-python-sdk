# coding: utf-8
from __future__ import unicode_literals

import json

from .base_object import BaseObject
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'

    @api_call
    def add_email_alias(self, email):
        """
        Adds a new email alias to the given user's account.

        :param email:
            The email alias to add to the user.
        :type email:
            `unicode`
        :returns:
            The new email alias object
        :rtype:
            :class:`EmailAlias`
        """
        url = self.get_url('email_aliases')
        body = {
            'email': email,
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_email_aliases(self, limit=None, fields=None):
        """
        Gets an list of email aliases for a user.

        :param limit:
            The maximum number of users to return. If not specified, the Box API will determine an appropriate limit.
        :type limit:
            `int` or None
        :param fields:
            List of fields to request
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the user's email aliases
        :rtype:
            :class:`BoxObjectCollection`
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('email_aliases'),
            limit=limit,
            marker=None,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def remove_email_alias(self, email_alias):
        """
        Remove an email alias from the user.

        :param email_alias:
            The email alias to remove.
        :type email_alias:
            :class:`EmailAlias`
        :returns:
            Whether the removal succeeded.
        :rtype:
            `bool`
        """
        url = self.get_url('email_aliases', email_alias.object_id)
        response = self._session.delete(url, expect_json_response=False)
        return response.ok

    @api_call
    def transfer_content(self, destination_user, notify=None, fields=None):
        """
        Move all of the items owned by a user into a new folder in another user's account.

        :param destination_user:
            The id of the user to transfer content to.
        :type destination_user:
            :class:`User`
        :param notify:
            Whether the destination user should receive email notification of the transfer.
        :type notify:
            `bool` or None
        :param fields:
            Fields to return on the resulting :class:`Folder` object
        :type fields:
            `Iterable` of `unicode`
        :returns:
            A :class:`Folder` object that was transferred to another user.
        :rtype:
            :class:`Folder`
        """
        url = self.get_url('folders', '0')
        body = {
            'owned_by': {
                'id': destination_user.object_id,
            },
        }
        params = {}
        if notify is not None:
            params['notify'] = notify
        if fields is not None:
            params['fields'] = ','.join(fields)
        response = self._session.put(url, data=json.dumps(body), params=params).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    def get_storage_policy_assignment(self):
        """
        Get the storage policy assignment assigned to the user.

        :returns:
            The :class:`StoragePolicyAssignment` object information
        :rtype:
            :class:`StoragePolicyAssignment`
        """
        url = self._session.get_url('storage_policy_assignments')
        additional_params = {
            'resolved_for_type': self.object_type,
            'resolved_for_id': self.object_id,
        }
        box_response = self._session.get(url, params=additional_params)
        response = box_response.json()['entries'][0]
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
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

    @api_call
    def get_avatar(self):
        """
        Get the avatar for the User.

        :returns:
            Avatar content as bytes.
        :rtype:
            `bytes`
        """
        url = self.get_url('avatar')
        response = self._session.get(url, expect_json_response=False)
        return response.content

    @api_call
    def delete(self, notify=True, force=False):
        # pylint: disable=arguments-differ
        """
        Delete a user's account.  This user will no longer be able to access Box.

        :param notify:
            Whether a notification should be sent about the deletion
        :type notify:
            `bool`
        :param force:
            Whether the user should be deleted even if they still own files
        :returns:
            Whether the deletion succeeded
        :rtype:
            `bool`
        """
        params = {
            'notify': notify,
            'force': force,
        }
        return super(User, self).delete(params=params)
