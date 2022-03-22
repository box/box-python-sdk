import os
from typing import Any

from test.integration_new import util


class LocalLargeFile:

    def __init__(self, *, name: str = None):
        if name is None:
            name = util.random_name()
        with open(name, 'wb') as f:
            f.seek(1024 * 1024 * 21)
            f.write(b'0')
        self.path = name

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if os.path.exists(self.path):
            os.remove(self.path)
