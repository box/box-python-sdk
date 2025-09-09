from enum import Enum

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShieldListContentDomainV2025R0TypeField(str, Enum):
    DOMAIN = 'domain'


class ShieldListContentDomainV2025R0(BaseObject):
    _discriminator = 'type', {'domain'}

    def __init__(
        self,
        domains: List[str],
        *,
        type: ShieldListContentDomainV2025R0TypeField = ShieldListContentDomainV2025R0TypeField.DOMAIN,
        **kwargs
    ):
        """
        :param domains: List of domain.
        :type domains: List[str]
        :param type: The type of content in the shield list., defaults to ShieldListContentDomainV2025R0TypeField.DOMAIN
        :type type: ShieldListContentDomainV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.domains = domains
        self.type = type
