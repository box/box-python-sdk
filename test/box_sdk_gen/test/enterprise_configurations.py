from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_v2025_r0 import (
    EnterpriseConfigurationV2025R0,
)

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_user_settings_v2025_r0 import (
    EnterpriseConfigurationUserSettingsV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_content_and_sharing_v2025_r0 import (
    EnterpriseConfigurationContentAndSharingV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_security_v2025_r0 import (
    EnterpriseConfigurationSecurityV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_shield_v2025_r0 import (
    EnterpriseConfigurationShieldV2025R0,
)

admin_client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))


def testGetEnterpriseConfigurationById():
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    enterprise_configuration: EnterpriseConfigurationV2025R0 = (
        admin_client.enterprise_configurations.get_enterprise_configuration_by_id_v2025_r0(
            enterprise_id,
            ['user_settings', 'content_and_sharing', 'security', 'shield'],
        )
    )
    assert to_string(enterprise_configuration.type) == 'enterprise_configuration'
    user_settings: EnterpriseConfigurationUserSettingsV2025R0 = (
        enterprise_configuration.user_settings
    )
    assert user_settings.is_enterprise_sso_required.value == False
    assert user_settings.new_user_default_language.value == 'English (US)'
    assert user_settings.new_user_default_storage_limit.value == -1
    content_and_sharing: EnterpriseConfigurationContentAndSharingV2025R0 = (
        enterprise_configuration.content_and_sharing
    )
    assert (
        content_and_sharing.collaboration_permissions.value.is_editor_role_enabled
        == True
    )
    security: EnterpriseConfigurationSecurityV2025R0 = enterprise_configuration.security
    assert security.is_managed_user_signup_enabled.value == False
    shield: EnterpriseConfigurationShieldV2025R0 = enterprise_configuration.shield
    assert len(shield.shield_rules) == 0
