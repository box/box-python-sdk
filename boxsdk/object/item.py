# coding: utf-8

from __future__ import unicode_literals, absolute_import
import json

from boxsdk.util.text_enum import TextEnum
from .base_object import BaseObject
from ..exception import (
    BoxAPIException,
    BoxValueError
)
from .metadata import Metadata
from ..util.api_call_decorator import api_call
from ..util.default_arg_value import SDK_VALUE_NOT_SET
from ..pagination.marker_based_dict_collection import MarkerBasedDictCollection
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection


class ClassificationType(TextEnum):
    """An enum of possible classification types"""
    PUBLIC = 'Public'
    INTERNAL = 'Internal'
    CONFIDENTIAL = 'Confidential'
    NONE = 'None'


class Item(BaseObject):
    """Box API endpoint for interacting with files and folders."""

    _classification_template_key = 'securityClassification-6VMVochwUWo'

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
        if file_id:
            self.validate_item_id(file_id)
        endpoint = '{0}/content'.format(file_id) if file_id else 'content'
        url = '{0}/files/{1}'.format(self._session.api_config.BASE_API_URL, endpoint)
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
        (https://developer.box.com/en/guides/uploads/check/)

        Returns an accelerator URL if available, which comes for free in the response.

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
        :return:
            The Accelerator upload url or None if cannot get the Accelerator upload url.
        :rtype:
            `unicode` or None
        :raises:
            :class:`BoxAPIException` when preflight check fails.
        """
        if file_id:
            self.validate_item_id(file_id)
        endpoint = '{0}/content'.format(file_id) if file_id else 'content'
        url = '{0}/files/{1}'.format(self._session.api_config.BASE_API_URL, endpoint)
        data = {'size': size}
        if name:
            data['name'] = name
        if parent_id:
            data['parent'] = {'id': parent_id}

        response_json = self._session.options(
            url=url,
            expect_json_response=True,
            data=json.dumps(data),
        ).json()
        return response_json.get('upload_url', None)

    @api_call
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
        self.validate_item_id(self._object_id)
        headers = {'If-Match': etag} if etag is not None else None
        return super(Item, self).update_info(data, headers=headers)

    @api_call
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

    @api_call
    def get(self, fields=None, etag=None):
        """Base class override.

        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
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
        self.validate_item_id(self._object_id)
        headers = {'If-None-Match': etag} if etag is not None else None
        return super(Item, self).get(fields=fields, headers=headers)

    @api_call
    def copy(self, parent_folder, name=None):
        """Copy the item to the given folder.

        :param parent_folder:
            The folder to which the item should be copied.
        :type parent_folder:
            :class:`Folder`
        :param name:
            A new name for the item, in case there is already another item in the new parent folder with the same name.
        :type name:
            `unicode` or None
        """
        self.validate_item_id(self._object_id)
        url = self.get_url('copy')
        data = {
            'parent': {'id': parent_folder.object_id}
        }
        if name is not None:
            data['name'] = name
        box_response = self._session.post(url, data=json.dumps(data))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def move(self, parent_folder, name=None):
        """
        Move the item to the given folder.

        :param parent_folder:
            The parent `Folder` object, where the item will be moved to.
        :type parent_folder:
            :class:`Folder`
        :param name:
            A new name for the item, in case there is already another item in the new parent folder with the same name.
        :type name:
            `unicode` or None
        """
        data = {
            'parent': {'id': parent_folder.object_id}
        }
        if name is not None:
            data['name'] = name
        return self.update_info(data)

    @api_call
    def create_shared_link(
            self,
            access=None,
            etag=None,
            unshared_at=SDK_VALUE_NOT_SET,
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
            and has permission to set expiration dates.  Takes an RFC3339-formatted string, e.g.
            '2018-10-31T23:59:59-07:00' for 11:59:59 PM on October 31, 2018 in the America/Los_Angeles timezone.
            The time portion can be omitted, which defaults to midnight (00:00:00) on that date.
        :type unshared_at:
            `unicode` or None
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

        if unshared_at is not SDK_VALUE_NOT_SET:
            data['shared_link']['unshared_at'] = unshared_at

        if allow_download is not None or allow_preview is not None:
            data['shared_link']['permissions'] = permissions = {}
            if allow_download is not None:
                permissions['can_download'] = allow_download
            if allow_preview is not None:
                permissions['can_preview'] = allow_preview

        if password is not None:
            data['shared_link']['password'] = password

        return self.update_info(data, etag=etag)

    @api_call
    def get_shared_link(
            self,
            access=None,
            etag=None,
            unshared_at=SDK_VALUE_NOT_SET,
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
            `unicode` or None
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

    @api_call
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

    @api_call
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
        # pylint:disable=arguments-differ
        self.validate_item_id(self._object_id)
        headers = {'If-Match': etag} if etag is not None else None
        return super(Item, self).delete(params, headers)

    def metadata(self, scope='global', template='properties'):
        """
        Instantiate a :class:`Metadata` object associated with this item.

        :param scope:
            Scope of the metadata. Must be either 'global' or 'enterprise'.
        :type scope:
            `unicode`
        :param template:
            The name of the metadata template.
            See https://developer.box.com/en/reference/resources/metadata/ for more details.
        :type template:
            `unicode`
        :return:
            A new metadata instance associated with this item.
        :rtype:
            :class:`Metadata`
        """
        self.validate_item_id(self._object_id)
        return Metadata(self._session, self, scope, template)

    def get_all_metadata(self):
        """
        Get all metadata attached to the item.
        """
        self.validate_item_id(self._object_id)
        return MarkerBasedDictCollection(
            session=self._session,
            url=self.get_url('metadata'),
            limit=None,
            marker=None,
            return_full_pages=False,
        )

    @api_call
    def get_watermark(self):
        """
        Return the watermark info for a Box file

        :return:
            Watermark object.
        :rtype:
            :class:`Watermark`
        """
        self.validate_item_id(self._object_id)
        url = self.get_url('watermark')
        box_response = self._session.get(url)
        response = box_response.json()
        return self.translator.get('watermark')(response['watermark'])

    @api_call
    def apply_watermark(self):
        """
        Apply watermark on a Box file

        :return:
            Watermark object.
        :rtype:
            :class:`Watermark`
        """
        self.validate_item_id(self._object_id)
        url = self.get_url('watermark')
        body_attributes = {
            'watermark': {
                'imprint': 'default'
            }
        }
        box_response = self._session.put(url, data=json.dumps(body_attributes))
        response = box_response.json()
        return self.translator.get('watermark')(response['watermark'])

    @api_call
    def delete_watermark(self):
        """
        Deletes the watermark info for a Box file

        :return:
            Whether or not the delete succeeded.
        :rtype:
            `bool`
        """
        self.validate_item_id(self._object_id)
        url = self.get_url('watermark')
        box_response = self._session.delete(url, expect_json_response=False)
        return box_response.ok

    @api_call
    def add_to_collection(self, collection):
        """
        Add the item to a collection.  This method is not currently safe from race conditions.

        :param collection:
            The collection to add the item to.
        :type collection:
            :class:`Collection`
        :return:
            This item.
        :rtype:
            :class:`Item`
        """
        collections = self.get(fields=['collections']).collections  # pylint:disable=no-member
        collections.append({'id': collection.object_id})
        data = {
            'collections': collections
        }
        return self.update_info(data)

    @api_call
    def remove_from_collection(self, collection):
        """
        Remove the item from a collection.  This method is not currently safe from race conditions.

        :param collection:
            The collection to remove the item from.
        :type collection:
            :class:`Collection`
        :return:
            This item.
        :rtype:
            :class:`Item`
        """
        collections = self.get(fields=['collections']).collections  # pylint:disable=no-member
        updated_collections = [c for c in collections if c['id'] != collection.object_id]
        data = {
            'collections': updated_collections
        }
        return self.update_info(data)

    @api_call
    def collaborate(self, accessible_by, role, can_view_path=None, notify=None, fields=None):
        """Collaborate user or group onto a Box item.

        :param accessible_by:
            An object containing the collaborator.
        :type accessible_by:
            class:`User` or class:`Group`
        :param role:
            The permission level to grant the collaborator.
        :type role:
            `unicode`
        :param can_view_path:
            Indicates whether the user can view the path of the item collaborated into.  This can only be set for
            collaborations on folders.
        :type can_view_path:
            `bool` or None
        :param notify:
            Determines if the collaborator should receive a notification for the collaboration.
        :type notify:
            `bool` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :return:
            The new collaboration
        :rtype:
            :class:`Collaboration`
        """
        self.validate_item_id(self._object_id)
        url = self._session.get_url('collaborations')
        body = {
            'item': {
                'type': self.object_type,
                'id': self.object_id,
            },
            'accessible_by': {
                'type': accessible_by.object_type,
                'id': accessible_by.object_id,
            },
            'role': role,
        }
        if can_view_path is not None:
            body['can_view_path'] = can_view_path
        params = {}
        if fields is not None:
            params['fields'] = ','.join(fields)
        if notify is not None:
            params['notify'] = notify
        response = self._session.post(url, data=json.dumps(body), params=params).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def collaborate_with_login(self, login, role, can_view_path=None, notify=None, fields=None):
        """Collaborate user onto a Box item with the user login.

        :param login:
            The email address of the person to grant access to.
        :type login:
            `unicode`
        :param role:
            The permission level to grant the collaborator.
        :type role:
            `unicode`
        :param can_view_path:
            Indicates whether the user can view the path of the folder collaborated into.
        :type can_view_path:
            `bool` or None
        :param notify:
            Determines if the collaborator should receive a notification for the collaboration.
        :type notify:
            `bool` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :return:
            The new collaboration with the user login
        :rtype:
            :class:`Collaboration`
        """
        self.validate_item_id(self._object_id)
        url = self._session.get_url('collaborations')
        body = {
            'item': {
                'type': self.object_type,
                'id': self.object_id,
            },
            'accessible_by': {
                'type': 'user',
                'login': login,
            },
            'role': role,
        }
        if can_view_path is not None:
            body['can_view_path'] = can_view_path
        params = {}
        if fields is not None:
            params['fields'] = ','.join(fields)
        if notify is not None:
            params['notify'] = notify
        response = self._session.post(url, data=json.dumps(body), params=params).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_collaborations(self, limit=None, marker=None, fields=None):
        """
        Get the entries in the collaboration.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start returning items from when using marker-based paging.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the collaboration.
        :rtype:
            :class:`BoxObjectCollection`
        """
        self.validate_item_id(self._object_id)
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('collaborations'),
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    def add_classification(self, classification):
        """
        Applies metadata classification for the specified :class:`File` or :class:`Folder` object.

        :param classification:
            The classification to add to the :class:`File` or :class:`Folder`
        :type classification:
            `unicode`
        :return:
            The classification added to the :class:`File` or :class:`Folder.
        :rtype:
            `unicode`
        """
        classification_metadata = {
            'Box__Security__Classification__Key': classification,
        }
        metadata_classification = self.metadata(
            scope='enterprise',
            template=self._classification_template_key
        ).create(classification_metadata)
        return metadata_classification['Box__Security__Classification__Key']

    def update_classification(self, classification):
        """
        Updates metadata classification for the specified :class:`File` or :class:`Folder` object.

        :param classification:
            The classification to add to the :class:`File` or :class:`Folder`
        :type classification:
            `unicode`
        :return:
            The classification updated on the :class:`File` or :class:`Folder.
        :rtype:
            `unicode`
        """
        classification_metadata = self.metadata('enterprise', self._classification_template_key)
        updates = classification_metadata.start_update()
        updates.add('/Box__Security__Classification__Key', classification)
        metadata_classification = classification_metadata.update(updates)
        return metadata_classification['Box__Security__Classification__Key']

    def set_classification(self, classification):
        """
        Attempts to add a metadata classification to a :class:`File` or :class:`Folder`, if classification exists, then
        do update.

        :param classification:
            The classification to add to the :class:`File` or :class:`Folder`
        :type classification:
            `unicode`
        :return:
            The classification set on the :class:`File` or :class:`Folder.
        :rtype:
            `unicode`
        """
        classification_metadata = {
            'Box__Security__Classification__Key': classification,
        }
        return self.metadata(
            scope='enterprise',
            template=self._classification_template_key
        ).set(metadata=classification_metadata)['Box__Security__Classification__Key']

    def get_classification(self):
        """
        Retrieves the classification specified for the :class:`File` or :class:`Folder`

        :return:
            The classification on the :class:`File` or :class:`Folder.
        :rtype:
            `unicode` or None
        """
        try:
            classification = self.metadata('enterprise', self._classification_template_key).get()
        except BoxAPIException as err:
            if err.status == 404 and err.code == "instance_not_found":
                return None
            else:
                raise
        return classification.get('Box__Security__Classification__Key', None)

    def remove_classification(self):
        """
        Removes a metadata classification from a :class:`File` or :class:`Folder`.

        :returns:
            Whether or not the delete was successful.
        :rtype:
            `bool`
        """
        return self.metadata('enterprise', self._classification_template_key).delete()

    @staticmethod
    def validate_item_id(item_id):
        """
        Validates an item ID is numeric

        :param item_id:
        :type item_id:
            `str` or `int`
        :raises:
            BoxException: if item_id is not numeric
        :returns:
        :rtype:
            None
        """
        if not isinstance(item_id, int) and not item_id.isdigit():
            raise BoxValueError("Invalid item ID")
