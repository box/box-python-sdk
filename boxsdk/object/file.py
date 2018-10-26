# coding: utf-8

from __future__ import unicode_literals

import json

from .item import Item
from ..util.api_call_decorator import api_call
from ..pagination.marker_based_object_collection import MarkerBasedObjectCollection
from ..pagination.limit_offset_based_object_collection import LimitOffsetBasedObjectCollection


class File(Item):
    """Box API endpoint for interacting with files."""

    _item_type = 'file'

    @api_call
    def preflight_check(self, size, name=None):
        """
        Make an API call to check if the file can be updated with the new name and size of the file.

        :param size:
            The size of the file in bytes. Specify 0 for unknown file-sizes.
        :type size:
            `int`
        :param name:
            The name of the file to be updated. It's optional, if the name is not being changed.
        :type name:
            `unicode`
        :raises:
            :class:`BoxAPIException` when preflight check fails.
        """
        self._preflight_check(
            size=size,
            name=name,
            file_id=self._object_id,
        )

    def _get_accelerator_upload_url_for_update(self):
        """
        Get Accelerator upload url for updating the file.

        :return:
            The Accelerator upload url for updating the file or None if cannot get one
        :rtype:
            `unicode` or None
        """
        return self._get_accelerator_upload_url(file_id=self._object_id)

    @api_call
    def content(self):
        """
        Get the content of a file on Box.

        :returns:
            File content as bytes.
        :rtype:
            `bytes`
        """
        url = self.get_url('content')
        box_response = self._session.get(url, expect_json_response=False)
        return box_response.content

    @api_call
    def download_to(self, writeable_stream):
        """
        Download the file; write it to the given stream.

        :param writeable_stream:
            A file-like object where bytes can be written into.
        :type writeable_stream:
            `file`
        """
        url = self.get_url('content')
        box_response = self._session.get(url, expect_json_response=False, stream=True)
        for chunk in box_response.network_response.response_as_stream.stream(decode_content=True):
            writeable_stream.write(chunk)

    @api_call
    def update_contents_with_stream(
            self,
            file_stream,
            etag=None,
            preflight_check=False,
            preflight_expected_size=0,
            upload_using_accelerator=False,
    ):
        """
        Upload a new version of a file, taking the contents from the given file stream.

        :param file_stream:
            The file-like object containing the bytes
        :type file_stream:
            `file`
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :type etag:
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
        :returns:
            A new file object
        :rtype:
            :class:`File`
        :raises:
            :class:`BoxAPIException` if the specified etag doesn't match the latest version of the file or preflight
            check fails.
        """
        if preflight_check:
            self.preflight_check(size=preflight_expected_size)

        url = self.get_url('content').replace(
            self._session.api_config.BASE_API_URL,
            self._session.api_config.UPLOAD_URL,
        )
        if upload_using_accelerator:
            accelerator_upload_url = self._get_accelerator_upload_url_for_update()
            if accelerator_upload_url:
                url = accelerator_upload_url

        files = {'file': ('unused', file_stream)}
        headers = {'If-Match': etag} if etag is not None else None
        file_response = self._session.post(url, expect_json_response=False, files=files, headers=headers).json()
        if 'entries' in file_response:
            file_response = file_response['entries'][0]
        return self.__class__(
            session=self._session,
            object_id=self._object_id,
            response_object=file_response,
        )

    @api_call
    def update_contents(
            self,
            file_path,
            etag=None,
            preflight_check=False,
            preflight_expected_size=0,
            upload_using_accelerator=False,
    ):
        """Upload a new version of a file. The contents are taken from the given file path.

        :param file_path:
            The path of the file that should be uploaded.
        :type file_path:
            `unicode`
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :type etag:
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
        :returns:
            A new file object
        :rtype:
            :class:`File`
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
            )

    @api_call
    def lock(self, prevent_download=False):
        """
        Lock a file, preventing others from modifying (or possibly even downloading) it.

        :param prevent_download:
            Whether or not the lock should prevent other users from downloading the file.
        :type prevent_download:
            `bool`
        :return:
            A new :class:`File` instance reflecting that the file has been locked.
        :rtype:
            :class:`File`
        """
        data = {
            'lock': {
                'is_download_prevented': prevent_download,
                'type': 'lock',
            }
        }
        return self.update_info(data)

    @api_call
    def unlock(self):
        """
        Unlock a file, releasing any restrictions that the lock maintained.

        :return:
            A new :class:`File` instance reflecting that the file has been unlocked.
        :rtype:
            :class:`File`
        """
        data = {'lock': None}
        return self.update_info(data)

    @api_call
    def get_shared_link_download_url(
            self,
            access=None,
            etag=None,
            unshared_at=None,
            allow_preview=None,
            password=None,
    ):
        """
        Get a shared link download url for the file with the given access permissions.
        This url is a direct download url for the file.

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
            The URL of the shared link that allows direct download.
        :rtype:
            `unicode`
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the item.
        """
        item = self.create_shared_link(
            access=access,
            etag=etag,
            unshared_at=unshared_at,
            allow_preview=allow_preview,
            password=password,
        )
        return item.shared_link['download_url']  # pylint:disable=no-member

    @api_call
    def get_comments(self, limit=None, offset=0, fields=None):
        """
        Get the comments on the file.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param offset:
            The index at which to start returning items.
        :type offset:
            `int`
        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the items in the folder.
        :rtype:
            :class:`BoxObjectCollection`
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
    def add_comment(self, message):
        """
        Add a comment to the file.

        :param message:
            The content of the reply comment.
        :type message:
            `unicode`
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
    def create_task(self, message=None, due_at=None):
        """
        Create a task on the given file.

        :param message:
            An optional message to include in the task.
        :type message:
            `unicode` or None
        :param due_at:
            When this task is due.
        :type due_at:
            `unicode` or None
        :return:
            The newly created task
        :rtype:
            :class:`Task`
        """
        url = self._session.get_url('tasks')
        task_attributes = {
            'item': {
                'type': 'file',
                'id': self.object_id
            },
            'action': 'review',
        }
        if message is not None:
            task_attributes['message'] = message
        if due_at is not None:
            task_attributes['due_at'] = due_at
        box_response = self._session.post(url, data=json.dumps(task_attributes))
        response = box_response.json()
        return self.translator.translate(
            session=self._session,
            response_object=response,
        )

    @api_call
    def get_tasks(self, fields=None):
        """
        Get the entries in the file tasks.

        :param fields:
            List of fields to request.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            An iterator of the entries in the file tasks
        :rtype:
            :class:`BoxObjectCollection`
        """
        return MarkerBasedObjectCollection(
            session=self._session,
            url=self.get_url('tasks'),
            limit=None,
            marker=None,
            fields=fields,
            return_full_pages=False,
        )
