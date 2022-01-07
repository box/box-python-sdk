# coding: utf-8
import base64
import hashlib
import json
import os
from typing import Any, Optional, TYPE_CHECKING, Iterable, IO

from boxsdk.util.api_call_decorator import api_call
from boxsdk.util.chunked_uploader import ChunkedUploader
from .base_object import BaseObject
from ..pagination.limit_offset_based_dict_collection import LimitOffsetBasedDictCollection

if TYPE_CHECKING:
    from boxsdk.pagination.box_object_collection import BoxObjectCollection
    from boxsdk.object.file import File


class UploadSession(BaseObject):
    _item_type = 'upload_session'
    _parent_item_type = 'file'

    def get_url(self, *args: Any) -> str:
        """
        Base class override. Endpoint is a little different - it's /files/upload_sessions.
        """
        return self._session.get_url(
            f'{self._parent_item_type}s/{self._item_type}s',
            self._object_id,
            *args
        ).replace(self.session.api_config.BASE_API_URL, self.session.api_config.UPLOAD_URL)

    @api_call
    def get_parts(self, limit: Optional[int] = None, offset: Optional[int] = None) -> 'BoxObjectCollection':
        """
        Get a list of parts uploaded so far.

        :param limit:
            The maximum number of items to return per page. If not specified, then will use the server-side default.
        :param offset:
            The index at which to start returning items.
        :returns:
            Returns a :class:`BoxObjectCollection` object containing the uploaded parts.
        """
        return LimitOffsetBasedDictCollection(
            session=self.session,
            url=self.get_url('parts'),
            limit=limit,
            offset=offset,
            fields=None,
            return_full_pages=False,
        )

    @api_call
    def upload_part_bytes(
            self,
            part_bytes: bytes,
            offset: int,
            total_size: int,
            part_content_sha1: Optional[bytes] = None
    ) -> dict:
        """
        Upload a part of a file.

        :param part_bytes:
            Part bytes
        :param offset:
            Offset, in number of bytes, of the part compared to the beginning of the file. This number should be a
            multiple of the part size.
        :param total_size:
            The size of the file that this part belongs to.
        :param part_content_sha1:
            SHA-1 hash of the part's content. If not specified, this will be calculated.
        :returns:
            The uploaded part record.
        """

        if part_content_sha1 is None:
            sha1 = hashlib.sha1()
            sha1.update(part_bytes)
            part_content_sha1 = sha1.digest()

        range_end = min(offset + self.part_size - 1, total_size - 1)  # pylint:disable=no-member
        headers = {
            'Content-Type': 'application/octet-stream',
            'Digest': f'SHA={base64.b64encode(part_content_sha1).decode("utf-8")}',
            'Content-Range': f'bytes {offset}-{range_end}/{total_size}',
        }
        response = self._session.put(
            self.get_url(),
            headers=headers,
            data=part_bytes,
        )
        return response.json()['part']

    @api_call
    def commit(
            self,
            content_sha1: bytes,
            parts: Iterable[Optional[dict]] = None,
            file_attributes: dict = None,
            etag: Optional[str] = None
    ) -> 'File':
        """
        Commit a multiput upload.

        :param content_sha1:
            SHA-1 hash of the file contents that was uploaded.
        :param parts:
            List of parts that were uploaded.
        :param file_attributes:
            A `dict` of attributes to set on the uploaded file.
        :param etag:
            If specified, instruct the Box API to delete the folder only if the current version's etag matches.
        :returns:
            The newly-uploaded file object.
        """
        body = {}
        if file_attributes is not None:
            body['attributes'] = file_attributes
        if parts is not None:
            body['parts'] = parts
        else:
            body['parts'] = list(self.get_parts())
        headers = {
            'Content-Type': 'application/json',
            'Digest': f'SHA={base64.b64encode(content_sha1).decode("utf-8")}',
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

    @api_call
    def abort(self) -> bool:
        """
        Abort an upload session, cancelling the upload and removing any parts that have already been uploaded.

        :returns:
            A boolean indication success of the upload abort.
        """
        return self.delete()

    def get_chunked_uploader_for_stream(self, content_stream: IO[bytes], file_size: int) -> ChunkedUploader:
        """
        Instantiate the chunked upload instance and create upload session.

        :param content_stream:
            File-like object containing the content of the part to be uploaded.
        :param file_size:
            The size of the file that this part belongs to.
        :returns:
            A :class:`ChunkedUploader` object.
        """
        return ChunkedUploader(self, content_stream, file_size)

    def get_chunked_uploader(self, file_path: str) -> ChunkedUploader:
        """
        Instantiate the chunked upload instance and create upload session with path to file.

        :param file_path:
            The local path to the file you wish to upload.
        :returns:
            A :class:`ChunkedUploader` object.
        """
        total_size = os.stat(file_path).st_size
        with open(file_path, 'rb') as content_stream:
            return self.get_chunked_uploader_for_stream(
                content_stream=content_stream,
                file_size=total_size,
            )
