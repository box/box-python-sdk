from typing import Optional

from box_sdk_gen.schemas.web_link_base import WebLinkBaseTypeField

from box_sdk_gen.schemas.web_link_base import WebLinkBase

from box_sdk_gen.box.errors import BoxSDKError


class WebLinkMini(WebLinkBase):
    def __init__(
        self,
        id: str,
        *,
        url: Optional[str] = None,
        sequence_id: Optional[str] = None,
        name: Optional[str] = None,
        type: WebLinkBaseTypeField = WebLinkBaseTypeField.WEB_LINK,
        etag: Optional[str] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this web link.
                :type id: str
                :param url: The URL this web link points to., defaults to None
                :type url: Optional[str], optional
                :param name: The name of the web link., defaults to None
                :type name: Optional[str], optional
                :param type: The value will always be `web_link`., defaults to WebLinkBaseTypeField.WEB_LINK
                :type type: WebLinkBaseTypeField, optional
                :param etag: The entity tag of this web link. Used with `If-Match`
        headers., defaults to None
                :type etag: Optional[str], optional
        """
        super().__init__(id=id, type=type, etag=etag, **kwargs)
        self.url = url
        self.sequence_id = sequence_id
        self.name = name
