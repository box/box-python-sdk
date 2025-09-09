from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.terms_of_service_base import TermsOfServiceBase

from box_sdk_gen.schemas.user_mini import UserMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TermsOfServiceUserStatusTypeField(str, Enum):
    TERMS_OF_SERVICE_USER_STATUS = 'terms_of_service_user_status'


class TermsOfServiceUserStatus(BaseObject):
    _discriminator = 'type', {'terms_of_service_user_status'}

    def __init__(
        self,
        id: str,
        *,
        type: TermsOfServiceUserStatusTypeField = TermsOfServiceUserStatusTypeField.TERMS_OF_SERVICE_USER_STATUS,
        tos: Optional[TermsOfServiceBase] = None,
        user: Optional[UserMini] = None,
        is_accepted: Optional[bool] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this terms of service user status.
        :type id: str
        :param type: The value will always be `terms_of_service_user_status`., defaults to TermsOfServiceUserStatusTypeField.TERMS_OF_SERVICE_USER_STATUS
        :type type: TermsOfServiceUserStatusTypeField, optional
        :param is_accepted: If the user has accepted the terms of services., defaults to None
        :type is_accepted: Optional[bool], optional
        :param created_at: When the legal item was created., defaults to None
        :type created_at: Optional[DateTime], optional
        :param modified_at: When the legal item was modified., defaults to None
        :type modified_at: Optional[DateTime], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.tos = tos
        self.user = user
        self.is_accepted = is_accepted
        self.created_at = created_at
        self.modified_at = modified_at
