from typing import Any, Optional

from test.integration_new import util
from test.integration_new import CLIENT
from boxsdk.object.folder import Folder


class BoxTestFolder:

    def __init__(self, *, name: str = None, parent_folder: Optional[Folder] = None):
        if name is None:
            name = util.random_name()
        if parent_folder is None:
            parent_folder = CLIENT.root_folder()
        self._folder: Folder = parent_folder.create_subfolder(name=name)

    def __enter__(self) -> Folder:
        return self._folder

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        util.permanently_delete(self._folder)
