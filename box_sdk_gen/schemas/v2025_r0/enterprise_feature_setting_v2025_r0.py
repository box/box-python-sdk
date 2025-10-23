from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.v2025_r0.user_or_group_reference_v2025_r0 import (
    UserOrGroupReferenceV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class EnterpriseFeatureSettingV2025R0FeatureField(BaseObject):
    def __init__(self, *, id: Optional[str] = None, **kwargs):
        """
        :param id: The identifier of the feature., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id


class EnterpriseFeatureSettingV2025R0(BaseObject):
    def __init__(
        self,
        *,
        id: Optional[str] = None,
        feature: Optional[EnterpriseFeatureSettingV2025R0FeatureField] = None,
        state: Optional[str] = None,
        can_configure: Optional[bool] = None,
        is_configured: Optional[bool] = None,
        allowlist: Optional[List[UserOrGroupReferenceV2025R0]] = None,
        denylist: Optional[List[UserOrGroupReferenceV2025R0]] = None,
        **kwargs
    ):
        """
        :param id: The identifier of the enterprise feature setting., defaults to None
        :type id: Optional[str], optional
        :param feature: The feature., defaults to None
        :type feature: Optional[EnterpriseFeatureSettingV2025R0FeatureField], optional
        :param state: The state of the feature., defaults to None
        :type state: Optional[str], optional
        :param can_configure: Whether the feature can be configured., defaults to None
        :type can_configure: Optional[bool], optional
        :param is_configured: Whether the feature is configured., defaults to None
        :type is_configured: Optional[bool], optional
        :param allowlist: Enterprise feature setting is enabled for only this set of users and groups., defaults to None
        :type allowlist: Optional[List[UserOrGroupReferenceV2025R0]], optional
        :param denylist: Enterprise feature setting is enabled for everyone except this set of users and groups., defaults to None
        :type denylist: Optional[List[UserOrGroupReferenceV2025R0]], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.feature = feature
        self.state = state
        self.can_configure = can_configure
        self.is_configured = is_configured
        self.allowlist = allowlist
        self.denylist = denylist
