from typing import Any, Iterable

from test.integration_new import CLIENT
from boxsdk.object.web_link import WebLink


class BoxTestSignRequest:

    def __init__(self, *, files: Iterable, signers: Iterable, parent_folder_id: str):
        self._sign_request = CLIENT.create_sign_request(files, signers, parent_folder_id)

    def __enter__(self) -> WebLink:
        return self._sign_request

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._sign_request.cancel()
