from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class CollaborationPermissionsV2025R0(BaseObject):
    def __init__(
        self,
        *,
        is_co_owner_role_enabled: Optional[bool] = None,
        is_editor_role_enabled: Optional[bool] = None,
        is_previewer_role_enabled: Optional[bool] = None,
        is_previewer_uploader_role_enabled: Optional[bool] = None,
        is_uploader_role_enabled: Optional[bool] = None,
        is_viewer_role_enabled: Optional[bool] = None,
        is_viewer_uploader_role_enabled: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_co_owner_role_enabled: The co-owner role is enabled for collaboration., defaults to None
        :type is_co_owner_role_enabled: Optional[bool], optional
        :param is_editor_role_enabled: The editor role is enabled for collaboration., defaults to None
        :type is_editor_role_enabled: Optional[bool], optional
        :param is_previewer_role_enabled: The previewer role is enabled for collaboration., defaults to None
        :type is_previewer_role_enabled: Optional[bool], optional
        :param is_previewer_uploader_role_enabled: The previewer uploader role is enabled for collaboration., defaults to None
        :type is_previewer_uploader_role_enabled: Optional[bool], optional
        :param is_uploader_role_enabled: The uploader role is enabled for collaboration., defaults to None
        :type is_uploader_role_enabled: Optional[bool], optional
        :param is_viewer_role_enabled: The viewer role is enabled for collaboration., defaults to None
        :type is_viewer_role_enabled: Optional[bool], optional
        :param is_viewer_uploader_role_enabled: The viewer uploader role is enabled for collaboration., defaults to None
        :type is_viewer_uploader_role_enabled: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.is_co_owner_role_enabled = is_co_owner_role_enabled
        self.is_editor_role_enabled = is_editor_role_enabled
        self.is_previewer_role_enabled = is_previewer_role_enabled
        self.is_previewer_uploader_role_enabled = is_previewer_uploader_role_enabled
        self.is_uploader_role_enabled = is_uploader_role_enabled
        self.is_viewer_role_enabled = is_viewer_role_enabled
        self.is_viewer_uploader_role_enabled = is_viewer_uploader_role_enabled
