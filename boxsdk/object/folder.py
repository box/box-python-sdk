import json
import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Tuple, Optional, Iterable, IO, Union

from boxsdk.object.group import Group
from boxsdk.object.item import Item
from boxsdk.object.user import User
from boxsdk.pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection
from boxsdk.pagination.marker_based_object_collection import MarkerBasedObjectCollection
from boxsdk.util.api_call_decorator import api_call
from boxsdk.util.datetime_formatter import normalize_date_to_rfc3339_format
from boxsdk.util.default_arg_value import SDK_VALUE_NOT_SET
from boxsdk.util.text_enum import TextEnum

if TYPE_CHECKING:
    from boxsdk.object.upload_session import UploadSession
    from boxsdk.util.chunked_uploader import ChunkedUploader
    from boxsdk.object.file import File
    from boxsdk.object.collaboration import CollaborationRole, Collaboration
    from boxsdk.object.web_link import WebLink
    from boxsdk.object.enterprise import Enterprise
    from boxsdk.pagination.box_object_collection import BoxObjectCollection
    from boxsdk.object.metadata_template import MetadataTemplate
    from boxsdk.object.metadata_cascade_policy import MetadataCascadePolicy
    from boxsdk.object.folder_lock import FolderLock


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


class _Collaborator:
    """This helper class represents a collaborator on Box. A Collaborator can be a User, Group, or an email address"""

    def __init__(self, collaborator: Any):
        if isinstance(collaborator, User):
            self._setup(user=collaborator)
        elif isinstance(collaborator, Group):
            self._setup(group=collaborator)
        elif isinstance(collaborator, str):
            self._setup(email_address=collaborator)
        else:
            raise TypeError('Collaborator must be User, Group, or unicode string')

    def _setup(self, user: User = None, group: Group = None, email_address: str = None) -> None:
        """
        :param user:
            The Box user if applicable
        :param group:
            The Box group if applicable
        :param email_address:
            The email address of the user if not a user of Box
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
    def access(self) -> Tuple[str, str]:
        """Return a tuple for how to access collaborator

        The first element is the key for access, the second is the value
        """
        return self._key, self._identifier

    @property
    def type(self) -> str:
        """Return the type of collaborator (user or group)"""
        return self._type


class Folder(Item):
    """Box API endpoint for interacting with folders."""

    _item_type = 'folder'

    @api_call
    def preflight_check(self, size: int, name: str) -> Optional[str]:
        """
        Make an API call to check if a new file with given name and size can be uploaded to this folder.
        Returns an accelerator URL if one is available.

        :param size:
            The size of the file in bytes. Specify 0 for unknown file-sizes.
        :param name:
            The name of the file to be uploaded.
        :return:
            The Accelerator upload url or None if cannot get the Accelerator upload url.
        :raises:
            :class:`BoxAPIException` when preflight check fails.
        """
        return self._preflight_check(
            size=size,
            name=name,
            parent_id=self._object_id,
        )

    @api_call
    def create_upload_session(self, file_size: int, file_name: str) -> 'UploadSession':
        """
        Creates a new chunked upload session for upload a new file.

        :param file_size:
            The size of the file in bytes that will be uploaded.
        :param file_name:
            The name of the file that will be uploaded.
        :returns:
            A :class:`UploadSession` object.
        """
        url = f'{self.session.api_config.UPLOAD_URL}/files/upload_sessions'
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
    def get_chunked_uploader(self, file_path: str, file_name: Optional[str] = None) -> 'ChunkedUploader':
        # pylint: disable=consider-using-with
        """
        Instantiate the chunked upload instance and create upload session with path to file.

        :param file_path:
            The local path to the file you wish to upload.
         :param file_name:
            The name with extention of the file that will be uploaded, e.g. new_file_name.zip.
            If not specified, the name from the local system is used.
        :returns:
            A :class:`ChunkedUploader` object.
        """
        total_size = os.stat(file_path).st_size
        upload_file_name = file_name if file_name else os.path.basename(file_path)
        content_stream = open(file_path, 'rb')

        try:
            upload_session = self.create_upload_session(total_size, upload_file_name)
            return upload_session.get_chunked_uploader_for_stream(content_stream, total_size)
        except Exception:
            content_stream.close()
            raise

    def _get_accelerator_upload_url_fow_new_uploads(self) -> Optional[str]:
        """
        Get Accelerator upload url for uploading new files.

        :return:
            The Accelerator upload url or None if cannot get one
        """
        return self._get_accelerator_upload_url()

    @api_call
    def get_items(
            self,
            limit: Optional[int] = None,
            offset: int = 0,
            marker: Optional[str] = None,
            use_marker: bool = False,
            sort: Optional[str] = None,
            direction: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> Iterable[Item]:
        """
        Get the items in a folder.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :param offset:
            The index at which to start returning items when using offset-based pagin.
        :param marker:
            The paging marker to start returning items from when using marker-based paging.
        :param use_marker:
            Whether to use marker-based paging instead of offset-based paging, defaults to False.
        :param sort:
            Item field to sort results on: 'id', 'name', or 'date'.
        :param direction:
            Sort direction for the items returned.
        :param fields:
            List of fields to request.
        :returns:
            The collection of items in the folder.
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
            file_stream: IO[bytes],
            file_name: str,
            file_description: Optional[str] = None,
            preflight_check: bool = False,
            preflight_expected_size: int = 0,
            upload_using_accelerator: bool = False,
            content_created_at: Union[datetime, str] = None,
            content_modified_at: Union[datetime, str] = None,
            additional_attributes: Optional[dict] = None,
            sha1: Optional[str] = None,
            etag: Optional[str] = None,
    ) -> 'File':
        """
        Upload a file to the folder.
        The contents are taken from the given file stream, and it will have the given name.

        :param file_stream:
            The file-like object containing the bytes
        :param file_name:
            The name to give the file on Box.
        :param file_description:
            The description to give the file on Box.
        :param preflight_check:
            If specified, preflight check will be performed before actually uploading the file.
        :param preflight_expected_size:
            The size of the file to be uploaded in bytes, which is used for preflight check. The default value is '0',
            which means the file size is unknown.
        :param upload_using_accelerator:
            If specified, the upload will try to use Box Accelerator to speed up the uploads for big files.
            It will make an extra API call before the actual upload to get the Accelerator upload url, and then make
            a POST request to that url instead of the default Box upload url. It falls back to normal upload endpoint,
            if cannot get the Accelerator upload url.

            Please notice that this is a premium feature, which might not be available to your app.
        :param content_created_at:
            A datetime string in a format supported by the dateutil library or a datetime.datetime object,
            which specifies when the file was created. If no timezone info provided, local timezone will be applied.
        :param content_modified_at:
            A datetime string in a format supported by the dateutil library or a datetime.datetime object, which
            specifies when the file was last modified. If no timezone info provided, local timezone will be applied.
        :param additional_attributes:
            A dictionary containing attributes to add to the file that are not covered by other parameters.
        :param sha1:
            A sha1 checksum for the file.
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :returns:
            The newly uploaded file.
        """
        accelerator_upload_url = None
        if preflight_check:
            # Preflight check does double duty, returning the accelerator URL if one is available in the response.
            accelerator_upload_url = self.preflight_check(size=preflight_expected_size, name=file_name)
        elif upload_using_accelerator:
            accelerator_upload_url = self._get_accelerator_upload_url_fow_new_uploads()

        url = f'{self._session.api_config.UPLOAD_URL}/files/content'
        if upload_using_accelerator and accelerator_upload_url:
            url = accelerator_upload_url

        attributes = {
            'name': file_name,
            'parent': {'id': self._object_id},
            'description': file_description,
            'content_created_at': normalize_date_to_rfc3339_format(content_created_at),
            'content_modified_at': normalize_date_to_rfc3339_format(content_modified_at),
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
        file_response = self._session.post(
            url, data=data, files=files, expect_json_response=False, headers=headers
        ).json()
        if 'entries' in file_response:
            file_response = file_response['entries'][0]
        return self.translator.translate(
            session=self._session,
            response_object=file_response,
        )

    @api_call
    def upload(
            self,
            file_path: str = None,
            file_name: str = None,
            file_description: Optional[str] = None,
            preflight_check: bool = False,
            preflight_expected_size: int = 0,
            upload_using_accelerator: bool = False,
            content_created_at: Union[datetime, str] = None,
            content_modified_at: Union[datetime, str] = None,
            additional_attributes: Optional[dict] = None,
            sha1: Optional[str] = None,
            etag: Optional[str] = None,
    ) -> 'File':
        """
        Upload a file to the folder.
        The contents are taken from the given file path, and it will have the given name.
        If file_name is not specified, the uploaded file will take its name from file_path.

        :param file_path:
            The file path of the file to upload to Box.
        :param file_name:
            The name to give the file on Box. If None, then use the leaf name of file_path
        :param file_description:
            The description to give the file on Box. If None, then no description will be set.
        :param preflight_check:
            If specified, preflight check will be performed before actually uploading the file.
        :param preflight_expected_size:
            The size of the file to be uploaded in bytes, which is used for preflight check. The default value is '0',
            which means the file size is unknown.
        :param upload_using_accelerator:
            If specified, the upload will try to use Box Accelerator to speed up the uploads for big files.
            It will make an extra API call before the actual upload to get the Accelerator upload url, and then make
            a POST request to that url instead of the default Box upload url. It falls back to normal upload endpoint,
            if cannot get the Accelerator upload url.

            Please notice that this is a premium feature, which might not be available to your app.
        :param content_created_at:
            A datetime string in a format supported by the dateutil library or a datetime.datetime object,
            which specifies when the file was created. If no timezone info provided, local timezone will be applied.
        :param content_modified_at:
            A datetime string in a format supported by the dateutil library or a datetime.datetime object, which
            specifies when the file was last modified.If no timezone info provided, local timezone will be applied.
        :param additional_attributes:
            A dictionary containing attributes to add to the file that are not covered by other parameters.
        :param sha1:
            A sha1 checksum for the new content.
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :returns:
            The newly uploaded file.
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
    def create_subfolder(self, name: str) -> 'Folder':
        """
        Create a subfolder with the given name in the folder.

        :param name:
            The name of the new folder
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
    def update_sync_state(self, sync_state: FolderSyncState) -> 'Folder':
        """Update the ``sync_state`` attribute of this folder.

        Change whether this folder will be synced by sync clients.

        :param sync_state:
            The desired sync state of this folder.
            Must be a member of the `FolderSyncState` enum.
        :return:
            A new :class:`Folder` instance with updated information reflecting the new sync state.
        """
        data = {
            'sync_state': sync_state,
        }
        return self.update_info(data=data)

    @api_call
    def create_shared_link(
            self,
            *,
            access: Optional[str] = None,
            etag: Optional[str] = None,
            unshared_at: Union[datetime, str, None] = SDK_VALUE_NOT_SET,
            allow_download: Optional[bool] = None,
            allow_preview: Optional[bool] = None,
            password: Optional[str] = None,
            vanity_name: Optional[str] = None,
            **kwargs: Any
    ) -> 'Folder':
        """
        Baseclass override.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :param etag:
            If specified, instruct the Box API to create the link only if the current version's etag matches.
        :param unshared_at:
            The date on which this link should be disabled. May only be set if the current user is not a free user
            and has permission to set expiration dates. Takes a datetime string supported by the dateutil library
            or a datetime.datetime object. If no timezone info provided, local timezone will be applied.
            The time portion can be omitted, which defaults to midnight (00:00:00) on that date.
        :param allow_download:
            Whether the folder being shared can be downloaded when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :param allow_preview:
            Whether the folder being shared can be previewed when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :param password:
            The password required to view this link. If no password is specified then no password will be set.
            Please notice that this is a premium feature, which might not be available to your app.
        :param vanity_name:
            Defines a custom vanity name to use in the shared link URL, eg. https://app.box.com/v/my-custom-vanity-name.
            If this parameter is None, the standard shared link URL will be used.
        :param kwargs:
            Used to fulfill the contract of overriden method
        :return:
            The updated object with shared link.
            Returns a new object of the same type, without modifying the original object passed as self.
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the folder.
        """
        # pylint:disable=arguments-differ
        return super().create_shared_link(
            access=access,
            etag=etag,
            unshared_at=unshared_at,
            allow_download=allow_download,
            allow_preview=allow_preview,
            password=password,
            vanity_name=vanity_name
        )

    @api_call
    def get_shared_link(
            self,
            *,
            access: Optional[str] = None,
            etag: Optional[str] = None,
            unshared_at: Union[datetime, str, None] = SDK_VALUE_NOT_SET,
            allow_download: Optional[bool] = None,
            allow_preview: Optional[bool] = None,
            password: Optional[str] = None,
            vanity_name: Optional[str] = None,
            **kwargs: Any
    ) -> 'str':
        """
        Baseclass override.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :param etag:
            If specified, instruct the Box API to create the link only if the current version's etag matches.
        :param unshared_at:
            The date on which this link should be disabled. May only be set if the current user is not a free user
            and has permission to set expiration dates. Takes a datetime string supported by the dateutil library
            or a datetime.datetime object. If no timezone info provided, local timezone will be applied.
            The time portion can be omitted, which defaults to midnight (00:00:00) on that date.
        :param allow_download:
            Whether the folder being shared can be downloaded when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :param allow_preview:
            Whether the folder being shared can be previewed when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :param password:
            The password required to view this link. If no password is specified then no password will be set.
            Please notice that this is a premium feature, which might not be available to your app.
        :param vanity_name:
            Defines a custom vanity name to use in the shared link URL, eg. https://app.box.com/v/my-custom-vanity-name.
            If this parameter is None, the standard shared link URL will be used.
        :param kwargs:
            Used to fulfill the contract of overriden method
        :returns:
            The URL of the shared link.
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the folder.
        """
        # pylint:disable=arguments-differ
        return super().get_shared_link(
            access=access,
            etag=etag,
            unshared_at=unshared_at,
            allow_download=allow_download,
            allow_preview=allow_preview,
            password=password,
            vanity_name=vanity_name
        )

    @api_call
    def add_collaborator(
            self,
            collaborator: Union[User, Group, str],
            role: 'CollaborationRole',
            notify: bool = False,
            can_view_path: bool = False
    ) -> 'Collaboration':
        """Add a collaborator to the folder

        :param collaborator:
            collaborator to add. It may be a User, Group, or email address (unicode string)
        :param role:
            The collaboration role
        :param notify:
            Whether to send a notification email to the collaborator
        :param can_view_path:
            Whether view path collaboration feature is enabled or not. Note - only
            folder owners can create collaborations with can_view_path.
        :return:
            The new collaboration
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
    def create_web_link(
            self,
            target_url: str,
            name: Optional[str] = None,
            description: Optional[str] = None
    ) -> 'WebLink':
        """
        Create a WebLink with a given url.

        :param target_url:
            The url the web link points to.
        :param name:
            The name of the web link. Optional, the API will give it a default if not specified.
        :param description:
            Description of the web link
        :return:
            A :class:`WebLink` object.
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
    def delete(
            self,
            *,
            recursive: bool = True,
            etag: Optional[str] = None,
            **kwargs
    ) -> bool:
        """Base class override. Delete the folder.

        :param recursive:
            Whether or not the folder should be deleted if it isn't empty.
        :param etag:
            If specified, instruct the Box API to delete the folder only if the current version's etag matches.
        :returns:
            Whether or not the update was successful.
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the folder.
        """
        # pylint:disable=arguments-differ,arguments-renamed
        return super().delete(params={'recursive': recursive}, etag=etag, **kwargs)

    @api_call
    def get_metadata_cascade_policies(
            self,
            owner_enterprise: 'Enterprise' = None,
            limit: Optional[int] = None,
            marker: Optional[str] = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the metadata cascade policies current applied to the folder.

        :param owner_enterprise:
            Which enterprise's metadata templates to get cascade policies for.  This defauls to the current
            enterprise.
        :param limit:
            The maximum number of entries to return per page. If not specified, then will use the server-side default.
        :param marker:
            The paging marker to start paging from.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the cascade policies attached on the folder.
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
    def cascade_metadata(self, metadata_template: 'MetadataTemplate') -> 'MetadataCascadePolicy':
        """
        Create a metadata cascade policy to apply the metadata instance values on the folder for the given metadata
        template to all files within the folder.

        :param metadata_template:
            The metadata template to cascade values for
        :returns:
            The created metadata cascade policy
        """
        url = self._session.get_url('metadata_cascade_policies')

        body = {
            'folder_id': self.object_id,
            'scope': metadata_template.scope,
            'templateKey': metadata_template.template_key,
        }

        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(self._session, response)

    @api_call
    def create_lock(self) -> 'FolderLock':
        """
        Creates a folder lock on a folder, preventing it from being moved and/or deleted.

        :returns:
            The created folder lock
        """
        url = self._session.get_url('folder_locks')

        body = {
            'folder': {
                'type': 'folder',
                'id': self.object_id
            },
            'locked_operations': {
                'move': True,
                'delete': True
            }
        }

        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(self._session, response)

    @api_call
    def get_locks(self) -> 'BoxObjectCollection':
        """
        Lists all folder locks for a given folder.

        :returns:
            The collection of locks for a folder.
        """
        url = self._session.get_url('folder_locks')

        additional_params = {
            'folder_id': self.object_id,
        }

        return MarkerBasedObjectCollection(
            url=url,
            session=self._session,
            additional_params=additional_params,
            return_full_pages=False,
        )
