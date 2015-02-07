# coding: utf-8

from __future__ import unicode_literals

import json

from .base_object import BaseObject


class Item(BaseObject):
    """Box API endpoint for interacting with files and folders."""

    def update_info(self, data, etag=None):
        """Baseclass override.

        :param etag:
            If specified, instruct the Box API to perform the update only if
            the current version's etag matches.
        :type etag:
            `unicode` or None
        :return:
            The updated object.
            Return a new object of the same type, without modifying the original object passed as self.
            Construct the new object with all the default attributes that are returned from the endpoint.
        :rtype:
            :class:`BaseObject`
        """
        # pylint:disable=arguments-differ
        headers = {'If-Match': etag} if etag is not None else None
        return super(Item, self).update_info(data, headers=headers)

    def rename(self, name):
        """
        Rename the item to a new name.

        :param name:
            The new name, you want the item to be renamed to.
        :type name:
            `unicode`
        """
        data = {
            'name': name,
        }
        return self.update_info(data)

    def get(self, fields=None, etag=None):
        """Base class override.

        :param etag:
            If specified, instruct the Box API to get the info only if the current version's etag doesn't match.
        :type etag:
            `unicode` or None
        :returns:
            Information about the file or folder.
        :rtype:
            `dict`
        :raises: :class:`BoxAPIException` if the specified etag matches the latest version of the item.
        """
        # pylint:disable=arguments-differ
        headers = {'If-None-Match': etag} if etag is not None else None
        return super(Item, self).get(fields=fields, headers=headers)

    def copy(self, parent_folder):
        """Copy the item to the given folder.

        :param parent_folder:
            The folder to which the item should be copied.
        :type parent_folder:
            :class:`Folder`
        """
        url = self.get_url('copy')
        data = {
            'parent': {'id': parent_folder.object_id}
        }
        box_response = self._session.post(url, data=json.dumps(data))
        response = box_response.json()
        return self.__class__(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )

    def move(self, parent_folder):
        """
        Move the item to the given folder.

        :param parent_folder:
            The parent `Folder` object, where the item will be moved to.
        :type parent_folder:
            `Folder`
        """
        data = {
            'parent': {'id': parent_folder.object_id}
        }
        return self.update_info(data)

    def get_shared_link(self, access=None, etag=None):
        """Get a shared link for the item with the given access permissions.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :type access:
            `unicode` or None
        :param etag:
            If specified, instruct the Box API to create the link only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :returns:
            The URL of the shared link.
        :rtype:
            `unicode`
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        data = {
            'shared_link': {} if not access else {
                'access': access
            }
        }
        item = self.update_info(data, etag=etag)
        return item.shared_link['url']

    def remove_shared_link(self, etag=None):
        """Delete the shared link for the item.

        :param etag:
            If specified, instruct the Box API to delete the link only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :returns:
            Whether or not the update was successful.
        :rtype:
            `bool`
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        data = {'shared_link': None}
        item = self.update_info(data, etag=etag)
        return item.shared_link['url']

    def delete(self, params=None, etag=None):
        """Delete the item.

        :param params:
            Additional parameters to send with the request.
        :type params:
            `dict`
        :param etag:
            If specified, instruct the Box API to delete the item only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :returns:
            Whether or not the delete was successful.
        :rtype:
            `bool`
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        headers = {'If-Match': etag} if etag is not None else None
        return super(Item, self).delete(params, headers)
