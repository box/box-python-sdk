import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from threading import Lock
from typing import IO, TYPE_CHECKING, Optional, List

from boxsdk.exception import BoxException
from boxsdk.config import API

if TYPE_CHECKING:
    from boxsdk.object.file import File
    from boxsdk.object.upload_session import UploadSession


class ChunkedUploader:

    def __init__(self, upload_session: 'UploadSession', content_stream: IO[bytes], file_size: int):
        """
        The initializer for the :class:`ChunkedUploader`

        :param upload_session:
            The upload session for doing the chunked uploader.
        :param content_stream:
            The file-like object to upload.
        :param file_size:
            The total size of the file for the chunked upload.
        :returns:
            An intialized`ChunkedUploader` object.
        """
        self._upload_session = upload_session
        self._content_stream = content_stream
        self._file_size = file_size
        self._part_array = []
        self._sha1 = hashlib.sha1()
        self._part_definitions = {}
        self._is_aborted = False
        self._lock = Lock()
        self._inflight_parts = {}
        self._chunk_index = 0
        self._executor = ThreadPoolExecutor(max_workers=API.CHUNK_UPLOAD_THREADS)

    def start(self) -> Optional['File']:
        """
        Starts the process of chunk uploading a file. Should return file. If commit was not processed will return None.
        You can call ChunkedUploader.resume to retry committing upload.

        :returns:
            An uploaded :class:`File` or None if session was not processed
        """
        if self._is_aborted:
            raise BoxException('The upload has been previously aborted. Please retry upload with a new upload session.')

        futures = [self._executor.submit(self._upload_part) for _ in range(self._upload_session.total_parts)]
        self._upload(futures)
        return self._commit_and_erase_stream_reference_when_succeed()

    def resume(self) -> Optional['File']:
        """
        Resumes the process of chunk uploading a file from where upload failed.
        Should return file. If commit was not processed will return None.
        You can call ChunkedUploader.resume to retry committing upload.

        :returns:
            An uploaded :class:`File` or None if session was not processed
        """
        if self._is_aborted:
            raise BoxException('The upload has been previously aborted. Please retry upload with a new upload session.')

        self._executor = ThreadPoolExecutor(max_workers=API.CHUNK_UPLOAD_THREADS)
        parts = self._upload_session.get_parts()
        for part in parts:
            self._part_definitions[part['offset']] = part

        with self._lock:
            futures = [self._executor.submit(lambda item=part: self._upload_part(item)) for part in self._inflight_parts.values()]
            for _ in range(self._upload_session.total_parts - self._chunk_index - len(self._inflight_parts)):
                futures.append(self._executor.submit(self._upload_part))

        self._upload(futures)
        return self._commit_and_erase_stream_reference_when_succeed()

    def abort(self) -> bool:
        """
        Abort an upload session, cancelling the upload and removing any parts that have already been uploaded.

        :returns:
            A boolean indication success of the upload abort.
        """
        self._content_stream = None
        self._part_definitions = {}
        self._inflight_parts = {}
        self._is_aborted = True
        return self._upload_session.abort()

    def _upload(self, futures: List[Future]) -> None:
        """
        Utility function for looping through all parts of the upload session and uploading them.
        """
        try:
            for future in as_completed(futures):
                future.result()
        except Exception as exc:
            self._executor.shutdown(wait=True)
            raise exc

        self._part_array = sorted(self._part_definitions.values(), key=lambda part: part['offset'])

    def _upload_part(self, task=None):
        if isinstance(task, InflightPart):
            next_part = task
        else:
            with self._lock:
                next_part = self._get_next_part()
                self._sha1.update(next_part.chunk)

        with self._lock:
            if self._part_definitions.get(next_part.offset):
                return
            self._inflight_parts[next_part.offset] = next_part

        uploaded_part = next_part.upload()

        with self._lock:
            self._part_definitions[next_part.offset] = uploaded_part
            del self._inflight_parts[next_part.offset]

    def _get_next_part(self) -> 'InflightPart':
        """
        Retrieves the next :class:`InflightPart` that needs to be uploaded

        :returns:
            The :class:`InflightPart` object to be uploaded next.
        """
        copied_length = 0
        chunk = b''
        offset = self._chunk_index * self._upload_session.part_size
        self._chunk_index += 1
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

    def _commit_and_erase_stream_reference_when_succeed(self):
        content_sha1 = self._sha1.digest()
        commit_result = self._upload_session.commit(content_sha1=content_sha1, parts=self._part_array)
        # Remove file stream reference when uploading file succeeded
        if commit_result is not None:
            self._content_stream = None
        self._executor.shutdown(wait=True)
        return commit_result


class InflightPart:

    def __init__(self, offset: int, chunk: bytes, upload_session: 'UploadSession', total_size: int):
        """
        The initializer for the :class:`InflightPart` object.

        :param offset:
            The offset for the :class:`InflightPart` that represents the position of the part to be uploaded
        :param chunk:
            The chunk in bytes to be uploaded.
        :param upload_session:
            The :class:`UploadSession` for the :class:`InflightPart`.
        :param total_size:
            The total size of the file to be chunked uploaded.
        """
        self._offset = offset
        self._chunk = chunk
        self._upload_session = upload_session
        self._total_size = total_size

    @property
    def offset(self) -> int:
        """
        Getter for the offset of the :class:`InflightPart`
        """
        return self._offset

    @property
    def chunk(self) -> bytes:
        """
        Getter for the chunk of the :class:`InflightPart`
        """
        return self._chunk

    def upload(self) -> dict:
        """
        Upload method for the :class:`InflightPart`

        :returns:
            The uploaded part record.
        """
        return self._upload_session.upload_part_bytes(
            part_bytes=self.chunk,
            offset=self.offset,
            total_size=self._total_size
        )
