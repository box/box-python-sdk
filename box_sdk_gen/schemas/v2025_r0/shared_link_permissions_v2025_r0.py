from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SharedLinkPermissionsV2025R0(BaseObject):
    def __init__(
        self,
        *,
        shared_links_option: Optional[str] = None,
        default_shared_link_type: Optional[str] = None,
        notes_shared_link_option: Optional[str] = None,
        default_notes_shared_link_type: Optional[str] = None,
        **kwargs
    ):
        """
        :param shared_links_option: The selected option for shared links permissions., defaults to None
        :type shared_links_option: Optional[str], optional
        :param default_shared_link_type: The default shared link type., defaults to None
        :type default_shared_link_type: Optional[str], optional
        :param notes_shared_link_option: The selected option for notes shared links permissions., defaults to None
        :type notes_shared_link_option: Optional[str], optional
        :param default_notes_shared_link_type: The default notes shared link type., defaults to None
        :type default_notes_shared_link_type: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.shared_links_option = shared_links_option
        self.default_shared_link_type = default_shared_link_type
        self.notes_shared_link_option = notes_shared_link_option
        self.default_notes_shared_link_type = default_notes_shared_link_type
