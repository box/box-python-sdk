from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.file import File

from box_sdk_gen.schemas.folder import Folder

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.schemas.group_mini import GroupMini

from box_sdk_gen.schemas.collaboration_item import CollaborationItem

from box_sdk_gen.schemas.app_item import AppItem

from box_sdk_gen.schemas.collaboration_access_grantee import CollaborationAccessGrantee

from box_sdk_gen.schemas.user_collaborations import UserCollaborations

from box_sdk_gen.schemas.terms_of_service_base import TermsOfServiceBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class CollaborationTypeField(str, Enum):
    COLLABORATION = 'collaboration'


class CollaborationRoleField(str, Enum):
    EDITOR = 'editor'
    VIEWER = 'viewer'
    PREVIEWER = 'previewer'
    UPLOADER = 'uploader'
    PREVIEWER_UPLOADER = 'previewer uploader'
    VIEWER_UPLOADER = 'viewer uploader'
    CO_OWNER = 'co-owner'
    OWNER = 'owner'


class CollaborationStatusField(str, Enum):
    ACCEPTED = 'accepted'
    PENDING = 'pending'
    REJECTED = 'rejected'


class CollaborationAcceptanceRequirementsStatusTermsOfServiceRequirementField(
    BaseObject
):
    def __init__(
        self,
        *,
        is_accepted: Optional[bool] = None,
        terms_of_service: Optional[TermsOfServiceBase] = None,
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


class CollaborationAcceptanceRequirementsStatusStrongPasswordRequirementField(
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


class CollaborationAcceptanceRequirementsStatusTwoFactorAuthenticationRequirementField(
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


class CollaborationAcceptanceRequirementsStatusField(BaseObject):
    def __init__(
        self,
        *,
        terms_of_service_requirement: Optional[
            CollaborationAcceptanceRequirementsStatusTermsOfServiceRequirementField
        ] = None,
        strong_password_requirement: Optional[
            CollaborationAcceptanceRequirementsStatusStrongPasswordRequirementField
        ] = None,
        two_factor_authentication_requirement: Optional[
            CollaborationAcceptanceRequirementsStatusTwoFactorAuthenticationRequirementField
        ] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.terms_of_service_requirement = terms_of_service_requirement
        self.strong_password_requirement = strong_password_requirement
        self.two_factor_authentication_requirement = (
            two_factor_authentication_requirement
        )


class Collaboration(BaseObject):
    _discriminator = 'type', {'collaboration'}

    def __init__(
        self,
        id: str,
        *,
        type: CollaborationTypeField = CollaborationTypeField.COLLABORATION,
        item: Optional[CollaborationItem] = None,
        app_item: Optional[AppItem] = None,
        accessible_by: Optional[CollaborationAccessGrantee] = None,
        invite_email: Optional[str] = None,
        role: Optional[CollaborationRoleField] = None,
        expires_at: Optional[DateTime] = None,
        is_access_only: Optional[bool] = None,
        status: Optional[CollaborationStatusField] = None,
        acknowledged_at: Optional[DateTime] = None,
        created_by: Optional[UserCollaborations] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        acceptance_requirements_status: Optional[
            CollaborationAcceptanceRequirementsStatusField
        ] = None,
        **kwargs
    ):
        """
                :param id: The unique identifier for this collaboration.
                :type id: str
                :param type: The value will always be `collaboration`., defaults to CollaborationTypeField.COLLABORATION
                :type type: CollaborationTypeField, optional
                :param invite_email: The email address used to invite an unregistered collaborator, if
        they are not a registered user., defaults to None
                :type invite_email: Optional[str], optional
                :param role: The level of access granted., defaults to None
                :type role: Optional[CollaborationRoleField], optional
                :param expires_at: When the collaboration will expire, or `null` if no expiration
        date is set., defaults to None
                :type expires_at: Optional[DateTime], optional
                :param is_access_only: If set to `true`, collaborators have access to
        shared items, but such items won't be visible in the
        All Files list. Additionally, collaborators won't
        see the path to the root folder for the
        shared item., defaults to None
                :type is_access_only: Optional[bool], optional
                :param status: The status of the collaboration invitation. If the status
        is `pending`, `login` and `name` return an empty string., defaults to None
                :type status: Optional[CollaborationStatusField], optional
                :param acknowledged_at: When the `status` of the collaboration object changed to
        `accepted` or `rejected`., defaults to None
                :type acknowledged_at: Optional[DateTime], optional
                :param created_at: When the collaboration object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: When the collaboration object was last modified., defaults to None
                :type modified_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.item = item
        self.app_item = app_item
        self.accessible_by = accessible_by
        self.invite_email = invite_email
        self.role = role
        self.expires_at = expires_at
        self.is_access_only = is_access_only
        self.status = status
        self.acknowledged_at = acknowledged_at
        self.created_by = created_by
        self.created_at = created_at
        self.modified_at = modified_at
        self.acceptance_requirements_status = acceptance_requirements_status
