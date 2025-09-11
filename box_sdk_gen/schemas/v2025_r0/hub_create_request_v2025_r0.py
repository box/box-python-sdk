from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class HubCreateRequestV2025R0(BaseObject):
    def __init__(self, title: str, *, description: Optional[str] = None, **kwargs):
        """
        :param title: Title of the Box Hub. It cannot be empty and should be less than 50 characters.
        :type title: str
        :param description: Description of the Box Hub., defaults to None
        :type description: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.title = title
        self.description = description
