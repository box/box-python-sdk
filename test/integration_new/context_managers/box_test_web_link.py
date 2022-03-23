from typing import Any, Optional

from test.integration_new import util
from test.integration_new import CLIENT
from boxsdk.object.web_link import WebLink
from boxsdk.object.folder import Folder


class BoxTestWebLink:

    def __init__(self, *, url: str, name: str = None, parent_folder: Optional[Folder] = None):
        if name is None:
            name = util.random_name()
        if parent_folder is None:
            parent_folder = CLIENT.folder('0')
        self._web_link: WebLink = parent_folder.create_web_link(target_url=url, name=name)

    def __enter__(self) -> WebLink:
        return self._web_link

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        util.permanently_delete(self._web_link)
