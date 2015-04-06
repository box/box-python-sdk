# coding: utf-8

from __future__ import unicode_literals
import json
import os
from six import text_type
from boxsdk.config import API
from boxsdk.object.collaboration import Collaboration
from boxsdk.object.file import File
from boxsdk.object.group import Group
from boxsdk.object.item import Item
from boxsdk.object.user import User
from boxsdk.util.text_enum import TextEnum
from boxsdk.util.translator import Translator


class FolderSyncState(TextEnum):
    """An enum of all possible values of a folder's ``sync_state`` attribute.

    The value of the ``sync_state`` attribute determines whether the folder
    will be synced by sync clients.
    """
    IS_SYNCED = 'synced'
    NOT_SYNCED = 'not_synced'
    PARTIALLY_SYNCED = 'partially_synced'


class _CollaborationType(TextEnum):
    """The type of a collaboration"""
    USER = 'user'
    GROUP = 'group'


class _Collaborator(object):
    """This helper class represents a collaborator on Box. A Collaborator can be a User, Group, or an email address"""
    def __init__(self, collaborator):
        if isinstance(collaborator, User):
            self._setup(user=collaborator)
        elif isinstance(collaborator, Group):
            self._setup(group=collaborator)
        elif isinstance(collaborator, text_type):
            self._setup(email_address=collaborator)
        else:
            raise TypeError('Collaborator must be User, Group, or unicode string')

    def _setup(self, user=None, group=None, email_address=None):
        """
        :param user:
            The Box user if applicable
        :type user:
            :class:`User`
        :param group:
            The Box group if applicable
        :type group:
            :class:`Group`
        :param email_address:
            The email address of the user if not a user of Box
        :type email_address:
            `unicode`
        """
        self._type = _CollaborationType.GROUP if group else _CollaborationType.USER
        id_object = user or group
        if id_object:
            self._key = 'id'
            self._identifier = id_object.object_id
        else:
            self._key = 'login'
            self._identifier = email_address

    @property
    def access(self):
        """Return a tuple for how to access collaborator

        The first element is the key for access, the second is the value
        :rtype:
            `tuple` of `unicode`, `unicode`
        """
        return self._key, self._identifier

    @property
    def type(self):
        """Return the type of collaborator (user or group)
        :rtype:
            `unicode`
        """
        return self._type


class Folder(Item):
    """Box API endpoint for interacting with folders."""

    _item_type = 'folder'

    def preflight_check(self, size, name):
        """
        Make an API call to check if a new file with given name and size can be uploaded to this folder.

        :param size:
            The size of the file in bytes. Specify 0 for unknown file-sizes.
        :type size:
            `int`
        :param name:
            The name of the file to be uploaded.
        :type name:
            `unicode`
        :raises:
            :class:`BoxAPIException` when preflight check fails.
        """
        self._preflight_check(
            size=size,
            name=name,
            parent_id=self._object_id,
        )

    def _get_accelerator_upload_url_fow_new_uploads(self):
        """
        Get Accelerator upload url for uploading new files.

        :return:
            The Accelerator upload url or None if cannot get one
        :rtype:
            `unicode` or None
        """
        return self._get_accelerator_upload_url()

    def get_items(self, limit, offset=0, fields=None):
        """Get the items in a folder.

        :param limit:
            The maximum number of items to return.
        :type limit:
            `int`
        :param offset:
            The index at which to start returning items.
        :type offset:
            `int`
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            A list of items in the folder.
        :rtype:
            `list` of :class:`Item`
        """
        url = self.get_url('items')
        params = {
            'limit': limit,
            'offset': offset,
        }
        if fields:
            params['fields'] = ','.join(fields)
        box_response = self._session.get(url, params=params)
        response = box_response.json()
        return [Translator().translate(item['type'])(self._session, item['id'], item) for item in response['entries']]

    def upload_stream(
            self,
            file_stream,
            file_name,
            preflight_check=False,
            preflight_expected_size=0,
            upload_using_accelerator=False,
    ):
        """
        Upload a file to the folder.
        The contents are taken from the given file stream, and it will have the given name.

        :param file_stream:
            The file-like object containing the bytes
        :type file_stream:
            `file`
        :param file_name:
            The name to give the file on Box.
        :type file_name:
            `unicode`
        :param preflight_check:
            If specified, preflight check will be performed before actually uploading the file.
        :type preflight_check:
            `bool`
        :param preflight_expected_size:
            The size of the file to be uploaded in bytes, which is used for preflight check. The default value is '0',
            which means the file size is unknown.
        :type preflight_expected_size:
            `int`
        :param upload_using_accelerator:
            If specified, the upload will try to use Box Accelerator to speed up the uploads for big files.
            It will make an extra API call before the actual upload to get the Accelerator upload url, and then make
            a POST request to that url instead of the default Box upload url. It falls back to normal upload endpoint,
            if cannot get the Accelerator upload url.

            Please notice that this is a premium feature, which might not be available to your app.
        :type upload_using_accelerator:
            `bool`
        :returns:
            The newly uploaded file.
        :rtype:
            :class:`File`
        """
        if preflight_check:
            self.preflight_check(size=preflight_expected_size, name=file_name)

        url = '{0}/files/content'.format(API.UPLOAD_URL)
        if upload_using_accelerator:
            accelerator_upload_url = self._get_accelerator_upload_url_fow_new_uploads()
            if accelerator_upload_url:
                url = accelerator_upload_url

        data = {'attributes': json.dumps({
            'name': file_name,
            'parent': {'id': self._object_id},
        })}
        files = {
            'file': ('unused', file_stream),
        }
        box_response = self._session.post(url, data=data, files=files, expect_json_response=False)
        file_response = box_response.json()['entries'][0]
        file_id = file_response['id']
        return File(
            session=self._session,
            object_id=file_id,
            response_object=file_response,
        )

    def upload(
            self,
            file_path=None,
            file_name=None,
            preflight_check=False,
            preflight_expected_size=0,
            upload_using_accelerator=False,
    ):
        """
        Upload a file to the folder.
        The contents are taken from the given file path, and it will have the given name.
        If file_name is not specified, the uploaded file will take its name from file_path.

        :param file_path:
            The file path of the file to upload to Box.
        :type file_path:
            `unicode`
        :param file_name:
            The name to give the file on Box. If None, then use the leaf name of file_path
        :type file_name:
            `unicode`
        :param preflight_check:
            If specified, preflight check will be performed before actually uploading the file.
        :type preflight_check:
            `bool`
        :param preflight_expected_size:
            The size of the file to be uploaded in bytes, which is used for preflight check. The default value is '0',
            which means the file size is unknown.
        :type preflight_expected_size:
            `int`
        :param upload_using_accelerator:
            If specified, the upload will try to use Box Accelerator to speed up the uploads for big files.
            It will make an extra API call before the actual upload to get the Accelerator upload url, and then make
            a POST request to that url instead of the default Box upload url. It falls back to normal upload endpoint,
            if cannot get the Accelerator upload url.

            Please notice that this is a premium feature, which might not be available to your app.
        :type upload_using_accelerator:
            `bool`
        :returns:
            The newly uploaded file.
        :rtype:
            :class:`File`
        """
        if file_name is None:
            file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as file_stream:
            return self.upload_stream(
                file_stream,
                file_name,
                preflight_check,
                preflight_expected_size=preflight_expected_size,
                upload_using_accelerator=upload_using_accelerator,
            )

    def create_subfolder(self, name):
        """
        Create a subfolder with the given name in the folder.

        :param name:
            The name of the new folder
        :type name:
            `unicode`
        """
        url = self.get_type_url()
        data = {
            'name': name,
            'parent': {
                'id': self._object_id,
            }
        }
        box_response = self._session.post(url, data=json.dumps(data))
        response = box_response.json()
        return Folder(
            session=self._session,
            object_id=response['id'],
            response_object=response,
        )

    def update_sync_state(self, sync_state):
        """Update the ``sync_state`` attribute of this folder.

        Change whether this folder will be synced by sync clients.

        :param sync_state:
            The desired sync state of this folder.
            Must be a member of the `FolderSyncState` enum.
        :type sync_state:
            :class:`FolderSyncState`
        :return:
            A new :class:`Folder` instance with updated information reflecting the new sync state.
        :rtype:
            :class:`Folder`
        """
        data = {
            'sync_state': sync_state,
        }
        return self.update_info(data=data)

    def add_collaborator(self, collaborator, role, notify=False):
        """Add a collaborator to the folder

        :param collaborator:
            collaborator to add. May be a User, Group, or email address (unicode string)
        :type collaborator:
            :class:`User` or :class:`Group` or `unicode`
        :param role:
            The collaboration role
        :type role:
            :class:`CollaboratorRole`
        :param notify:
            Whether to send a notification email to the collaborator
        :type notify:
            `bool`
        :return:
            The new collaboration
        :rtype:
            :class:`Collaboration`
        """
        collaborator_helper = _Collaborator(collaborator)
        url = API.BASE_API_URL + '/collaborations'
        item = {'id': self._object_id, 'type': 'folder'}
        access_key, access_value = collaborator_helper.access
        accessible_by = {
            access_key: access_value,
            'type': collaborator_helper.type
        }
        data = json.dumps({
            'item': item,
            'accessible_by': accessible_by,
            'role': role,
        })
        params = {'notify': notify}
        box_response = self._session.post(url, expect_json_response=True, data=data, params=params)
        collaboration_response = box_response.json()
        collab_id = collaboration_response['id']
        return Collaboration(
            session=self._session,
            object_id=collab_id,
            response_object=collaboration_response,
        )

    def delete(self, recursive=True, etag=None):
        """Base class override. Delete the folder.

        :param recursive:
            Whether or not the folder should be deleted if it isn't empty.
        :type recursive:
            `bool`
        :param etag:
            If specified, instruct the Box API to delete the folder only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :returns:
            Whether or not the update was successful.
        :rtype:
            `bool`
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the folder.
        """
        return super(Folder, self).delete({'recursive': recursive}, etag)
