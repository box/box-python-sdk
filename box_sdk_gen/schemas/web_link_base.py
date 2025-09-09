from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class WebLinkBaseTypeField(str, Enum):
    WEB_LINK = 'web_link'


class WebLinkBase(BaseObject):
    _discriminator = 'type', {'web_link'}

    def __init__(
        self,
        id: str,
        *,
        type: WebLinkBaseTypeField = WebLinkBaseTypeField.WEB_LINK,
        etag: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this web link.
                :type id: str
                :param type: The value will always be `web_link`., defaults to WebLinkBaseTypeField.WEB_LINK
                :type type: WebLinkBaseTypeField, optional
                :param etag: The entity tag of this web link. Used with `If-Match`
        headers., defaults to None
                :type etag: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.etag = etag
