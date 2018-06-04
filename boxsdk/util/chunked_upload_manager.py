# coding: utf-8

from __future__ import unicode_literals, absolute_import

from concurrent.futures import ThreadPoolExecutor, FIRST_EXCEPTION, wait
import hashlib
from threading import Lock

from six import BytesIO


class ChunkedUploadManager(object):
    """
    Class for managing a chunked upload. By default, uploads chunks in parallel using a thread pool.
    """
    executor_factory = ThreadPoolExecutor
    num_workers = 3

    def __init__(self, upload_session, content_stream, file_size):
        """
        :param upload_session:      Upload session to manage.
        :type upload_session:       :class:`ChunkedUploadSession`
        :param content_stream:      File-like object containing the content to be uploaded.
        :type content_stream:       `file`
        :param file_size:           The size of the file that's being uploaded.
        :type file_size:            `int`
        """
        self._session = upload_session
        self._stream = content_stream
        self._total_size = file_size
        self._content_sha1 = hashlib.sha1()
        self._part_queue = self.executor_factory(max_workers=self.num_workers)
        self._get_work_lock = self._lock_factory()
        self._uploaded_parts = {}
        self._work_generator = self._get_next_work_item()
        self._futures = []

    def start(self):
        """
        Start a chunked upload. Uploads each part, then commit. Returns the newly created file.

        :rtype:     :class:`File`
        """
        self._futures = [self._future_factory() for _ in range(self._session.total_parts)]
        wait(self._futures, return_when=FIRST_EXCEPTION)
        for future in self._futures:
            future.cancel()
            if future.exception():
                raise future.exception()
        return self._commit()

    def resume(self):
        """
        Resume a chunked upload. Upload parts that aren't already uploaded, then commit. Returns the newly created file.

        :rtype:     :class:`File`
        """
        parts = self._session.get_parts()
        for part in parts:
            self._uploaded_parts[part['offset']] = part

    def _future_factory(self):
        """
        Factory function for creating :class:`Future` objects representing work items.

        :rtype:     :class:`Future`
        """
        future = self._part_queue.submit(self._upload_next_part)
        future.add_done_callback(self._part_done)
        return future

    def _commit(self):
        """
        Commits the upload.

        :rtype:     :class:`File`
        """
        return self._session.commit(
            [self._uploaded_parts[offset] for offset in sorted(self._uploaded_parts)],
            self._content_sha1.digest(),
        )

    def _get_offsets(self):
        """
        Generator over part offsets that need to be uploaded.

        :ytype:         `int`
        """
        offset = 0
        while offset <= self._total_size:
            if offset not in self._uploaded_parts:
                yield min(offset, self._total_size)
            offset += self._session.part_size

    def _get_next_work_item(self):
        """
        Generator over work items.

        Uploading a part requires 3 dynamic things:

        * offset indicating which part is being uploaded; the number of bytes from the beginning of the file
        * stream containing the content of the part; a file-like object
        * sha1 containing the hash of the content of the part

        This generator yields 3-tuples containing these things.

        :ytype:     (`int`, :class:`BytesIO`, `unicode`)
        """
        for offset in self._get_offsets():
            stream, sha1 = self._get_next_part_stream_and_sha1()
            yield offset, stream, sha1

    def _get_next_part_stream_and_sha1(self):
        """
        Get a content stream containing the content for the next part to upload, and the SHA-1 hash of that content.

        Tries to read part_size bytes from the underlying stream, but if fewer bytes than that are available, that's
        OK for the last chunk.

        Also, updates the SHA-1 hash that will be sent with the commit call.

        :rtype:     (:class:`BytesIO`, `unicode`)
        """
        part_buffer = BytesIO()
        copied_length = 0
        sha1 = hashlib.sha1()
        while copied_length < self._session.part_size:
            # Reading from a stream can be a bit tricky: we're guaranteed to get no more than the number of bytes
            # requested, but we can receive fewer. If we get 0 bytes, then we know we're at the end of the stream,
            # but if we get None, we need to try again.
            chunk = self._stream.read(self._session.part_size - copied_length)
            if chunk is None:
                continue
            if len(chunk) == 0:  # pylint:disable=len-as-condition
                break
            copied_length += len(chunk)
            part_buffer.write(chunk)
            sha1.update(chunk)
            self._content_sha1.update(chunk)
        part_buffer.seek(0)
        return part_buffer, sha1.digest()

    def _upload_next_part(self):
        """
        Called by worker threads to upload the next part.

        While holding a lock, gets the next work item. This guarantees that only one thread tries to read from the
        file at once, and that the file is read in order, which lets us hash the parts and the entire file with just
        one read of the underlying stream.
        """
        with self._get_work_lock:
            offset, stream, sha1 = next(self._work_generator)
        return self._session.upload_part(stream, offset, self._total_size, sha1)

    def _part_done(self, future):
        """
        Callback for when a part is finished uploading. Save the part JSON so it can be sent with the commit call.

        :param future:      Future object containing the result of the part upload.
        :type future:       :class:`Future`
        """
        part = future.result()['part']
        offset = part['offset']
        self._uploaded_parts[offset] = part

    @staticmethod
    def _lock_factory():
        return Lock()
