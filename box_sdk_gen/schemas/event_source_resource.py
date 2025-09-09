from typing import Union

from typing import Dict

from box_sdk_gen.schemas.user import User

from box_sdk_gen.schemas.event_source import EventSource

from box_sdk_gen.schemas.file import File

from box_sdk_gen.schemas.folder import Folder

from box_sdk_gen.schemas.app_item_event_source import AppItemEventSource

from box_sdk_gen.box.errors import BoxSDKError

EventSourceResource = Union[User, EventSource, File, Folder, Dict, AppItemEventSource]
