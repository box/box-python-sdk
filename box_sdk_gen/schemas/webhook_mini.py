from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class WebhookMiniTypeField(str, Enum):
    WEBHOOK = 'webhook'


class WebhookMiniTargetTypeField(str, Enum):
    FILE = 'file'
    FOLDER = 'folder'


class WebhookMiniTargetField(BaseObject):
    _discriminator = 'type', {'file', 'folder'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[WebhookMiniTargetTypeField] = None,
        **kwargs
    ):
        """
        :param id: The ID of the item to trigger a webhook., defaults to None
        :type id: Optional[str], optional
        :param type: The type of item to trigger a webhook., defaults to None
        :type type: Optional[WebhookMiniTargetTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class WebhookMini(BaseObject):
    _discriminator = 'type', {'webhook'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[WebhookMiniTypeField] = None,
        target: Optional[WebhookMiniTargetField] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this webhook., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `webhook`., defaults to None
        :type type: Optional[WebhookMiniTypeField], optional
        :param target: The item that will trigger the webhook., defaults to None
        :type target: Optional[WebhookMiniTargetField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.target = target
