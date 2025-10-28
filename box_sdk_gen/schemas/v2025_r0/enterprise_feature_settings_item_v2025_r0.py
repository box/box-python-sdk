from typing import Optional

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_v2025_r0 import (
    EnterpriseConfigurationItemV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_feature_setting_v2025_r0 import (
    EnterpriseFeatureSettingV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class EnterpriseFeatureSettingsItemV2025R0(EnterpriseConfigurationItemV2025R0):
    def __init__(
        self,
        *,
        value: Optional[EnterpriseFeatureSettingV2025R0] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value
