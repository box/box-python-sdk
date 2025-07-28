from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class WeblinkReferenceV2025R0TypeField(str, Enum):
    WEBLINK = 'weblink'


class WeblinkReferenceV2025R0(BaseObject):
    _discriminator = 'type', {'weblink'}

    def __init__(
        self,
        id: str,
        *,
        type: WeblinkReferenceV2025R0TypeField = WeblinkReferenceV2025R0TypeField.WEBLINK,
        **kwargs
    ):
        """
        :param id: ID of the weblink.
        :type id: str
        :param type: The value will always be `weblink`., defaults to WeblinkReferenceV2025R0TypeField.WEBLINK
        :type type: WeblinkReferenceV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
