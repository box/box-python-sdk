from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.enterprise_feature_settings_item_v2025_r0 import (
    EnterpriseFeatureSettingsItemV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_string_v2025_r0 import (
    EnterpriseConfigurationItemStringV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_boolean_v2025_r0 import (
    EnterpriseConfigurationItemBooleanV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_integer_v2025_r0 import (
    EnterpriseConfigurationItemIntegerV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_v2025_r0 import (
    EnterpriseConfigurationItemV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.user_tracking_code_v2025_r0 import (
    UserTrackingCodeV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class EnterpriseConfigurationUserSettingsV2025R0UserTrackingCodesField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[List[UserTrackingCodeV2025R0]] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationUserSettingsV2025R0(BaseObject):
    def __init__(
        self,
        *,
        enterprise_feature_settings: Optional[
            List[EnterpriseFeatureSettingsItemV2025R0]
        ] = None,
        user_invites_expiration_time_frame: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        is_username_change_restricted: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_box_sync_restricted_for_new_users: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_view_all_users_enabled_for_new_users: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_device_limit_exemption_enabled_for_new_users: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_external_collaboration_restricted_for_new_users: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_unlimited_storage_enabled_for_new_users: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        new_user_default_storage_limit: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        new_user_default_timezone: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        new_user_default_language: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        is_enterprise_sso_required: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_enterprise_sso_in_testing: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_sso_auto_add_groups_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_sso_auto_add_user_to_groups_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_sso_auto_remove_user_from_groups_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        user_tracking_codes: Optional[
            EnterpriseConfigurationUserSettingsV2025R0UserTrackingCodesField
        ] = None,
        number_of_user_tracking_codes_remaining: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        is_instant_login_restricted: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.enterprise_feature_settings = enterprise_feature_settings
        self.user_invites_expiration_time_frame = user_invites_expiration_time_frame
        self.is_username_change_restricted = is_username_change_restricted
        self.is_box_sync_restricted_for_new_users = is_box_sync_restricted_for_new_users
        self.is_view_all_users_enabled_for_new_users = (
            is_view_all_users_enabled_for_new_users
        )
        self.is_device_limit_exemption_enabled_for_new_users = (
            is_device_limit_exemption_enabled_for_new_users
        )
        self.is_external_collaboration_restricted_for_new_users = (
            is_external_collaboration_restricted_for_new_users
        )
        self.is_unlimited_storage_enabled_for_new_users = (
            is_unlimited_storage_enabled_for_new_users
        )
        self.new_user_default_storage_limit = new_user_default_storage_limit
        self.new_user_default_timezone = new_user_default_timezone
        self.new_user_default_language = new_user_default_language
        self.is_enterprise_sso_required = is_enterprise_sso_required
        self.is_enterprise_sso_in_testing = is_enterprise_sso_in_testing
        self.is_sso_auto_add_groups_enabled = is_sso_auto_add_groups_enabled
        self.is_sso_auto_add_user_to_groups_enabled = (
            is_sso_auto_add_user_to_groups_enabled
        )
        self.is_sso_auto_remove_user_from_groups_enabled = (
            is_sso_auto_remove_user_from_groups_enabled
        )
        self.user_tracking_codes = user_tracking_codes
        self.number_of_user_tracking_codes_remaining = (
            number_of_user_tracking_codes_remaining
        )
        self.is_instant_login_restricted = is_instant_login_restricted
