from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class HubDocumentPageV2025R0(BaseObject):
    def __init__(
        self,
        id: str,
        type: str,
        title_fragment: str,
        *,
        parent_id: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this page.
        :type id: str
        :param type: The type of this resource. The value is always `page`.
        :type type: str
        :param title_fragment: The title text of the page. Includes rich text formatting.
        :type title_fragment: str
        :param parent_id: The unique identifier of the parent page. Null for root-level pages., defaults to None
        :type parent_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.title_fragment = title_fragment
        self.parent_id = parent_id
