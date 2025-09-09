from typing import Optional

from typing import Dict

from box_sdk_gen.schemas.file_base import FileBaseTypeField

from box_sdk_gen.schemas.file_base import FileBase

from box_sdk_gen.schemas.file_version_mini import FileVersionMini

from box_sdk_gen.box.errors import BoxSDKError


class FileMini(FileBase):
    _fields_to_json_mapping: Dict[str, str] = {
        'sha_1': 'sha1',
        **FileBase._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'sha1': 'sha_1',
        **FileBase._json_to_fields_mapping,
    }

    def __init__(
        self,
        id: str,
        *,
        sequence_id: Optional[str] = None,
        name: Optional[str] = None,
        sha_1: Optional[str] = None,
        file_version: Optional[FileVersionMini] = None,
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
                :param name: The name of the file., defaults to None
                :type name: Optional[str], optional
                :param sha_1: The SHA1 hash of the file. This can be used to compare the contents
        of a file on Box with a local file., defaults to None
                :type sha_1: Optional[str], optional
                :param etag: The HTTP `etag` of this file. This can be used within some API
        endpoints in the `If-Match` and `If-None-Match` headers to only
        perform changes on the file if (no) changes have happened., defaults to None
                :type etag: Optional[str], optional
                :param type: The value will always be `file`., defaults to FileBaseTypeField.FILE
                :type type: FileBaseTypeField, optional
        """
        super().__init__(id=id, etag=etag, type=type, **kwargs)
        self.sequence_id = sequence_id
        self.name = name
        self.sha_1 = sha_1
        self.file_version = file_version
