from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class AppItemTypeField(str, Enum):
    APP_ITEM = 'app_item'


class AppItem(BaseObject):
    _discriminator = 'type', {'app_item'}

    def __init__(
        self,
        id: str,
        application_type: str,
        *,
        type: AppItemTypeField = AppItemTypeField.APP_ITEM,
        **kwargs
    ):
        """
        :param id: The unique identifier for this app item.
        :type id: str
        :param application_type: The type of the app that owns this app item.
        :type application_type: str
        :param type: The value will always be `app_item`., defaults to AppItemTypeField.APP_ITEM
        :type type: AppItemTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.application_type = application_type
        self.type = type
