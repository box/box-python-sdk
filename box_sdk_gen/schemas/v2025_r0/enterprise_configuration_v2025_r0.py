from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_security_v2025_r0 import (
    EnterpriseConfigurationSecurityV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_content_and_sharing_v2025_r0 import (
    EnterpriseConfigurationContentAndSharingV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_user_settings_v2025_r0 import (
    EnterpriseConfigurationUserSettingsV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_shield_v2025_r0 import (
    EnterpriseConfigurationShieldV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class EnterpriseConfigurationV2025R0TypeField(str, Enum):
    ENTERPRISE_CONFIGURATION = 'enterprise_configuration'


class EnterpriseConfigurationV2025R0(BaseObject):
    _discriminator = 'type', {'enterprise_configuration'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[EnterpriseConfigurationV2025R0TypeField] = None,
        security: Optional[Optional[EnterpriseConfigurationSecurityV2025R0]] = None,
        content_and_sharing: Optional[
            Optional[EnterpriseConfigurationContentAndSharingV2025R0]
        ] = None,
        user_settings: Optional[
            Optional[EnterpriseConfigurationUserSettingsV2025R0]
        ] = None,
        shield: Optional[Optional[EnterpriseConfigurationShieldV2025R0]] = None,
        **kwargs
    ):
        """
        :param id: The identifier of the enterprise configuration which is the ID of the enterprise., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `enterprise_configuration`., defaults to None
        :type type: Optional[EnterpriseConfigurationV2025R0TypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.security = security
        self.content_and_sharing = content_and_sharing
        self.user_settings = user_settings
        self.shield = shield
