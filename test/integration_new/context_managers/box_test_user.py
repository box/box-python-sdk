from typing import Any

from boxsdk.object.user import User
from test.integration_new import util
from test.integration_new import CLIENT


class BoxTestUser:

    def __init__(self, *, name: str = None, login: str = None):
        if name is None:
            name = util.random_name()

        self._user: User = CLIENT.create_user(name=name, login=login)

    def __enter__(self) -> User:
        return self._user

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._user.delete(notify=False, force=True)
