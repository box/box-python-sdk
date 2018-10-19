# coding: utf-8
from __future__ import unicode_literals, absolute_import

import base64
import hashlib
import json

from .base_object import BaseObject
from ..config import API
from ..pagination.chunked_upload_part_limit_offset_based_object_collection import ChunkedUploadPartLimitOffsetBasedObjectCollection


class UploadSession(BaseObject):
    _item_type = 'upload_session'
    _parent_item_type = 'file'

    def get_url(self, *args):
        """
        Base class override. Endpoint is a little different - it's /files/upload_sessions.

        :rtype:
            `unicode`
        """
        return self.session.get_url(
            '{0}s/{1}s'.format(self._parent_item_type, self._item_type),
            self._object_id,
            *args
        ).replace(API.BASE_API_URL, API.UPLOAD_URL)

    def get_parts(self, limit=None, offset=None, fields=None):
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
        :param fields:
            Fields to include on the returned items.
        :type fields:
            `Iterable` of `unicode`
        :returns:
            Returns a `list` of parts uploaded so far.
        :rtype:
            `list` of `dict`
        """
        return ChunkedUploadPartLimitOffsetBasedObjectCollection(
            session=self.session,
            url=self.get_url('parts'),
            limit=limit,
            fields=fields,
            offset=offset,
            return_full_pages=False,
        )

    def upload_part(self, part_bytes, offset, total_size, part_content_sha1=None):
        """
        Upload a part of a file.

        :param part_bytes:
            Part bytes
        :type part_bytes:
            `bytes`
        :param offset:
            Offset, in number of bytes, of the part compared to the beginning of the file.
        :type offset:
            `int`
        :param total_size:
            The size of the file that this part belongs to.
        :type total_size:
            `int`
        :param part_content_sha1:
            SHA-1 hash of the part's content. If not specified, this will be calculated.
        :type part_content_sha1:
            `unicode`
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

        return self._session.put(
            self.get_url(),
            headers={
                'Content-Type': 'application/octet-stream',
                'Digest': 'SHA={0}'.format(base64.b64encode(part_content_sha1).decode('utf-8')),
                'Content-Range': 'bytes {0}-{1}/{2}'.format(offset, range_end, total_size),
            },
            data=part_bytes
        )

    def commit(self, content_sha1, parts=None, file_attributes=None, etag=None):
        """
        Commit a multiput upload.

        :param content_sha1:
            SHA-1 hash of the file contents that was uploaded.
        :type content_sha1:
            `unicode`
        :param parts:
            List of parts that were uploaded.
        :type parts:
            `Iterable` of `dict` or None
        :param file_attributes:
            A `dict` of attributes to set on the uploaded file.
        :type file_attributes:
            `dict`
        :param etag:
            etag lets you ensure that your app only alters files/folders on Box if you have the current version.
        :type etag:
            `unicode` or None
        :returns:
            A :class:`File` object.
        :rtype:
            :class:`File`
        """
        body = {}
        parts_list = []
        if file_attributes is not None:
            body['attributes'] = file_attributes
        if parts is None:
            parts = self.get_parts()
            for part in parts:
                parts_list.append(part)
            body['parts'] = parts_list
        else:
            body['parts'] = parts
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
        return self.translator.translate(entry['type'])(
            session=self.session,
            object_id=entry['id'],
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
        response = self._session.delete(self.get_url())
        return response.ok
