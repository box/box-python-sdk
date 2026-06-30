from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class HubCopyRequestV2025R0(BaseObject):
    def __init__(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        include_items: Optional[bool] = None,
        **kwargs
    ):
        """
                :param title: Title of the Box Hub. It cannot be empty and should be less than 50 characters., defaults to None
                :type title: Optional[str], optional
                :param description: Description of the Box Hub., defaults to None
                :type description: Optional[str], optional
                :param include_items: If true, the items which the user has Editor or Owner access to in the original Box Hub will be copied to the new Box Hub.
        Defaults to false., defaults to None
                :type include_items: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.include_items = include_items
