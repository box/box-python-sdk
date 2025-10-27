from typing import Optional

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.enterprise_feature_settings_item_v2025_r0 import (
    EnterpriseFeatureSettingsItemV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_string_v2025_r0 import (
    EnterpriseConfigurationItemStringV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_v2025_r0 import (
    EnterpriseConfigurationItemV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shared_link_permissions_v2025_r0 import (
    SharedLinkPermissionsV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_boolean_v2025_r0 import (
    EnterpriseConfigurationItemBooleanV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.collaboration_permissions_v2025_r0 import (
    CollaborationPermissionsV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.list_user_v2025_r0 import ListUserV2025R0

from box_sdk_gen.schemas.v2025_r0.enterprise_configuration_item_integer_v2025_r0 import (
    EnterpriseConfigurationItemIntegerV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class EnterpriseConfigurationContentAndSharingV2025R0SharedLinkDefaultPermissionsSelectedField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[SharedLinkPermissionsV2025R0] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationContentAndSharingV2025R0CollaborationPermissionsField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[CollaborationPermissionsV2025R0] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationContentAndSharingV2025R0CollaborationRestrictionsField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[List[str]] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationContentAndSharingV2025R0ExternalCollaborationStatusField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self, *, value: Optional[str] = None, is_used: Optional[bool] = None, **kwargs
    ):
        """
        :param value: The external collaboration status., defaults to None
        :type value: Optional[str], optional
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationContentAndSharingV2025R0ExternalCollaborationAllowlistUsersField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[List[ListUserV2025R0]] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationContentAndSharingV2025R0PermanentDeletionAllowlistUsersField(
    EnterpriseConfigurationItemV2025R0
):
    def __init__(
        self,
        *,
        value: Optional[List[ListUserV2025R0]] = None,
        is_used: Optional[bool] = None,
        **kwargs
    ):
        """
        :param is_used: Indicates whether a configuration is used for a given enterprise., defaults to None
        :type is_used: Optional[bool], optional
        """
        super().__init__(is_used=is_used, **kwargs)
        self.value = value


class EnterpriseConfigurationContentAndSharingV2025R0(BaseObject):
    def __init__(
        self,
        *,
        enterprise_feature_settings: Optional[
            List[EnterpriseFeatureSettingsItemV2025R0]
        ] = None,
        sharing_item_type: Optional[EnterpriseConfigurationItemStringV2025R0] = None,
        shared_link_company_definition: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        shared_link_access: Optional[EnterpriseConfigurationItemStringV2025R0] = None,
        shared_link_default_access: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        shared_link_default_permissions_selected: Optional[
            EnterpriseConfigurationContentAndSharingV2025R0SharedLinkDefaultPermissionsSelectedField
        ] = None,
        is_open_custom_urls_disabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_custom_domain_hidden_in_shared_link: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        collaboration_permissions: Optional[
            EnterpriseConfigurationContentAndSharingV2025R0CollaborationPermissionsField
        ] = None,
        default_collaboration_role: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        is_invite_privilege_restricted: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        collaboration_restrictions: Optional[
            EnterpriseConfigurationContentAndSharingV2025R0CollaborationRestrictionsField
        ] = None,
        is_collaborator_invite_links_disabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_invite_group_collaborator_disabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_ownership_transfer_restricted: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        external_collaboration_status: Optional[
            EnterpriseConfigurationContentAndSharingV2025R0ExternalCollaborationStatusField
        ] = None,
        external_collaboration_allowlist_users: Optional[
            EnterpriseConfigurationContentAndSharingV2025R0ExternalCollaborationAllowlistUsersField
        ] = None,
        is_watermarking_enterprise_feature_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_root_content_creation_restricted: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_tag_creation_restricted: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        tag_creation_restriction: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        is_email_uploads_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_custom_settings_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_forms_login_required: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_forms_branding_default_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_cc_free_trial_active: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_file_request_editors_allowed: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_file_request_branding_default_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_file_request_login_required: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_shared_links_expiration_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        shared_links_expiration_days: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        is_public_shared_links_expiration_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        public_shared_links_expiration_days: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        shared_expiration_target: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        is_shared_links_expiration_notification_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        shared_links_expiration_notification_days: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        is_shared_links_expiration_notification_prevented: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_auto_delete_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        auto_delete_days: Optional[EnterpriseConfigurationItemIntegerV2025R0] = None,
        is_auto_delete_expiration_modification_prevented: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        auto_delete_target: Optional[EnterpriseConfigurationItemStringV2025R0] = None,
        is_collaboration_expiration_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        collaboration_expiration_days: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        is_collaboration_expiration_modification_prevented: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        is_collaboration_expiration_notification_enabled: Optional[
            EnterpriseConfigurationItemBooleanV2025R0
        ] = None,
        collaboration_expiration_target: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        trash_auto_clear_time: Optional[
            EnterpriseConfigurationItemIntegerV2025R0
        ] = None,
        permanent_deletion_access: Optional[
            EnterpriseConfigurationItemStringV2025R0
        ] = None,
        permanent_deletion_allowlist_users: Optional[
            EnterpriseConfigurationContentAndSharingV2025R0PermanentDeletionAllowlistUsersField
        ] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.enterprise_feature_settings = enterprise_feature_settings
        self.sharing_item_type = sharing_item_type
        self.shared_link_company_definition = shared_link_company_definition
        self.shared_link_access = shared_link_access
        self.shared_link_default_access = shared_link_default_access
        self.shared_link_default_permissions_selected = (
            shared_link_default_permissions_selected
        )
        self.is_open_custom_urls_disabled = is_open_custom_urls_disabled
        self.is_custom_domain_hidden_in_shared_link = (
            is_custom_domain_hidden_in_shared_link
        )
        self.collaboration_permissions = collaboration_permissions
        self.default_collaboration_role = default_collaboration_role
        self.is_invite_privilege_restricted = is_invite_privilege_restricted
        self.collaboration_restrictions = collaboration_restrictions
        self.is_collaborator_invite_links_disabled = (
            is_collaborator_invite_links_disabled
        )
        self.is_invite_group_collaborator_disabled = (
            is_invite_group_collaborator_disabled
        )
        self.is_ownership_transfer_restricted = is_ownership_transfer_restricted
        self.external_collaboration_status = external_collaboration_status
        self.external_collaboration_allowlist_users = (
            external_collaboration_allowlist_users
        )
        self.is_watermarking_enterprise_feature_enabled = (
            is_watermarking_enterprise_feature_enabled
        )
        self.is_root_content_creation_restricted = is_root_content_creation_restricted
        self.is_tag_creation_restricted = is_tag_creation_restricted
        self.tag_creation_restriction = tag_creation_restriction
        self.is_email_uploads_enabled = is_email_uploads_enabled
        self.is_custom_settings_enabled = is_custom_settings_enabled
        self.is_forms_login_required = is_forms_login_required
        self.is_forms_branding_default_enabled = is_forms_branding_default_enabled
        self.is_cc_free_trial_active = is_cc_free_trial_active
        self.is_file_request_editors_allowed = is_file_request_editors_allowed
        self.is_file_request_branding_default_enabled = (
            is_file_request_branding_default_enabled
        )
        self.is_file_request_login_required = is_file_request_login_required
        self.is_shared_links_expiration_enabled = is_shared_links_expiration_enabled
        self.shared_links_expiration_days = shared_links_expiration_days
        self.is_public_shared_links_expiration_enabled = (
            is_public_shared_links_expiration_enabled
        )
        self.public_shared_links_expiration_days = public_shared_links_expiration_days
        self.shared_expiration_target = shared_expiration_target
        self.is_shared_links_expiration_notification_enabled = (
            is_shared_links_expiration_notification_enabled
        )
        self.shared_links_expiration_notification_days = (
            shared_links_expiration_notification_days
        )
        self.is_shared_links_expiration_notification_prevented = (
            is_shared_links_expiration_notification_prevented
        )
        self.is_auto_delete_enabled = is_auto_delete_enabled
        self.auto_delete_days = auto_delete_days
        self.is_auto_delete_expiration_modification_prevented = (
            is_auto_delete_expiration_modification_prevented
        )
        self.auto_delete_target = auto_delete_target
        self.is_collaboration_expiration_enabled = is_collaboration_expiration_enabled
        self.collaboration_expiration_days = collaboration_expiration_days
        self.is_collaboration_expiration_modification_prevented = (
            is_collaboration_expiration_modification_prevented
        )
        self.is_collaboration_expiration_notification_enabled = (
            is_collaboration_expiration_notification_enabled
        )
        self.collaboration_expiration_target = collaboration_expiration_target
        self.trash_auto_clear_time = trash_auto_clear_time
        self.permanent_deletion_access = permanent_deletion_access
        self.permanent_deletion_allowlist_users = permanent_deletion_allowlist_users
