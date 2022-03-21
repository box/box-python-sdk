import os.path
import uuid
import warnings
from pathlib import Path

from test.integration_new import CLIENT
from boxsdk.exception import BoxAPIException
from boxsdk.object.base_item import BaseItem


def permanently_delete(item: BaseItem):
    item.delete(recursive=True)
    try:
        CLIENT.trash().permanently_delete_item(item)
    except BoxAPIException:
        warnings.warn(
            f"Unable to permanently remove {item.type}: {item.id} from trash. Probably this item is under retention.",
            category=RuntimeWarning,
            stacklevel=2
        )


def get_current_dir_path() -> str:
    return str(Path(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))))


def get_file_path(file_name: str) -> str:
    return str(Path(f"{os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))}/resources/{file_name}"))


def random_name():
    return str(uuid.uuid4())
