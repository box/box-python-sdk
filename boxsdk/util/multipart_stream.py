from io import BytesIO
from typing import Any

from box_sdk_gen.networking.multipart_stream import (
    MultipartField,
    MultipartStream as _MultipartStream,
)


class MultipartStream(_MultipartStream):
    """
    Streaming multipart/form-data body that ensures that data is encoded before files.
    This allows a server to process information in the data before receiving the file bytes.
    File streams are read lazily, so uploads are sent without loading whole files in memory.

    Field values are either a string, bytes or a binary stream, or a
    (file_name, value) or (file_name, value, content_type) tuple.
    """

    def __init__(self, data: dict, files: dict):
        super().__init__(
            [self._to_field(name, value) for name, value in data.items()]
            + [self._to_field(name, value) for name, value in files.items()]
        )

    @staticmethod
    def _to_field(name: str, value: Any) -> MultipartField:
        file_name, content_type = None, None
        if isinstance(value, tuple):
            file_name, value, *rest = value
            content_type = rest[0] if rest else None
        if isinstance(value, bytes):
            value = BytesIO(value)
        return name, file_name, value, content_type
