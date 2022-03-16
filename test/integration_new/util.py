import os.path
import random
import string
from pathlib import Path

from boxsdk.object.folder import Folder
from boxsdk.object.base_item import BaseItem
from test.integration_new import client


def permanently_delete(item: BaseItem):
    item.delete(recursive=True)
    client.trash().permanently_delete_item(item)


def permanently_delete_folder(folder: Folder):
    folder.delete(recursive=True)
    client.trash().permanently_delete_item(folder)


def get_file_path(file_name: str) -> str:
    return str(Path(f"{os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))}/resources/{file_name}"))


def random_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
