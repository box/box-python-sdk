# coding: utf-8

from __future__ import unicode_literals, absolute_import

import base64
import hashlib
import json

from .base_object import BaseObject
from ..util.api_call_decorator import api_call


class ChunkedUploadSession(BaseObject):
    _item_type = 'upload_session'
    _parent_item_type = 'file'

    def get_url(self, *args):
        """
        Base class override. Endpoint is a little different - it's /files/upload_sessions.
        """
        return self.session.get_url(
            '{0}s/{1}s'.format(self._parent_item_type, self._item_type),
            self._object_id,
            *args
        ).replace(self.session.api_config.BASE_API_URL, self.session.api_config.UPLOAD_URL)

    @api_call
    def get_parts(self):
        """
        Get a list of parts uploaded so far.

        :rtype:     `list` of `dict`
        """
        response = self.session.get(self.get_url('parts')).json()
        return response.entries

    def _calculate_part_sha1(self, content_stream):
        content_sha1 = hashlib.sha1()
        stream_position = content_stream.tell()
        hashed_length = 0
        while hashed_length < self.part_size:  # pylint:disable=no-member
            chunk = content_stream.read(self.part_size - hashed_length)  # pylint:disable=no-member
            if chunk is None:
                continue
            if len(chunk) == 0:  # pylint:disable=len-as-condition
                break
            hashed_length += len(chunk)
            content_sha1.update(chunk)
        content_stream.seek(stream_position)
        return content_sha1.digest()

    @api_call
    def upload_part(self, content_stream, offset, total_size, part_content_sha1=None):
        """
        Upload a part of a file.

        :param content_stream:      File-like object containing the content of the part to be uploaded.
        :type content_stream:       :class:`File`
        :param offset:              Offset, in number of bytes, of the part compared to the beginning of the file.
        :type offset:               `int`
        :param total_size:          The size of the file that this part belongs to.
        :type total_size:           `int`
        :param part_content_sha1:   SHA-1 hash of the part's content. If not specified, this will be calculated.
        :type part_content_sha1:    `unicode`
        :rtype:                     `dict`
        """
        if part_content_sha1 is None:
            part_content_sha1 = self._calculate_part_sha1(content_stream)

        range_end = min(offset + self.part_size - 1, total_size - 1)  # pylint:disable=no-member

        return self._session.put(
            self.get_url(),
            headers={
                'Content-Type': 'application/octet-stream',
                'Digest': 'SHA={0}'.format(base64.b64encode(part_content_sha1).decode('utf-8')),
                'Content-Range': 'bytes {0}-{1}/{2}'.format(offset, range_end, total_size),
            },
            data=content_stream,
        ).json()

    @api_call
    def commit(self, parts, content_sha1):
        """
        Commit a multiput upload.

        :param parts:           List of parts that were uploaded.
        :type parts:            `Iterable` of `dict`
        :param content_sha1:    SHA-1 has of the file contents that was uploaded.
        :type content_sha1:     `unicode`
        :rtype:                 :class:`File`
        """
        response = self._session.post(
            self.get_url('commit'),
            headers={
                'Content-Type': 'application/json',
                'Digest': 'SHA={0}'.format(base64.b64encode(content_sha1).decode('utf-8')),
            },
            data=json.dumps({'parts': parts}),
        ).json()
        entry = response['entries'][0]
        return self.session.translator.translate('file')(self.session, entry['id'], entry)
