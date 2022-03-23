from typing import Any, Optional

from test.integration_new import util
from test.integration_new import CLIENT
from boxsdk.object.file import File
from boxsdk.object.folder import Folder


class BoxTestFile:

    def __init__(self, *, file_path: str, name: str = None, parent_folder: Optional[Folder] = None):
        if name is None:
            extention = file_path.split('.')[-1]
            name = f'{util.random_name()}.{extention}'
        if parent_folder is None:
            parent_folder = CLIENT.folder('0')
        self._file: File = parent_folder.upload(file_path=file_path, file_name=name)

    def __enter__(self) -> File:
        return self._file

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        util.permanently_delete(self._file)
