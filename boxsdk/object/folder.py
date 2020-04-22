# coding: utf-8

from __future__ import unicode_literals
import json
import os
from six import text_type

from boxsdk.object.group import Group
from boxsdk.object.item import Item
from boxsdk.object.user import User
from boxsdk.pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from boxsdk.pagination.marker_based_object_collection import MarkerBasedObjectCollection
from boxsdk.util.api_call_decorator import api_call
from boxsdk.util.text_enum import TextEnum


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

    @api_call
    def preflight_check(self, size, name):
        """
        Make an API call to check if a new file with given name and size can be uploaded to this folder.
        Returns an accelerator URL if one is available.

        :param size:
            The size of the file in bytes. Specify 0 for unknown file-sizes.
        :type size:
            `int`
        :param name:
            The name of the file to be uploaded.
        :type name:
            `unicode`
        :return:
            The Accelerator upload url or None if cannot get the Accelerator upload url.
        :rtype:
            `unicode` or None
        :raises:
            :class:`BoxAPIException` when preflight check fails.
        """
        return self._preflight_check(
            size=size,
            name=name,
            parent_id=self._object_id,
        )

    def create_upload_session(self, file_size, file_name):
        """
        Creates a new chunked upload session for upload a new file.

        :param file_size:
            The size of the file in bytes that will be uploaded.
        :type file_size:
            `int`
        :param file_name:
            The name of the file that will be uploaded.
        :type file_name:
            `unicode`
        :returns:
            A :class:`UploadSession` object.
        :rtype:
            :class:`UploadSession`
        """
        url = '{0}/files/upload_sessions'.format(self.session.api_config.UPLOAD_URL)
        body_params = {
            'folder_id': self.object_id,
            'file_size': file_size,
            'file_name': file_name,
        }
        response = self._session.post(url, data=json.dumps(body_params)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_chunked_uploader(self, file_path):
        """
        Instantiate the chunked upload instance and create upload session with path to file.

        :param file_path:
            The local path to the file you wish to upload.
        :type file_path:
            `unicode`
        :returns:
            A :class:`ChunkedUploader` object.
        :rtype:
            :class:`ChunkedUploader`
        """
        total_size = os.stat(file_path).st_size
        content_stream = open(file_path, 'rb')
        file_name = os.path.basename(file_path)
        upload_session = self.create_upload_session(total_size, file_name)
        return upload_session.get_chunked_uploader_for_stream(content_stream, total_size)

    def _get_accelerator_upload_url_fow_new_uploads(self):
        """
        Get Accelerator upload url for uploading new files.

        :return:
            The Accelerator upload url or None if cannot get one
        :rtype:
            `unicode` or None
        """
        return self._get_accelerator_upload_url()

    @api_call
    def get_items(self, limit=None, offset=0, marker=None, use_marker=False, sort=None, direction=None, fields=None):
        """
        Get the items in a folder.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param offset:
            The index at which to start returning items when using offset-based pagin.
        :type offset:
            `int`
        :param use_marker:
            Whether to use marker-based paging instead of offset-based paging, defaults to False.
        :type use_marker:
            `bool`
        :param marker:
            The paging marker to start returning items from when using marker-based paging.
        :type marker:
            `unicode` or None
        :param sort:
            Item field to sort results on: 'id', 'name', or 'date'.
        :type sort':
            `unicode` or None
        :param direction:
            Sort direction for the items returned.
        :type direction:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            The collection of items in the folder.
        :rtype:
            `Iterable` of :class:`Item`
        """
        url = self.get_url('items')
        additional_params = {}
        if limit is not None:
            additional_params['limit'] = limit
        if sort:
            additional_params['sort'] = sort
        if direction:
            additional_params['direction'] = direction

        if use_marker:
            additional_params['usemarker'] = True
            return MarkerBasedObjectCollection(
                url=url,
                session=self._session,
                limit=limit,
                marker=marker,
                fields=fields,
                additional_params=additional_params,
                return_full_pages=False,
            )

        return LimitOffsetBasedObjectCollection(
            url=url,
            session=self._session,
            limit=limit,
            offset=offset,
            fields=fields,
            additional_params=additional_params,
            return_full_pages=False,
        )

    @api_call
    def upload_stream(
            self,
            file_stream,
            file_name,
            file_description=None,
            preflight_check=False,
            preflight_expected_size=0,
            upload_using_accelerator=False,
            content_created_at=None,
            content_modified_at=None,
            additional_attributes=None,
            sha1=None,
            etag=None,
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
        :param file_description:
            The description to give the file on Box.
        :type file_description:
            `unicode` or None
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
        :param content_created_at:
            The RFC-3339 datetime when the file was created.
        :type content_created_at:
            `unicode` or None
        :param content_modified_at:
            The RFC-3339 datetime when the file content was last modified.
        :type content_modified_at:
            `unicode` or None
        :param additional_attributes:
            A dictionary containing attributes to add to the file that are not covered by other parameters.
        :type additional_attributes:
            `dict` or None
        :param sha1:
            A sha1 checksum for the file.
        :type sha1:
            `unicode` or None
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :returns:
            The newly uploaded file.
        :rtype:
            :class:`File`
        """
        accelerator_upload_url = None
        if preflight_check:
            # Preflight check does double duty, returning the accelerator URL if one is available in the response.
            accelerator_upload_url = self.preflight_check(size=preflight_expected_size, name=file_name)
        elif upload_using_accelerator:
            accelerator_upload_url = self._get_accelerator_upload_url_fow_new_uploads()

        url = '{0}/files/content'.format(self._session.api_config.UPLOAD_URL)
        if upload_using_accelerator and accelerator_upload_url:
            url = accelerator_upload_url

        attributes = {
            'name': file_name,
            'parent': {'id': self._object_id},
            'description': file_description,
            'content_created_at': content_created_at,
            'content_modified_at': content_modified_at,
        }
        if additional_attributes:
            attributes.update(additional_attributes)

        data = {'attributes': json.dumps(attributes)}
        files = {
            'file': ('unused', file_stream),
        }
        headers = {}
        if etag is not None:
            headers['If-Match'] = etag
        if sha1 is not None:
            # The Content-MD5 field accepts sha1
            headers['Content-MD5'] = sha1
        if not headers:
            headers = None
        file_response = self._session.post(url, data=data, files=files, expect_json_response=False, headers=headers).json()
        if 'entries' in file_response:
            file_response = file_response['entries'][0]
        return self.translator.translate(
            session=self._session,
            response_object=file_response,
        )

    @api_call
    def upload(
            self,
            file_path=None,
            file_name=None,
            file_description=None,
            preflight_check=False,
            preflight_expected_size=0,
            upload_using_accelerator=False,
            content_created_at=None,
            content_modified_at=None,
            additional_attributes=None,
            sha1=None,
            etag=None,
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
        :param file_description:
            The description to give the file on Box. If None, then no description will be set.
        :type file_description:
            `unicode` or None
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
        :param content_created_at:
            The RFC-3339 datetime when the file was created.
        :type content_created_at:
            `unicode` or None
        :param content_modified_at:
            The RFC-3339 datetime when the file content was last modified.
        :type content_modified_at:
            `unicode` or None
        :param additional_attributes:
            A dictionary containing attributes to add to the file that are not covered by other parameters.
        :type additional_attributes:
            `dict` or None
        :param sha1:
            A sha1 checksum for the new content.
        :type sha1:
            `unicode` or None
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :type etag:
            `unicode` or None
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
                file_description,
                preflight_check,
                preflight_expected_size=preflight_expected_size,
                upload_using_accelerator=upload_using_accelerator,
                content_created_at=content_created_at,
                content_modified_at=content_modified_at,
                additional_attributes=additional_attributes,
                sha1=sha1,
                etag=etag,
            )

    @api_call
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
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
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

    @api_call
    def add_collaborator(self, collaborator, role, notify=False, can_view_path=False):
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
        :param can_view_path:
            Whether view path collaboration feature is enabled or not. Note - only
            folder owners can create collaborations with can_view_path.
        :type can_view_path:
            `bool`
        :return:
            The new collaboration
        :rtype:
            :class:`Collaboration`
        """
        collaborator_helper = _Collaborator(collaborator)
        url = self._session.get_url('collaborations')
        item = {'id': self._object_id, 'type': 'folder'}
        access_key, access_value = collaborator_helper.access
        accessible_by = {
            access_key: access_value,
            'type': collaborator_helper.type,
        }
        body_params = {
            'item': item,
            'accessible_by': accessible_by,
            'role': role,
        }
        if can_view_path:
            body_params['can_view_path'] = True
        data = json.dumps(body_params)
        params = {'notify': notify}
        box_response = self._session.post(url, expect_json_response=True, data=data, params=params)
        collaboration_response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=collaboration_response,
        )

    @api_call
    def create_web_link(self, target_url, name=None, description=None):
        """
        Create a WebLink with a given url.

        :param target_url:
            The url the web link points to.
        :type target_url:
            `unicode`
        :param name:
            The name of the web link. Optional, the API will give it a default if not specified.
        :type name:
            `unicode` or None
        :param description:
            Description of the web link
        :type name:
            `unicode` or None
        :return:
            A :class:`WebLink` object.
        :rtype:
            :class:`WebLink`
        """
        url = self._session.get_url('web_links')
        web_link_attributes = {
            'url': target_url,
            'parent': {
                'id': self.object_id
            }
        }
        if name is not None:
            web_link_attributes['name'] = name
        if description is not None:
            web_link_attributes['description'] = description
        response = self._session.post(url, data=json.dumps(web_link_attributes)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response
        )

    @api_call
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
        # pylint:disable=arguments-differ
        return super(Folder, self).delete({'recursive': recursive}, etag)

    @api_call
    def get_metadata_cascade_policies(self, owner_enterprise=None, limit=None, marker=None, fields=None):
        """
        Get the metadata cascade policies current applied to the folder.

        :param owner_enterprise:
            Which enterprise's metadata templates to get cascade policies for.  This defauls to the current
            enterprise.
        :type owner_enterprise:
            :class:`Enterprise`
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param marker:
            The paging marker to start paging from.
        :type marker:
            `unicode` or None
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the cascade policies attached on the folder.
        :rtype:
            :class:`BoxObjectCollection`
        """
        additional_params = {
            'folder_id': self.object_id,
        }
        if owner_enterprise is not None:
            additional_params['owner_enterprise_id'] = owner_enterprise.object_id

        return MarkerBasedObjectCollection(
            url=self._session.get_url('metadata_cascade_policies'),
            session=self._session,
            additional_params=additional_params,
            limit=limit,
            marker=marker,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def cascade_metadata(self, metadata_template):
        """
        Create a metadata cascade policy to apply the metadata instance values on the folder for the given metadata
        template to all files within the folder.

        :param metadata_template:
            The metadata template to cascade values for
        :type metadata_template:
            :class:`MetadataTemplate`
        :returns:
            The created metadata cascade policy
        :rtype:
            :class:`MetadataCascadePolicy`
        """
        url = self._session.get_url('metadata_cascade_policies')

        body = {
            'folder_id': self.object_id,
            'scope': metadata_template.scope,
            'templateKey': metadata_template.template_key,
        }

        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(self._session, response)
