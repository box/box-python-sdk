from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.v2025_r0.hub_collaboration_user_v2025_r0 import (
    HubCollaborationUserV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.group_mini_v2025_r0 import GroupMiniV2025R0

from box_sdk_gen.schemas.v2025_r0.hub_base_v2025_r0 import HubBaseV2025R0

from box_sdk_gen.schemas.v2025_r0.hub_access_grantee_v2025_r0 import (
    HubAccessGranteeV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.terms_of_service_base_v2025_r0 import (
    TermsOfServiceBaseV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class HubCollaborationV2025R0TypeField(str, Enum):
    HUB_COLLABORATION = 'hub_collaboration'


class HubCollaborationV2025R0StatusField(str, Enum):
    ACCEPTED = 'accepted'
    PENDING = 'pending'
    REJECTED = 'rejected'


class HubCollaborationV2025R0AcceptanceRequirementsStatusTermsOfServiceRequirementField(
    BaseObject
):
    def __init__(
        self,
        *,
        is_accepted: Optional[bool] = None,
        terms_of_service: Optional[TermsOfServiceBaseV2025R0] = None,
        **kwargs
    ):
        """
                :param is_accepted: Whether or not the terms of service have been accepted.  The
        field is `null` when there is no terms of service required., defaults to None
                :type is_accepted: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.is_accepted = is_accepted
        self.terms_of_service = terms_of_service


class HubCollaborationV2025R0AcceptanceRequirementsStatusStrongPasswordRequirementField(
    BaseObject
):
    def __init__(
        self,
        *,
        enterprise_has_strong_password_required_for_external_users: Optional[
            bool
        ] = None,
        user_has_strong_password: Optional[bool] = None,
        **kwargs
    ):
        """
                :param enterprise_has_strong_password_required_for_external_users: Whether or not the enterprise that owns the content requires
        a strong password to collaborate on the content, or enforces
        an exposed password detection for the external collaborators., defaults to None
                :type enterprise_has_strong_password_required_for_external_users: Optional[bool], optional
                :param user_has_strong_password: Whether or not the user has a strong and not exposed password set
        for their account. The field is `null` when a strong password is
        not required., defaults to None
                :type user_has_strong_password: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.enterprise_has_strong_password_required_for_external_users = (
            enterprise_has_strong_password_required_for_external_users
        )
        self.user_has_strong_password = user_has_strong_password


class HubCollaborationV2025R0AcceptanceRequirementsStatusTwoFactorAuthenticationRequirementField(
    BaseObject
):
    def __init__(
        self,
        *,
        enterprise_has_two_factor_auth_enabled: Optional[bool] = None,
        user_has_two_factor_authentication_enabled: Optional[bool] = None,
        **kwargs
    ):
        """
                :param enterprise_has_two_factor_auth_enabled: Whether or not the enterprise that owns the content requires
        two-factor authentication to be enabled in order to
        collaborate on the content., defaults to None
                :type enterprise_has_two_factor_auth_enabled: Optional[bool], optional
                :param user_has_two_factor_authentication_enabled: Whether or not the user has two-factor authentication
        enabled. The field is `null` when two-factor
        authentication is not required., defaults to None
                :type user_has_two_factor_authentication_enabled: Optional[bool], optional
        """
        super().__init__(**kwargs)
        self.enterprise_has_two_factor_auth_enabled = (
            enterprise_has_two_factor_auth_enabled
        )
        self.user_has_two_factor_authentication_enabled = (
            user_has_two_factor_authentication_enabled
        )


class HubCollaborationV2025R0AcceptanceRequirementsStatusField(BaseObject):
    def __init__(
        self,
        *,
        terms_of_service_requirement: Optional[
            HubCollaborationV2025R0AcceptanceRequirementsStatusTermsOfServiceRequirementField
        ] = None,
        strong_password_requirement: Optional[
            HubCollaborationV2025R0AcceptanceRequirementsStatusStrongPasswordRequirementField
        ] = None,
        two_factor_authentication_requirement: Optional[
            HubCollaborationV2025R0AcceptanceRequirementsStatusTwoFactorAuthenticationRequirementField
        ] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.terms_of_service_requirement = terms_of_service_requirement
        self.strong_password_requirement = strong_password_requirement
        self.two_factor_authentication_requirement = (
            two_factor_authentication_requirement
        )


class HubCollaborationV2025R0(BaseObject):
    _discriminator = 'type', {'hub_collaboration'}

    def __init__(
        self,
        id: str,
        *,
        type: HubCollaborationV2025R0TypeField = HubCollaborationV2025R0TypeField.HUB_COLLABORATION,
        hub: Optional[HubBaseV2025R0] = None,
        accessible_by: Optional[HubAccessGranteeV2025R0] = None,
        role: Optional[str] = None,
        status: Optional[HubCollaborationV2025R0StatusField] = None,
        acceptance_requirements_status: Optional[
            HubCollaborationV2025R0AcceptanceRequirementsStatusField
        ] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this collaboration.
                :type id: str
                :param type: The value will always be `hub_collaboration`., defaults to HubCollaborationV2025R0TypeField.HUB_COLLABORATION
                :type type: HubCollaborationV2025R0TypeField, optional
                :param role: The level of access granted to a Box Hub.
        Possible values are `editor`, `viewer`, and `co-owner`., defaults to None
                :type role: Optional[str], optional
                :param status: The status of the collaboration invitation. If the status
        is `pending`, `login` and `name` return an empty string., defaults to None
                :type status: Optional[HubCollaborationV2025R0StatusField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.hub = hub
        self.accessible_by = accessible_by
        self.role = role
        self.status = status
        self.acceptance_requirements_status = acceptance_requirements_status
