from io import SEEK_END
from typing import Iterator, List, Optional, Tuple, Union

from urllib3.fields import RequestField
from urllib3.filepost import choose_boundary

from ..internal.utils import ByteStream

CHUNK_SIZE = 64 * 1024

MultipartField = Tuple[str, Optional[str], Union[str, ByteStream], Optional[str]]


class MultipartStream:
    """
    File-like multipart/form-data body which reads part streams lazily,
    so uploads are sent without buffering whole files in memory.

    Fields are (name, file_name, value, content_type) tuples, where value is
    either a string or a binary stream read from its current position.
    """

    def __init__(self, fields: List[MultipartField]):
        self.boundary = choose_boundary()
        self.content_type = f'multipart/form-data; boundary={self.boundary}'
        self._segments: List[Union[bytes, ByteStream]] = []
        for name, file_name, value, content_type in fields:
            field = RequestField(name=name, data=b'', filename=file_name)
            field.make_multipart(content_type=content_type)
            self._segments.append(
                f'--{self.boundary}\r\n{field.render_headers()}'.encode('utf-8')
            )
            self._segments.append(
                value.encode('utf-8') if isinstance(value, str) else value
            )
            self._segments.append(b'\r\n')
        self._segments.append(f'--{self.boundary}--\r\n'.encode('utf-8'))
        self._index = 0
        self._offset = 0
        # bytes still to send per stream segment, None when the size is unknown
        self._remaining: List[Optional[int]] = [
            None if isinstance(segment, bytes) else self._stream_size(segment)
            for segment in self._segments
        ]
        # requests reads `len` to set Content-Length; None makes it fall back
        # to chunked transfer encoding
        self.len = self._compute_length()

    @staticmethod
    def _stream_size(stream: ByteStream) -> Optional[int]:
        try:
            if not stream.seekable():
                return None
            position = stream.tell()
            size = stream.seek(0, SEEK_END) - position
            stream.seek(position)
            return size
        except (OSError, AttributeError):
            return None

    def _compute_length(self) -> Optional[int]:
        total = 0
        for segment, remaining in zip(self._segments, self._remaining):
            if isinstance(segment, bytes):
                total += len(segment)
            elif remaining is None:
                return None
            else:
                total += remaining
        return total

    def read(self, size: Optional[int] = -1) -> bytes:
        if size is None or size < 0:
            return b''.join(iter(lambda: self.read(CHUNK_SIZE), b''))

        chunks = []
        while size > 0 and self._index < len(self._segments):
            segment = self._segments[self._index]
            if isinstance(segment, bytes):
                chunk = segment[self._offset : self._offset + size]
                self._offset += len(chunk)
                if self._offset >= len(segment):
                    self._index += 1
                    self._offset = 0
            else:
                remaining = self._remaining[self._index]
                if remaining == 0:
                    # send exactly the size declared in Content-Length, even if the stream grew
                    self._index += 1
                    continue
                chunk = segment.read(
                    size if remaining is None else min(size, remaining)
                )
                if not chunk:
                    if remaining is not None:
                        raise IOError(
                            f'Multipart stream ended {remaining} bytes before its declared size'
                        )
                    self._index += 1
                    continue
                if remaining is not None:
                    self._remaining[self._index] = remaining - len(chunk)
            chunks.append(chunk)
            size -= len(chunk)
        return b''.join(chunks)

    def __iter__(self) -> Iterator[bytes]:
        return iter(lambda: self.read(CHUNK_SIZE), b'')

    def __repr__(self) -> str:
        return f'<MultipartStream boundary={self.boundary}>'
