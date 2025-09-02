from typing import Optional

from box_sdk_gen.schemas.v2025_r0.hub_base_v2025_r0 import HubBaseV2025R0TypeField

from box_sdk_gen.schemas.v2025_r0.hub_base_v2025_r0 import HubBaseV2025R0

from box_sdk_gen.schemas.v2025_r0.user_mini_v2025_r0 import UserMiniV2025R0

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class HubV2025R0(HubBaseV2025R0):
    def __init__(
        self,
        id: str,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        created_at: Optional[DateTime] = None,
        updated_at: Optional[DateTime] = None,
        created_by: Optional[UserMiniV2025R0] = None,
        updated_by: Optional[UserMiniV2025R0] = None,
        view_count: Optional[int] = None,
        is_ai_enabled: Optional[bool] = None,
        is_collaboration_restricted_to_enterprise: Optional[bool] = None,
        can_non_owners_invite: Optional[bool] = None,
        can_shared_link_be_created: Optional[bool] = None,
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
                :param title: The title given to the Box Hub., defaults to None
                :type title: Optional[str], optional
                :param description: The description of the Box Hub. First 200 characters are returned., defaults to None
                :type description: Optional[str], optional
                :param created_at: The date and time when the folder was created. This value may
        be `null` for some folders such as the root folder or the trash
        folder., defaults to None
                :type created_at: Optional[DateTime], optional
                :param updated_at: The date and time when the Box Hub was last updated., defaults to None
                :type updated_at: Optional[DateTime], optional
                :param view_count: The number of views for the Box Hub., defaults to None
                :type view_count: Optional[int], optional
                :param is_ai_enabled: Indicates if AI features are enabled for the Box Hub., defaults to None
                :type is_ai_enabled: Optional[bool], optional
                :param is_collaboration_restricted_to_enterprise: Indicates if collaboration is restricted to the enterprise., defaults to None
                :type is_collaboration_restricted_to_enterprise: Optional[bool], optional
                :param can_non_owners_invite: Indicates if non-owners can invite others to the Box Hub., defaults to None
                :type can_non_owners_invite: Optional[bool], optional
                :param can_shared_link_be_created: Indicates if a shared link can be created for the Box Hub., defaults to None
                :type can_shared_link_be_created: Optional[bool], optional
                :param type: The value will always be `hubs`., defaults to HubBaseV2025R0TypeField.HUBS
                :type type: HubBaseV2025R0TypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.title = title
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by
        self.view_count = view_count
        self.is_ai_enabled = is_ai_enabled
        self.is_collaboration_restricted_to_enterprise = (
            is_collaboration_restricted_to_enterprise
        )
        self.can_non_owners_invite = can_non_owners_invite
        self.can_shared_link_be_created = can_shared_link_be_created
