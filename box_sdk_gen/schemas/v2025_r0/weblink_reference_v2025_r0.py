from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class WeblinkReferenceV2025R0TypeField(str, Enum):
    WEB_LINK = 'web_link'


class WeblinkReferenceV2025R0(BaseObject):
    _discriminator = 'type', {'web_link'}

    def __init__(
        self,
        id: str,
        *,
        type: WeblinkReferenceV2025R0TypeField = WeblinkReferenceV2025R0TypeField.WEB_LINK,
        **kwargs
    ):
        """
        :param id: ID of the web link.
        :type id: str
        :param type: The value will always be `web_link`., defaults to WeblinkReferenceV2025R0TypeField.WEB_LINK
        :type type: WeblinkReferenceV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
