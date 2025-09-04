from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class HubBaseV2025R0TypeField(str, Enum):
    HUBS = 'hubs'


class HubBaseV2025R0(BaseObject):
    _discriminator = 'type', {'hubs'}

    def __init__(
        self,
        id: str,
        *,
        type: HubBaseV2025R0TypeField = HubBaseV2025R0TypeField.HUBS,
        **kwargs
    ):
        """
                :param id: The unique identifier that represent a Box Hub.

        The ID for any Box Hub can be determined
        by visiting a Box Hub in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/hubs/123`
        the `hub_id` is `123`.
                :type id: str
                :param type: The value will always be `hubs`., defaults to HubBaseV2025R0TypeField.HUBS
                :type type: HubBaseV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
