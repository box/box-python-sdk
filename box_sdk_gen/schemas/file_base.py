from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class FileBaseTypeField(str, Enum):
    FILE = 'file'


class FileBase(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        id: str,
        *,
        etag: Optional[str] = None,
        type: FileBaseTypeField = FileBaseTypeField.FILE,
        **kwargs
    ):
        """
                :param id: The unique identifier that represent a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
                :type id: str
                :param etag: The HTTP `etag` of this file. This can be used within some API
        endpoints in the `If-Match` and `If-None-Match` headers to only
        perform changes on the file if (no) changes have happened., defaults to None
                :type etag: Optional[str], optional
                :param type: The value will always be `file`., defaults to FileBaseTypeField.FILE
                :type type: FileBaseTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.etag = etag
        self.type = type
