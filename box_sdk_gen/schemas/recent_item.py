from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.schemas.recent_item_resource import RecentItemResource

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class RecentItemInteractionTypeField(str, Enum):
    ITEM_PREVIEW = 'item_preview'
    ITEM_UPLOAD = 'item_upload'
    ITEM_COMMENT = 'item_comment'
    ITEM_OPEN = 'item_open'
    ITEM_MODIFY = 'item_modify'


class RecentItem(BaseObject):
    def __init__(
        self,
        *,
        type: Optional[str] = None,
        item: Optional[RecentItemResource] = None,
        interaction_type: Optional[RecentItemInteractionTypeField] = None,
        interacted_at: Optional[DateTime] = None,
        interaction_shared_link: Optional[str] = None,
        **kwargs
    ):
        """
                :param type: The value will always be `recent_item`., defaults to None
                :type type: Optional[str], optional
                :param interaction_type: The most recent type of access the user performed on
        the item., defaults to None
                :type interaction_type: Optional[RecentItemInteractionTypeField], optional
                :param interacted_at: The time of the most recent interaction., defaults to None
                :type interacted_at: Optional[DateTime], optional
                :param interaction_shared_link: If the item was accessed through a shared link it will appear here,
        otherwise this will be null., defaults to None
                :type interaction_shared_link: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.item = item
        self.interaction_type = interaction_type
        self.interacted_at = interacted_at
        self.interaction_shared_link = interaction_shared_link
