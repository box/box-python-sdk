from __future__ import unicode_literals, absolute_import

import base64
import hashlib
import json

from .base_object import BaseObject
from ..pagination.limit_offset_based_dict_collection import LimitOffsetBasedDictCollection

class ChunkedUpload(object):
    _item_type = 'chunked_upload'

    def __init__(self, upload_session, content_stream, file_size):
        self._upload_session = upload_session
        self._content_stream = content_stream
        self._file_size = file_size

    # def get_url(self, *args):
    #     """
    #     Base class override. Endpoint is a little different - it's /files/upload_sessions.

    #     :rtype:
    #         `unicode`
    #     """
    #     return self._session.get_url(
    #         '{0}s/{1}s'.format(self._parent_item_type, self._item_type),
    #         self._object_id,
    #         *args
    #     ).replace(self.session.api_config.BASE_API_URL, self.session.api_config.UPLOAD_URL)

    def start(self):
        part_array = []
        sha1 = hashlib.sha1()
        for part_num in range(self._upload_session.total_parts):
            copied_length = 0
            chunk = b''
            while copied_length < self._upload_session.part_size:
                bytes_read = self._content_stream.read(self._upload_session.part_size - copied_length)
                if bytes_read is None:
                    # stream returns none when no bytes are ready currently but there are
                    # potentially more bytes in the stream to be read.
                    continue
                if len(bytes_read) == 0:
                    # stream is exhausted.
                    break
                chunk += bytes_read
                copied_length += len(bytes_read)

            uploaded_part = self._upload_session.upload_part_bytes(chunk, part_num*self._upload_session.part_size,
                                                                   self._file_size)
            part_array.append(uploaded_part)
            sha1.update(chunk)
        content_sha1 = sha1.digest()
        self._upload_session.commit(content_sha1=content_sha1, parts=part_array)
