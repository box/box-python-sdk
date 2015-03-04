# coding: utf-8

from __future__ import unicode_literals

import json

from boxsdk.config import API
from .item import Item
from .metadata import Metadata


class File(Item):
    """Box API endpoint for interacting with files."""

    _item_type = 'file'

    @classmethod
    def preflight_check(cls, session, size, name=None, file_id=None, parent_id=None):
        """
        Make an API call to check if certain file can be uploaded to Box or not.
        (https://developers.box.com/docs/#files-preflight-check)

        :param session:
            An instance of :class:`BoxSession` used to make requests.
        :type session:
            :class:`BoxSession`
        :param size:
            The size of the file in bytes. Specify 0 for unknown file-sizes.
        :type size:
            `int`
        :param name:
            The name of the file to be uploaded. This is optional if `file_id` is specified.
            But required for new file uploads.
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
        args = [file_id] if file_id else []
        args.append('content')
        url = cls.get_type_url(*args)
        data = {'size': size}
        if name:
            data['name'] = name
        if parent_id:
            data['parent'] = {'id': parent_id}

        session.options(
            url=url,
            expect_json_response=False,
            data=json.dumps(data),
        )

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

    def update_contents_with_stream(self, file_stream, preflight_check=False, etag=None):
        """
        Upload a new version of a file, taking the contents from the given file stream.

        :param file_stream:
            The file-like object containing the bytes
        :type file_stream:
            `file`
        :param preflight_check:
            Whether or not makes an extra API call before the update to check if the new file stream can be uploaded.
            (https://developers.box.com/docs/#files-preflight-check)
        :type preflight_check:
            `bool`
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :returns:
            A new file object
        :rtype:
            :class:`File`
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the file.
        """
        url = self.get_url('content').replace(API.BASE_API_URL, API.UPLOAD_URL)
        files = {'file': ('unused', file_stream)}
        headers = {'If-Match': etag} if etag is not None else None
        return File(
            session=self._session,
            object_id=self._object_id,
            response_object=self._session.post(url, expect_json_response=False, files=files, headers=headers).json(),
        )

    def update_contents(self, file_path, preflight_check=False, etag=None):
        """Upload a new version of a file. The contents are taken from the given file path.

        :param file_path:
            The path of the file that should be uploaded.
        :type file_path:
            `unicode`
        :param preflight_check:
            Whether or not makes an extra API call before the update to check if the new file stream can be uploaded.
            (https://developers.box.com/docs/#files-preflight-check)
        :type preflight_check:
            `bool`
        :param etag:
            If specified, instruct the Box API to update the item only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :returns:
            A new file object
        :rtype:
            :class:`File`
        :raises: :class:`BoxAPIException` if the specified etag doesn't match the latest version of the file.
        """
        with open(file_path, 'rb') as file_stream:
            return self.update_contents_with_stream(file_stream, preflight_check, etag)

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

    def metadata(self, scope='global', template='properties'):
        """
        Instantiate a :class:`Metadata` object associated with this file.

        :param scope:
            Scope of the metadata. Must be either 'global' or 'enterprise'.
        :type scope:
            `unicode`
        :param template:
            The name of the metadata template. See https://developers.box.com/metadata-api/#basics for more details.
        :type template:
            `unicode`
        :return:
            A new metadata instance associated with this file.
        :rtype:
            :class:`Metadata`
        """
        return Metadata(self._session, self, scope, template)
