# coding: utf-8
from __future__ import unicode_literals, absolute_import

import base64
import hashlib
import json
import os

from boxsdk.util.chunked_uploader import ChunkedUploader
from .base_object import BaseObject
from ..pagination.limit_offset_based_dict_collection import LimitOffsetBasedDictCollection


class UploadSession(BaseObject):
    _item_type = 'upload_session'
    _parent_item_type = 'file'

    def get_url(self, *args):
        """
        Base class override. Endpoint is a little different - it's /files/upload_sessions.

        :rtype:
            `unicode`
        """
        return self._session.get_url(
            '{0}s/{1}s'.format(self._parent_item_type, self._item_type),
            self._object_id,
            *args
        ).replace(self.session.api_config.BASE_API_URL, self.session.api_config.UPLOAD_URL)

    def get_parts(self, limit=None, offset=None):
        """
        Get a list of parts uploaded so far.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :type limit:
            `int` or None
        :param offset:
            The index at which to start returning items.
        :type offset:
            `int` or None
        :returns:
            Returns a :class:`BoxObjectCollection` object containing the uploaded parts.
        :rtype:
            :class:`BoxObjectCollection`
        """
        return LimitOffsetBasedDictCollection(
            session=self.session,
            url=self.get_url('parts'),
            limit=limit,
            offset=offset,
            fields=None,
            return_full_pages=False,
        )

    def upload_part_bytes(self, part_bytes, offset, total_size, part_content_sha1=None):
        """
        Upload a part of a file.

        :param part_bytes:
            Part bytes
        :type part_bytes:
            `bytes`
        :param offset:
            Offset, in number of bytes, of the part compared to the beginning of the file. This number should be a
            multiple of the part size.
        :type offset:
            `int`
        :param total_size:
            The size of the file that this part belongs to.
        :type total_size:
            `int`
        :param part_content_sha1:
            SHA-1 hash of the part's content. If not specified, this will be calculated.
        :type part_content_sha1:
            `bytes` or None
        :returns:
            The uploaded part record.
        :rtype:
            `dict`
        """

        if part_content_sha1 is None:
            sha1 = hashlib.sha1()
            sha1.update(part_bytes)
            part_content_sha1 = sha1.digest()

        range_end = min(offset + self.part_size - 1, total_size - 1)  # pylint:disable=no-member
        headers = {
            'Content-Type': 'application/octet-stream',
            'Digest': 'SHA={0}'.format(base64.b64encode(part_content_sha1).decode('utf-8')),
            'Content-Range': 'bytes {0}-{1}/{2}'.format(offset, range_end, total_size),
        }
        response = self._session.put(
            self.get_url(),
            headers=headers,
            data=part_bytes,
        )
        return response.json()['part']

    def commit(self, content_sha1, parts=None, file_attributes=None, etag=None):
        """
        Commit a multiput upload.

        :param content_sha1:
            SHA-1 hash of the file contents that was uploaded.
        :type content_sha1:
            `bytes`
        :param parts:
            List of parts that were uploaded.
        :type parts:
            `Iterable` of `dict` or None
        :param file_attributes:
            A `dict` of attributes to set on the uploaded file.
        :type file_attributes:
            `dict`
        :param etag:
            If specified, instruct the Box API to delete the folder only if the current version's etag matches.
        :type etag:
            `unicode` or None
        :returns:
            The newly-uploaded file object.
        :rtype:
            :class:`File`
        """
        body = {}
        if file_attributes is not None:
            body['attributes'] = file_attributes
        if parts is not None:
            body['parts'] = parts
        else:
            body['parts'] = [part for part in self.get_parts()]
        headers = {
            'Content-Type': 'application/json',
            'Digest': 'SHA={0}'.format(base64.b64encode(content_sha1).decode('utf-8')),
        }
        if etag is not None:
            headers['If-Match'] = etag
        response = self._session.post(
            self.get_url('commit'),
            headers=headers,
            data=json.dumps(body),
        ).json()
        entry = response['entries'][0]
        return self.translator.translate(
            session=self._session,
            response_object=entry,
        )

    def abort(self):
        """
        Abort an upload session, cancelling the upload and removing any parts that have already been uploaded.

        :returns:
            A boolean indication success of the upload abort.
        :rtype:
            `bool`
        """
        return self.delete()

    def get_chunked_uploader_for_stream(self, content_stream, file_size):
        """
        Instantiate the chunked upload instance and create upload session.

        :param content_stream:
            File-like object containing the content of the part to be uploaded.
        :type content_stream:
            :class:`File`
        :param file_size:
            The size of the file that this part belongs to.
        :type file_size:
            `int`
        :returns:
            A :class:`ChunkedUploader` object.
        :rtype:
            :class:`ChunkedUploader`
        """
        return ChunkedUploader(self, content_stream, file_size)

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
        return self.get_chunked_uploader_for_stream(
            content_stream=content_stream,
            file_size=total_size,
        )
