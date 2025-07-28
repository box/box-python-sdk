from typing import Optional

from typing import Dict

from box_sdk_gen.schemas.file_version_base import FileVersionBaseTypeField

from box_sdk_gen.schemas.file_version_base import FileVersionBase

from box_sdk_gen.box.errors import BoxSDKError


class FileVersionMini(FileVersionBase):
    _fields_to_json_mapping: Dict[str, str] = {
        'sha_1': 'sha1',
        **FileVersionBase._fields_to_json_mapping,
    }
    _json_to_fields_mapping: Dict[str, str] = {
        'sha1': 'sha_1',
        **FileVersionBase._json_to_fields_mapping,
    }

    def __init__(
        self,
        id: str,
        *,
        sha_1: Optional[str] = None,
        type: FileVersionBaseTypeField = FileVersionBaseTypeField.FILE_VERSION,
        **kwargs
    ):
        """
        :param id: The unique identifier that represent a file version.
        :type id: str
        :param sha_1: The SHA1 hash of this version of the file., defaults to None
        :type sha_1: Optional[str], optional
        :param type: The value will always be `file_version`., defaults to FileVersionBaseTypeField.FILE_VERSION
        :type type: FileVersionBaseTypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.sha_1 = sha_1
