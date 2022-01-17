# coding: utf-8
import json
import os
from typing import TYPE_CHECKING, Optional, Tuple, Union, IO, Iterable, List

from .item import Item
from ..util.api_call_decorator import api_call
from ..util.deprecation_decorator import deprecated
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection

if TYPE_CHECKING:
    from boxsdk.object.upload_session import UploadSession
    from boxsdk.util.chunked_uploader import ChunkedUploader
    from boxsdk.object.file_version import FileVersion
    from boxsdk.pagination.box_object_collection import BoxObjectCollection
    from boxsdk.object.comment import Comment
    from boxsdk.object.task import Task
    from boxsdk.object.folder import Folder


class File(Item):
    """Box API endpoint for interacting with files."""

    _item_type = 'file'

    @api_call
    def preflight_check(self, size: int, name: Optional[str] = None) -> Optional[str]:
        """
        Make an API call to check if the file can be updated with the new name and size of the file.
        Returns an accelerator URL if one is available.

        :param size:
            The size of the file in bytes. Specify 0 for unknown file-sizes.
        :param name:
            The name of the file to be updated. It's optional, if the name is not being changed.
        :return:
            The Accelerator upload url or None if cannot get the Accelerator upload url.
        :raises:
            :class:`BoxAPIException` when preflight check fails.
        """
        return self._preflight_check(
            size=size,
            name=name,
            file_id=self._object_id,
        )

    def create_upload_session(self, file_size: int, file_name: Optional[str] = None) -> 'UploadSession':
        """
        Create a new chunked upload session for uploading a new version of the file.

        :param file_size:
            The size of the file in bytes that will be uploaded.
        :param file_name:
            The new name of the file version that will be uploaded.
        :returns:
            A :class:`UploadSession` object.
        """
        body_params = {
            'file_id': self.object_id,
            'file_size': file_size,
        }
        if file_name is not None:
            body_params['file_name'] = file_name
        url = self.get_url('upload_sessions').replace(self.session.api_config.BASE_API_URL, self.session.api_config.UPLOAD_URL)
        response = self._session.post(url, data=json.dumps(body_params)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_chunked_uploader(self, file_path: str, rename_file: bool = False) -> 'ChunkedUploader':
        """
        Instantiate the chunked upload instance and create upload session with path to file.

        :param file_path:
            The local path to the file you wish to upload.
        :param rename_file:
            Indicates whether the file should be renamed or not.
        :returns:
            A :class:`ChunkedUploader` object.
        """
        total_size = os.stat(file_path).st_size
        with open(file_path, 'rb') as content_stream:
            file_name = os.path.basename(file_path) if rename_file else None
            upload_session = self.create_upload_session(total_size, file_name)
            return upload_session.get_chunked_uploader_for_stream(content_stream, total_size)

    def _get_accelerator_upload_url_for_update(self) -> Optional[str]:
        """
        Get Accelerator upload url for updating the file.

        :return:
            The Accelerator upload url for updating the file or None if cannot get one
        """
        return self._get_accelerator_upload_url(file_id=self._object_id)

    @staticmethod
    def _construct_range_header(boundaries: Union[Tuple[int], Tuple[int, int]]) -> str:
        """
        Construct the correct value for the Range header, given a closed or open-ended range.

        :param boundaries:
            The range of bytes (inclusive)
        :returns:
            The value for the Range header
        :raises ValueError:
        """
        if len(boundaries) == 1:
            return f'bytes={boundaries[0]}-'
        if len(boundaries) == 2:
            return f'bytes={boundaries[0]}-{boundaries[1]}'

        raise ValueError('Expected a 1-tuple or 2-tuple for byte range')

    @api_call
    def content(self, file_version: Optional['FileVersion'] = None, byte_range: Tuple[int, int] = None) -> bytes:
        """
        Get the content of a file on Box.

        :param file_version:
            The specific version of the file to retrieve the contents of.
        :param byte_range:
            A tuple of inclusive byte offsets to download, e.g. (100, 199) to download the second 100 bytes of a file
        :returns:
            File content as bytes.
        """
        url = self.get_url('content')
        params = {'version': file_version.object_id} if file_version is not None else None
        headers = {'Range': self._construct_range_header(byte_range)} if byte_range is not None else None
        box_response = self._session.get(url, expect_json_response=False, params=params, headers=headers)
        return box_response.content

    @api_call
    def download_to(
            self,
            writeable_stream: IO[bytes],
            file_version: Optional['FileVersion'] = None,
            byte_range: Tuple[int, int] = None
    ) -> None:
        """
        Download the file; write it to the given stream.

        :param writeable_stream:
            A file-like object where bytes can be written into.
        :param file_version:
            The specific version of the file to retrieve the contents of.
        :param byte_range:
            A tuple of inclusive byte offsets to download, e.g. (100, 199) to download the second 100 bytes of a file
        """
        url = self.get_url('content')
        params = {'version': file_version.object_id} if file_version is not None else None
        headers = {'Range': self._construct_range_header(byte_range)} if byte_range is not None else None
        box_response = self._session.get(url, expect_json_response=False, stream=True, params=params, headers=headers)
        for chunk in box_response.network_response.response_as_stream.stream(decode_content=True):
            writeable_stream.write(chunk)

    @api_call
    def get_download_url(self, file_version: Optional['FileVersion'] = None) -> str:
        """
        Get the url to download the file.

        :param file_version:
            The specific version of the file to retrieve the contents of.
        :return: Url to download the file
        """
        url = self.get_url('content')
        params = {'version': file_version.object_id} if file_version is not None else None
        box_response = self._session.get(
            url,
            params=params,
            expect_json_response=False,
            allow_redirects=False,
        )
        return box_response.headers['location']

    @api_call
    def update_contents_with_stream(
            self,
            file_stream: IO[bytes],
            etag: Optional[str] = None,
            preflight_check: bool = False,
            preflight_expected_size: int = 0,
            upload_using_accelerator: bool = False,
            file_name: Optional[str] = None,
            content_modified_at: Optional[str] = None,
            additional_attributes: Optional[dict] = None,
            sha1: Optional[str] = None,
    ) -> 'File':
        """
        Upload a new version of a file, taking the contents from the given file stream.

        :param file_stream:
            The file-like object containing the bytes
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
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
        :param file_name:
            The new name to give the file on Box.
        :param content_modified_at:
            The RFC-3339 datetime when the file content was last modified.
        :param additional_attributes:
            A dictionary containing attributes to add to the file that are not covered by other parameters.
        :param sha1:
            A sha1 checksum for the new content.
        :returns:
            A new file object
        :raises:
            :class:`BoxAPIException` if the specified etag doesn't match the latest version of the file or preflight
            check fails.
        """
        accelerator_upload_url = None
        if preflight_check:
            # Preflight check does double duty, returning the accelerator URL if one is available in the response.
            accelerator_upload_url = self.preflight_check(size=preflight_expected_size)
        elif upload_using_accelerator:
            accelerator_upload_url = self._get_accelerator_upload_url_for_update()

        url = self.get_url('content').replace(
            self._session.api_config.BASE_API_URL,
            self._session.api_config.UPLOAD_URL,
        )
        if upload_using_accelerator and accelerator_upload_url:
            url = accelerator_upload_url

        attributes = {
            'name': file_name,
            'content_modified_at': content_modified_at,
        }
        if additional_attributes:
            attributes.update(additional_attributes)

        data = {'attributes': json.dumps(attributes)}
        files = {'file': ('unused', file_stream)}
        headers = {}
        if etag is not None:
            headers['If-Match'] = etag
        if sha1 is not None:
            # The Content-MD5 field accepts sha1
            headers['Content-MD5'] = sha1
        if not headers:
            headers = None
        file_response = self._session.post(
            url,
            expect_json_response=False,
            data=data,
            files=files,
            headers=headers,
        ).json()
        if 'entries' in file_response:
            file_response = file_response['entries'][0]
        return self.translator.translate(
            session=self._session,
            response_object=file_response,
        )

    @api_call
    def update_contents(
            self,
            file_path: str,
            etag: Optional[str] = None,
            preflight_check: bool = False,
            preflight_expected_size: int = 0,
            upload_using_accelerator: bool = False,
            file_name: Optional[str] = None,
            content_modified_at: Optional[str] = None,
            additional_attributes: Optional[dict] = None,
            sha1: Optional[str] = None,
    ) -> 'File':
        """Upload a new version of a file. The contents are taken from the given file path.

        :param file_path:
            The path of the file that should be uploaded.
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
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
        :param file_name:
            The new name to give the file on Box.
        :param content_modified_at:
            The RFC-3339 datetime when the file content was last modified.
        :param additional_attributes:
            A dictionary containing attributes to add to the file that are not covered by other parameters.
        :param sha1:
            A sha1 checksum for the new content.
        :returns:
            A new file object
        :raises:
            :class:`BoxAPIException` if the specified etag doesn't match the latest version of the file or preflight
            check fails.
        """
        with open(file_path, 'rb') as file_stream:
            return self.update_contents_with_stream(
                file_stream,
                etag,
                preflight_check,
                preflight_expected_size=preflight_expected_size,
                upload_using_accelerator=upload_using_accelerator,
                file_name=file_name,
                content_modified_at=content_modified_at,
                additional_attributes=additional_attributes,
                sha1=sha1,
            )

    @api_call
    def lock(self, prevent_download: bool = False, expire_time: Optional[str] = None) -> 'File':
        """
        Lock a file, preventing others from modifying (or possibly even downloading) it.

        :param prevent_download:
            Whether or not the lock should prevent other users from downloading the file.
        :param expire_time:
            The RFC-3339 datetime when the lock should automatically expire, unlocking the file.
        :return:
            A new :class:`File` instance reflecting that the file has been locked.
        """
        data = {
            'lock': {
                'type': 'lock',
                'is_download_prevented': prevent_download,
            }
        }
        if expire_time is not None:
            data['lock']['expires_at'] = expire_time
        return self.update_info(data=data)

    @api_call
    def unlock(self) -> 'File':
        """
        Unlock a file, releasing any restrictions that the lock maintained.

        :return:
            A new :class:`File` instance reflecting that the file has been unlocked.
        """
        data = {'lock': None}
        return self.update_info(data=data)

    @api_call
    def get_shared_link_download_url(
            self,
            access: Optional[str] = None,
            etag: Optional[str] = None,
            unshared_at: Optional[str] = None,
            allow_preview: Optional[bool] = None,
            password: Optional[str] = None,
            vanity_name: Optional[str] = None
    ) -> str:
        """
        Get a shared link download url for the file with the given access permissions.
        This url is a direct download url for the file.

        :param access:
            Determines who can access the shared link. May be open, company, or collaborators. If no access is
            specified, the default access will be used.
        :param etag:
            If specified, instruct the Box API to create the link only if the current version's etag matches.
        :param unshared_at:
            The date on which this link should be disabled. May only be set if the current user is not a free user
            and has permission to set expiration dates.  Takes an RFC3339-formatted string, e.g.
            '2018-10-31T23:59:59-07:00' for 11:59:59 PM on October 31, 2018 in the America/Los_Angeles timezone.
            The time portion can be omitted, which defaults to midnight (00:00:00) on that date.
        :param allow_preview:
            Whether or not the item being shared can be previewed when accessed via the shared link.
            If this parameter is None, the default setting will be used.
        :param password:
            The password required to view this link. If no password is specified then no password will be set.
            Please notice that this is a premium feature, which might not be available to your app.
        :param vanity_name:
            Defines a custom vanity name to use in the shared link URL, eg. https://app.box.com/v/my-custom-vanity-name.
            If this parameter is None, the standard shared link URL will be used.
        :returns:
            The URL of the shared link that allows direct download.
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        item = self.create_shared_link(
            access=access,
            etag=etag,
            unshared_at=unshared_at,
            allow_preview=allow_preview,
            password=password,
            vanity_name=vanity_name
        )
        return item.shared_link['download_url']  # pylint:disable=no-member

    @api_call
    def get_comments(
            self,
            limit: Optional[int] = None,
            offset: int = 0,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get the comments on the file.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :param offset:
            The index at which to start returning items.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the items in the folder.
        """
        return LimitOffsetBasedObjectCollection(
            self.session,
            self.get_url('comments'),
            limit=limit,
            fields=fields,
            offset=offset,
            return_full_pages=False,
        )

    @api_call
    def add_comment(self, message: str) -> 'Comment':
        """
        Add a comment to the file.

        :param message:
            The content of the reply comment.
        :return: Added comment
        """
        url = self._session.get_url('comments')
        comment_class = self._session.translator.get('comment')
        data = comment_class.construct_params_from_message(message)
        data['item'] = {
            'type': 'file',
            'id': self.object_id
        }
        box_response = self._session.post(url, data=json.dumps(data))
        response = box_response.json()
        return self._session.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def create_task(
            self,
            message: Optional[str] = None,
            due_at: Optional[str] = None,
            action: str = 'review',
            completion_rule: Optional[str] = None
    ) -> 'Task':
        """
        Create a task on the given file.

        :param message:
            An optional message to include in the task.
        :param due_at:
            When this task is due.
        :param action:
            The type of task the task assignee will be prompted to perform.
            Value is one of review,complete
        :param completion_rule:
            Defines which assignees need to complete this task before the task
            is considered completed.
            Value is one of all_assignees,any_assignee
        :return:
            The newly created task
        """
        url = self._session.get_url('tasks')
        task_attributes = {
            'item': {
                'type': 'file',
                'id': self.object_id
            },
            'action': action,
        }
        if message is not None:
            task_attributes['message'] = message
        if due_at is not None:
            task_attributes['due_at'] = due_at
        if completion_rule is not None:
            task_attributes['completion_rule'] = completion_rule
        box_response = self._session.post(url, data=json.dumps(task_attributes))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_tasks(self, fields: Iterable[str] = None) -> 'BoxObjectCollection':
        """
        Get the entries in the file tasks.

        :param fields:
            List of fields to request.
        :returns:
            An iterator of the entries in the file tasks
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('tasks'),
            limit=None,
            marker=None,
            fields=fields,
            return_full_pages=False,
        )

    @api_call
    def get_previous_versions(
            self,
            limit: Optional[int] = None,
            offset: int = None,
            fields: Iterable[str] = None
    ) -> 'BoxObjectCollection':
        """
        Get previous versions of the file.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :param offset:
            The index at which to start returning items.
        :param fields:
            List of fields to request.
        :returns:
            An iterator of the previous versions of the file.
        """
        return LimitOffsetBasedObjectCollection(
            session=self.session,
            url=self.get_url('versions'),
            limit=limit,
            fields=fields,
            offset=offset,
            return_full_pages=False,
        )

    @api_call
    def promote_version(self, file_version: 'FileVersion') -> 'FileVersion':
        """
        Promote a file version to become the current version of this file.  This will create a new file version
        identical to the previous version as the new current version.

        :param file_version:
            The file version to promote.
        :returns:
            The new file version created as the current.
        """
        url = self.get_url('versions', 'current')
        body = {
            'type': 'file_version',
            'id': file_version.object_id,
        }
        response = self._session.post(url, data=json.dumps(body)).json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def delete_version(self, file_version: 'FileVersion', etag: Optional[str] = None) -> bool:
        """
        Delete a specific version of a file.

        :param file_version:
            The file version to delete.
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :returns:
            Whether the operation succeeded.
        """
        url = self.get_url('versions', file_version.object_id)
        headers = {'If-Match': etag} if etag is not None else None
        response = self._session.delete(url, expect_json_response=False, headers=headers)
        return response.ok

    @api_call
    def get_embed_url(self) -> str:
        """
        Get a URL suitable for embedding the file in an iframe in a web application.

        :returns:
            The embed URL.
        """
        url = self.get_url()
        params = {'fields': 'expiring_embed_link'}
        response = self._session.get(url, params=params).json()
        return response['expiring_embed_link']['url']

    @api_call
    def get_representation_info(self, rep_hints: Optional[str] = None) -> List[dict]:
        """
        Get information about the representations available for a file.

        :param rep_hints:
            A formatted string describing which representations are desired.
        :returns:
            The representation information
        """
        url = self.get_url()
        params = {'fields': 'representations'}
        headers = {'X-Rep-Hints': rep_hints} if rep_hints is not None else None
        response = self._session.get(url, params=params, headers=headers).json()
        return response['representations']['entries']

    @deprecated('Use get_thumbnail_representation')
    @api_call
    def get_thumbnail(
            self,
            extension: str = 'png',
            min_width: Optional[int] = None,
            min_height: Optional[int] = None,
            max_width: Optional[int] = None,
            max_height: Optional[int] = None
    ) -> bytes:
        """
        Retrieve a thumbnail image for the file.

        :param extension:
            The file extension for the thumbnail, e.g. 'png' or 'jpg'
        :param min_width:
            The minimum width required for the thumbnail image
        :param min_height:
            The minimum height required for the thumbnail image
        :param max_width:
            The maximum width required for the thumbnail image
        :param max_height:
            The maximum height required for the thumbnail image
        :returns:
            The file contents of the thumbnail image
        """
        url = self.get_url('thumbnail.' + extension)
        params = {}
        if min_width is not None:
            params['min_width'] = min_width
        if min_height is not None:
            params['min_height'] = min_height
        if max_width is not None:
            params['max_width'] = max_width
        if max_height is not None:
            params['max_height'] = max_height

        response = self._session.get(url, params=params, expect_json_response=False)
        return response.content

    @api_call
    def get_thumbnail_representation(self, dimensions: str, extension: str = 'png') -> bytes:
        """
        Retrieve a thumbnail image for the file.

        :param dimensions:
            The width by height size of this representation in pixels (e.g. '92x92')
        :param extension:
            The file extension for the thumbnail, e.g. 'png' or 'jpg'
        :returns:
            The file contents of the thumbnail image
        """
        rep_hints = f'[{extension}?dimensions={dimensions}]'
        representations = self.get_representation_info(rep_hints)
        if representations:
            representation = representations[0]
            if representation['status'].get('code') in ('error_conversion_failed', 'error_password_protected'):
                return b''
            url = representation['content']['url_template']
            url = url.replace('{+asset_path}', '')
            response = self._session.get(url, expect_json_response=False)
            return response.content
        return b''

    @api_call
    def copy(
            self,
            *,
            parent_folder: 'Folder',
            name: Optional[str] = None,
            file_version: 'FileVersion' = None,
            **_kwargs
    ) -> 'File':
        # pylint: disable=arguments-differ
        """Copy the item to the given folder.

        :param parent_folder:
            The folder to which the item should be copied.
        :param name:
            A new name for the item, in case there is already another item in the new parent folder with the same name.
        :param file_version:
            A specific version of the file to copy
        :returns:
            The copy of the file
        """
        # pylint: disable=arguments-differ
        url = self.get_url('copy')
        data = {
            'parent': {'id': parent_folder.object_id}
        }
        if name is not None:
            data['name'] = name
        if file_version is not None:
            data['version'] = file_version.object_id
        box_response = self._session.post(url, data=json.dumps(data))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )
