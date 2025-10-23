from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_boolean_v2025_r0 import (
    EnterpriseConfigurationItemBooleanV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_v2025_r0 import (
    EnterpriseConfigurationItemV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_string_v2025_r0 import (
    EnterpriseConfigurationItemStringV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_integer_v2025_r0 import (
    EnterpriseConfigurationItemIntegerV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.external_collab_security_settings_v2025_r0 import (
    ExternalCollabSecuritySettingsV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.keysafe_settings_v2025_r0 import (
    KeysafeSettingsV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.custom_session_duration_group_item_v2025_r0 import (
    CustomSessionDurationGroupItemV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class EnterpriseConfigurationSecurityV2025R0LastPasswordResetAtField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[DateTime] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param value: When an enterprise password reset was last applied., defaults to None
        :type value: Optional[DateTime], optional
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationSecurityV2025R0ExternalCollabMultiFactorAuthSettingsField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[Optional[ExternalCollabSecuritySettingsV2025R0]] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationSecurityV2025R0KeysafeField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[Optional[KeysafeSettingsV2025R0]] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationSecurityV2025R0CustomSessionDurationGroupsField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[List[CustomSessionDurationGroupItemV2025R0]] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationSecurityV2025R0EnforcedMfaFrequencyFieldValueField(
    BaseObject
):
    def __init__(
        self, *, days: Optional[int] = None, hours: Optional[int] = None, **kwargs
    ):
        """
        :param days: Number of days before the user is required to authenticate again., defaults to None
        :type days: Optional[int], optional
        :param hours: Number of hours before the user is required to authenticate again., defaults to None
        :type hours: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.days = days
        self.hours = hours


class EnterpriseConfigurationSecurityV2025R0EnforcedMfaFrequencyField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[
            EnterpriseConfigurationSecurityV2025R0EnforcedMfaFrequencyFieldValueField
        ] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationSecurityV2025R0(BaseObject):
    def __init__(
        self,
        *,
        is_managed_user_signup_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_managed_user_signup_notification_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_managed_user_signup_corporate_email_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_new_user_notification_daily_digest_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_managed_user_email_change_disabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_multi_factor_auth_required: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_weak_password_prevention_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_password_leak_detection_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        last_password_reset_at: Optional[
            EnterpriseConfigurationSecurityV2025R0LastPasswordResetAtField
        ] = None,
        is_password_request_notification_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_password_change_notification_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_strong_password_for_ext_collab_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_managed_user_migration_disabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        join_link: Optional[EnterpriseConfigurationItemStringV2025R0] = None,
        join_url: Optional[EnterpriseConfigurationItemStringV2025R0] = None,
        failed_login_attempts_to_trigger_admin_notification: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        password_min_length: Optional[EnterpriseConfigurationItemIntegerV2025R0] = None,
        password_min_uppercase_characters: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        password_min_numeric_characters: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        password_min_special_characters: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        password_reset_frequency: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        previous_password_reuse_limit: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        session_duration: Optional[EnterpriseConfigurationItemStringV2025R0] = None,
        external_collab_multi_factor_auth_settings: Optional[
            EnterpriseConfigurationSecurityV2025R0ExternalCollabMultiFactorAuthSettingsField
        ] = None,
        keysafe: Optional[EnterpriseConfigurationSecurityV2025R0KeysafeField] = None,
        is_custom_session_duration_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        custom_session_duration_value: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        custom_session_duration_groups: Optional[
            EnterpriseConfigurationSecurityV2025R0CustomSessionDurationGroupsField
        ] = None,
        multi_factor_auth_type: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        enforced_mfa_frequency: Optional[
            EnterpriseConfigurationSecurityV2025R0EnforcedMfaFrequencyField
        ] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.is_managed_user_signup_enabled = is_managed_user_signup_enabled
        self.is_managed_user_signup_notification_enabled = (
            is_managed_user_signup_notification_enabled
        )
        self.is_managed_user_signup_corporate_email_enabled = (
            is_managed_user_signup_corporate_email_enabled
        )
        self.is_new_user_notification_daily_digest_enabled = (
            is_new_user_notification_daily_digest_enabled
        )
        self.is_managed_user_email_change_disabled = (
            is_managed_user_email_change_disabled
        )
        self.is_multi_factor_auth_required = is_multi_factor_auth_required
        self.is_weak_password_prevention_enabled = is_weak_password_prevention_enabled
        self.is_password_leak_detection_enabled = is_password_leak_detection_enabled
        self.last_password_reset_at = last_password_reset_at
        self.is_password_request_notification_enabled = (
            is_password_request_notification_enabled
        )
        self.is_password_change_notification_enabled = (
            is_password_change_notification_enabled
        )
        self.is_strong_password_for_ext_collab_enabled = (
            is_strong_password_for_ext_collab_enabled
        )
        self.is_managed_user_migration_disabled = is_managed_user_migration_disabled
        self.join_link = join_link
        self.join_url = join_url
        self.failed_login_attempts_to_trigger_admin_notification = (
            failed_login_attempts_to_trigger_admin_notification
        )
        self.password_min_length = password_min_length
        self.password_min_uppercase_characters = password_min_uppercase_characters
        self.password_min_numeric_characters = password_min_numeric_characters
        self.password_min_special_characters = password_min_special_characters
        self.password_reset_frequency = password_reset_frequency
        self.previous_password_reuse_limit = previous_password_reuse_limit
        self.session_duration = session_duration
        self.external_collab_multi_factor_auth_settings = (
            external_collab_multi_factor_auth_settings
        )
        self.keysafe = keysafe
        self.is_custom_session_duration_enabled = is_custom_session_duration_enabled
        self.custom_session_duration_value = custom_session_duration_value
        self.custom_session_duration_groups = custom_session_duration_groups
        self.multi_factor_auth_type = multi_factor_auth_type
        self.enforced_mfa_frequency = enforced_mfa_frequency
