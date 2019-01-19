from __future__ import unicode_literals, absolute_import

import hashlib

from boxsdk.exception import BoxException


class ChunkedUploader(object):

    def __init__(self, upload_session, content_stream, file_size):
        """
        The initializer for the :class:`ChunkedUploader`

        :param upload_session:
            The upload session for doing the chunked uploader.
        :type upload_session:
            :class:`UploadSession`
        :param content_stream:
            The file-like object to upload.
        :type content_stream:
            :class:`File`
        :param file_size:
            The total size of the file for the chunked upload.
        :type file_size:
            `int`
        :returns:
            An intialized`ChunkedUploader` object.
        :rtype:
            :class:`ChunkedUploader`
        """
        self._upload_session = upload_session
        self._content_stream = content_stream
        self._file_size = file_size
        self._part_array = []
        self._sha1 = hashlib.sha1()
        self._part_definitions = {}
        self._inflight_part = None
        self._is_aborted = False

    def start(self):
        """
        Starts the process of chunk uploading a file.

        :returns:
            An uploaded :class:`File`
        :rtype:
            :class:`File`
        """
        if self._is_aborted:
            raise BoxException('The upload has been previously aborted. Please retry upload with a new upload session.')
        self._upload()
        content_sha1 = self._sha1.digest()
        return self._upload_session.commit(content_sha1=content_sha1, parts=self._part_array)

    def resume(self):
        """
        Resumes the process of chunk uploading a file from where upload failed.

        :returns:
            An uploaded :class:`File`
        :rtype:
            :class:`File`
        """
        if self._is_aborted:
            raise BoxException('The upload has been previously aborted. Please retry upload with a new upload session.')
        parts = self._upload_session.get_parts()
        self._part_array = []
        # Construct a part array that is the first consecutive run of uploaded parts up to an inflight part so resume
        # has a previous state to start from for in process uploads and cross process uploads.
        # Construct a part definition to be used later to determine if a part has been uploaded by offset.
        for part in parts:
            if self._inflight_part and part['offset'] <= self._inflight_part.offset:
                self._part_array.append(part)
            if self._inflight_part and part['offset'] == self._inflight_part.offset:
                self._inflight_part = None
            self._part_definitions[part['offset']] = part
        self._upload()
        content_sha1 = self._sha1.digest()
        return self._upload_session.commit(content_sha1=content_sha1, parts=self._part_array)

    def abort(self):
        """
        Abort an upload session, cancelling the upload and removing any parts that have already been uploaded.

        :returns:
            A boolean indication success of the upload abort.
        :rtype:
            `bool`
        """
        self._content_stream = None
        self._part_array = []
        self._inflight_part = None
        self._is_aborted = True
        return self._upload_session.abort()

    def _upload(self):
        """
        Utility function for looping through all parts of of the upload session and uploading them.
        """
        while len(self._part_array) < self._upload_session.total_parts:
            # Retrieve the part inflight if it exists, if it does not exist then get the next part from the stream.
            next_part = self._inflight_part or self._get_next_part()
            # Set the retrieve part to the current part inflight.
            self._inflight_part = next_part
            self._sha1.update(next_part.chunk)
            # Retrieve the uploaded part if the part has already been uploaded. If not upload the current part.
            uploaded_part = self._part_definitions.get(next_part.offset) or next_part.upload()
            self._inflight_part = None
            # Record that the part has been uploaded.
            self._part_array.append(uploaded_part)
            self._part_definitions[next_part.offset] = uploaded_part

    def _get_next_part(self):
        """
        Retrieves the next :class:`InflightPart` that needs to be uploaded

        :returns:
            The :class:`InflightPart` object to be uploaded next.
        :rtype:
            :class:`InflightPart`
        """
        copied_length = 0
        chunk = b''
        offset = len(self._part_array) * self._upload_session.part_size
        while copied_length < self._upload_session.part_size:
            bytes_read = self._content_stream.read(self._upload_session.part_size - copied_length)
            if bytes_read is None:
                # stream returns none when no bytes are ready currently but there are
                # potentially more bytes in the stream to be read.
                continue
            if not bytes_read:
                # stream is exhausted.
                break
            chunk += bytes_read
            copied_length += len(bytes_read)
        return InflightPart(offset, chunk, self._upload_session, self._file_size)


class InflightPart(object):

    def __init__(self, offset, chunk, upload_session, total_size):
        """
        The initializer for the :class:`InflightPart` object.

        :param offset:
            The offset for the :class:`InflightPart` that represents the position of the part to be uploaded
        :type offset:
            `int`
        :param chunk:
            The chunk in bytes to be uploaded.
        :type chunk:
            `bytes`
        :param upload_session:
            The :class:`UploadSession` for the :class:`InflightPart`.
        :type upload_session:
            :class:`UploadSession`
        :param total_size:
            The total size of the file to be chunked uploaded.
        :type total_size:
            `int`
        """
        self._offset = offset
        self._chunk = chunk
        self._upload_session = upload_session
        self._total_size = total_size

    @property
    def offset(self):
        """
        Getter for the offset of the :class:`InflightPart`
        """
        return self._offset

    @property
    def chunk(self):
        """
        Getter for the chunk of the :class:`InflightPart`
        """
        return self._chunk

    def upload(self):
        """
        Upload method for the :class:`InflightPart`

        :returns:
            The uploaded part record.
        :rtype:
            `dict`
        """
        return self._upload_session.upload_part_bytes(
            part_bytes=self.chunk,
            offset=self.offset,
            total_size=self._total_size
        )
