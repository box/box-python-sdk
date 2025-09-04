from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class HubUpdateRequestV2025R0(BaseObject):
    def __init__(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_ai_enabled: Optional[bool] = None,
        is_collaboration_restricted_to_enterprise: Optional[bool] = None,
        can_non_owners_invite: Optional[bool] = None,
        can_shared_link_be_created: Optional[bool] = None,
        **kwargs
    ):
        """
        :param title: Title of the Box Hub. It cannot be empty and should be less than 50 characters., defaults to None
        :type title: Optional[str], optional
        :param description: Description of the Box Hub., defaults to None
        :type description: Optional[str], optional
        :param is_ai_enabled: Indicates if AI features are enabled for the Box Hub., defaults to None
        :type is_ai_enabled: Optional[bool], optional
        :param is_collaboration_restricted_to_enterprise: Indicates if collaboration is restricted to the enterprise., defaults to None
        :type is_collaboration_restricted_to_enterprise: Optional[bool], optional
        :param can_non_owners_invite: Indicates if non-owners can invite others to the Box Hub., defaults to None
        :type can_non_owners_invite: Optional[bool], optional
        :param can_shared_link_be_created: Indicates if a shared link can be created for the Box Hub., defaults to None
        :type can_shared_link_be_created: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.is_ai_enabled = is_ai_enabled
        self.is_collaboration_restricted_to_enterprise = (
            is_collaboration_restricted_to_enterprise
        )
        self.can_non_owners_invite = can_non_owners_invite
        self.can_shared_link_be_created = can_shared_link_be_created
