from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.schemas.group_mini import GroupMini

from box_sdk_gen.box.errors import BoxSDKError


class AppItemEventSourceTypeField(str, Enum):
    APP_ITEM = 'app_item'


class AppItemEventSource(BaseObject):
    _discriminator = 'type', {'app_item'}

    def __init__(
        self,
        id: str,
        app_item_type: str,
        *,
        type: AppItemEventSourceTypeField = AppItemEventSourceTypeField.APP_ITEM,
        user: Optional[UserMini] = None,
        group: Optional[GroupMini] = None,
        **kwargs
    ):
        """
        :param id: The id of the `AppItem`.
        :type id: str
        :param app_item_type: The type of the `AppItem`.
        :type app_item_type: str
        :param type: The type of the source that this event represents. Can only be `app_item`., defaults to AppItemEventSourceTypeField.APP_ITEM
        :type type: AppItemEventSourceTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.app_item_type = app_item_type
        self.type = type
        self.user = user
        self.group = group
