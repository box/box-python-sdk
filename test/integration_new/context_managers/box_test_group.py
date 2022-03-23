from typing import Any

from boxsdk.object.group import Group
from test.integration_new import util
from test.integration_new import CLIENT


class BoxTestGroup:

    def __init__(self, *, name: str = None):
        if name is None:
            name = util.random_name()

        self._group: Group = CLIENT.create_group(name=name)

    def __enter__(self) -> Group:
        return self._group

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._group.delete()
