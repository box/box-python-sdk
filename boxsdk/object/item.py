# coding: utf-8

from __future__ import unicode_literals

import json

from .base_object import BaseObject
from boxsdk.config import API
from boxsdk.exception import BoxAPIException


class Item(BaseObject):
    """Box API endpoint for interacting with files and folders."""

    def _get_accelerator_upload_url(self, file_id=None):
        """
        Make an API call to get the Accelerator upload url for either upload a new file or updating an existing file.

        :param file_id:
            Box id of the file to be uploaded. Not required for new file uploads.
        :type file_id:
            `unicode` or None
        :return:
            The Accelerator upload url or None if cannot get the Accelerator upload url.
        :rtype:
            `unicode` or None
        """
        endpoint = '{0}/content'.format(file_id) if file_id else 'content'
        url = '{0}/files/{1}'.format(API.BASE_API_URL, endpoint)
        try:
            response_json = self._session.options(
                url=url,
                expect_json_response=True,
            ).json()
            return response_json.get('upload_url', None)
        except BoxAPIException:
            return None

    def _preflight_check(self, size, name=None, file_id=None, parent_id=None):
        """
        Make an API call to check if certain file can be uploaded to Box or not.
        (https://box-content.readme.io/reference#preflight-check)

        :param size:
            The size of the file to be uploaded in bytes. Specify 0 for unknown file sizes.
        :type size:
            `int`
        :param name:
            The name of the file to be uploaded. This is optional if `file_id` is specified,
            but required for new file uploads.
        :type name:
            `unicode`
        :param file_id:
            Box id of the file to be uploaded. Not required for new file uploads.
        :type file_id:
            `unicode`
        :param parent_id:
            The ID of the parent folder. Required only for new file uploads.
        :type parent_id:
            `unicode`
        :raises:
            :class:`BoxAPIException` when preflight check fails.
        """
        endpoint = '{0}/content'.format(file_id) if file_id else 'content'
        url = '{0}/files/{1}'.format(API.BASE_API_URL, endpoint)
        data = {'size': size}
        if name:
            data['name'] = name
        if parent_id:
            data['parent'] = {'id': parent_id}

        self._session.options(
            url=url,
            expect_json_response=False,
            data=json.dumps(data),
        )

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

    def create_shared_link(
            self,
            access=None,
            etag=None,
            unshared_at=None,
            allow_download=None,
            allow_preview=None,
            password=None,
    ):
        """
        Create a shared link for the item with the given access permissions.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :type access:
            `unicode` or None
        :param etag:
            If specified, instruct the Box API to create the link only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :param unshared_at:
            The date on which this link should be disabled. May only be set if the current user is not a free user
            and has permission to set expiration dates.
        :type unshared_at:
            :class:`datetime.date` or None
        :param allow_download:
            Whether or not the item being shared can be downloaded when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :type allow_download:
            `bool` or None
        :param allow_preview:
            Whether or not the item being shared can be previewed when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :type allow_preview:
            `bool` or None
        :param password:
            The password required to view this link. If no password is specified then no password will be set.
            Please notice that this is a premium feature, which might not be available to your app.
        :type password:
            `unicode` or None
        :return:
            The updated object with s shared link.
            Returns a new object of the same type, without modifying the original object passed as self.
        :rtype:
            :class:`Item`
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        data = {
            'shared_link': {} if not access else {
                'access': access
            }
        }

        if unshared_at is not None:
            data['shared_link']['unshared_at'] = unshared_at.isoformat()

        if allow_download is not None or allow_preview is not None:
            data['shared_link']['permissions'] = permissions = {}
            if allow_download is not None:
                permissions['can_download'] = allow_download
            if allow_preview is not None:
                permissions['can_preview'] = allow_preview

        if password is not None:
            data['shared_link']['password'] = password

        return self.update_info(data, etag=etag)

    def get_shared_link(
            self,
            access=None,
            etag=None,
            unshared_at=None,
            allow_download=None,
            allow_preview=None,
            password=None,
    ):
        """
        Get a shared link for the item with the given access permissions.
        This url leads to a Box.com shared link page, where the item can be previewed, downloaded, etc.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :type access:
            `unicode` or None
        :param etag:
            If specified, instruct the Box API to create the link only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :param unshared_at:
            The date on which this link should be disabled. May only be set if the current user is not a free user
            and has permission to set expiration dates.
        :type unshared_at:
            :class:`datetime.date` or None
        :param allow_download:
            Whether or not the item being shared can be downloaded when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :type allow_download:
            `bool` or None
        :param allow_preview:
            Whether or not the item being shared can be previewed when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :type allow_preview:
            `bool` or None
        :param password:
            The password required to view this link. If no password is specified then no password will be set.
            Please notice that this is a premium feature, which might not be available to your app.
        :type password:
            `unicode` or None
        :returns:
            The URL of the shared link.
        :rtype:
            `unicode`
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        item = self.create_shared_link(
            access=access,
            etag=etag,
            unshared_at=unshared_at,
            allow_download=allow_download,
            allow_preview=allow_preview,
            password=password,
        )
        return item.shared_link['url']  # pylint:disable=no-member

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
        return item.shared_link is None  # pylint:disable=no-member

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
