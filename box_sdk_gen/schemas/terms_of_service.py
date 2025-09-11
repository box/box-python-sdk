from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.terms_of_service_base import TermsOfServiceBaseTypeField

from box_sdk_gen.schemas.terms_of_service_base import TermsOfServiceBase

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class TermsOfServiceStatusField(str, Enum):
    ENABLED = 'enabled'
    DISABLED = 'disabled'


class TermsOfServiceEnterpriseTypeField(str, Enum):
    ENTERPRISE = 'enterprise'


class TermsOfServiceEnterpriseField(BaseObject):
    _discriminator = 'type', {'enterprise'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[TermsOfServiceEnterpriseTypeField] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: The unique identifier for this enterprise., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `enterprise`., defaults to None
        :type type: Optional[TermsOfServiceEnterpriseTypeField], optional
        :param name: The name of the enterprise., defaults to None
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name


class TermsOfServiceTosTypeField(str, Enum):
    MANAGED = 'managed'
    EXTERNAL = 'external'


class TermsOfService(TermsOfServiceBase):
    def __init__(
        self,
        id: str,
        *,
        status: Optional[TermsOfServiceStatusField] = None,
        enterprise: Optional[TermsOfServiceEnterpriseField] = None,
        tos_type: Optional[TermsOfServiceTosTypeField] = None,
        text: Optional[str] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        type: TermsOfServiceBaseTypeField = TermsOfServiceBaseTypeField.TERMS_OF_SERVICE,
        **kwargs
    ):
        """
                :param id: The unique identifier for this terms of service.
                :type id: str
                :param status: Whether these terms are enabled or not., defaults to None
                :type status: Optional[TermsOfServiceStatusField], optional
                :param tos_type: Whether to apply these terms to managed users or external users., defaults to None
                :type tos_type: Optional[TermsOfServiceTosTypeField], optional
                :param text: The text for your terms and conditions. This text could be
        empty if the `status` is set to `disabled`., defaults to None
                :type text: Optional[str], optional
                :param created_at: When the legal item was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: When the legal item was modified., defaults to None
                :type modified_at: Optional[DateTime], optional
                :param type: The value will always be `terms_of_service`., defaults to TermsOfServiceBaseTypeField.TERMS_OF_SERVICE
                :type type: TermsOfServiceBaseTypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.status = status
        self.enterprise = enterprise
        self.tos_type = tos_type
        self.text = text
        self.created_at = created_at
        self.modified_at = modified_at
