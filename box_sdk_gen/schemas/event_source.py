from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError


class EventSourceItemTypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'


class EventSourceClassificationField(BaseObject):
    def __init__(self, *, name: Optional[str] = None, **kwargs):
        """
        :param name: The classification's name., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.name = name


class EventSource(BaseObject):
    _discriminator = 'item_type', {'file', 'folder'}

    def __init__(
        self,
        item_type: EventSourceItemTypeField,
        item_id: str,
        item_name: str,
        *,
        classification: Optional[EventSourceClassificationField] = None,
        parent: Optional[FolderMini] = None,
        owned_by: Optional[UserMini] = None,
        **kwargs
    ):
        """
                :param item_type: The type of the item that the event
        represents. Can be `file` or `folder`.
                :type item_type: EventSourceItemTypeField
                :param item_id: The unique identifier that represents the
        item.
                :type item_id: str
                :param item_name: The name of the item.
                :type item_name: str
                :param classification: The object containing classification information for the item that
        triggered the event. This field will not appear if the item does not
        have a classification set., defaults to None
                :type classification: Optional[EventSourceClassificationField], optional
        """
        super().__init__(**kwargs)
        self.item_type = item_type
        self.item_id = item_id
        self.item_name = item_name
        self.classification = classification
        self.parent = parent
        self.owned_by = owned_by
