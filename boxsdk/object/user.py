# coding: utf-8

import json
from typing import TYPE_CHECKING, Optional, Iterable

from .base_object import BaseObject
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..util.api_call_decorator import api_call

if TYPE_CHECKING:
    from boxsdk.object.email_alias import EmailAlias
    from boxsdk.pagination.box_object_collection import BoxObjectCollection
    from boxsdk.object.folder import Folder
    from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment


class User(BaseObject):
    """Represents a Box user."""

    _item_type = 'user'

    @api_call
    def add_email_alias(self, email: str) -> 'EmailAlias':
        """
        Adds a new email alias to the given user's account.

        :param email:
            The email alias to add to the user.
        :returns:
            The new email alias object
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
    def get_email_aliases(self, limit: Optional[int] = None, fields: Iterable[str] = None) -> 'BoxObjectCollection':
        """
        Gets an list of email aliases for a user.

        :param limit:
            The maximum number of users to return. If not specified, the Box API will determine an appropriate limit.
        :param fields:
            List of fields to request
        :returns:
            An iterator of the user's email aliases
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
    def remove_email_alias(self, email_alias: 'EmailAlias') -> bool:
        """
        Remove an email alias from the user.

        :param email_alias:
            The email alias to remove.
        :returns:
            Whether the removal succeeded.
        """
        url = self.get_url('email_aliases', email_alias.object_id)
        response = self._session.delete(url, expect_json_response=False)
        return response.ok

    @api_call
    def transfer_content(
            self,
            destination_user: 'User',
            notify: Optional[bool] = None,
            fields: Iterable[str] = None
    ) -> 'Folder':
        """
        Move all of the items owned by a user into a new folder in another user's account.

        :param destination_user:
            The id of the user to transfer content to.
        :param notify:
            Whether the destination user should receive email notification of the transfer.
        :param fields:
            Fields to return on the resulting :class:`Folder` object
        :returns:
            A :class:`Folder` object that was transferred to another user.
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

    def get_storage_policy_assignment(self) -> 'StoragePolicyAssignment':
        """
        Get the storage policy assignment assigned to the user.

        :returns:
            The :class:`StoragePolicyAssignment` object information
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
    def get_group_memberships(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the entries in the user group membership using limit-offset paging.

        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param offset:
            The offset of the item at which to begin the response.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the groups
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
    def get_avatar(self) -> bytes:
        """
        Get the avatar for the User.

        :returns:
            Avatar content as bytes.
        """
        url = self.get_url('avatar')
        response = self._session.get(url, expect_json_response=False)
        return response.content

    @api_call
    def delete(self, *, notify: bool = True, force: bool = False, **kwargs) -> bool:
        # pylint: disable=arguments-differ,arguments-renamed
        """
        Delete a user's account.  This user will no longer be able to access Box.

        :param notify:
            Whether a notification should be sent about the deletion
        :param force:
            Whether the user should be deleted even if they still own files
        :returns:
            Whether the deletion succeeded
        """
        params = {
            'notify': notify,
            'force': force,
        }
        return super().delete(params=params, **kwargs)
