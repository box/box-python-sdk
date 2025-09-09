from enum import Enum

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShieldListContentEmailV2025R0TypeField(str, Enum):
    EMAIL = 'email'


class ShieldListContentEmailV2025R0(BaseObject):
    _discriminator = 'type', {'email'}

    def __init__(
        self,
        email_addresses: List[str],
        *,
        type: ShieldListContentEmailV2025R0TypeField = ShieldListContentEmailV2025R0TypeField.EMAIL,
        **kwargs
    ):
        """
        :param email_addresses: List of emails.
        :type email_addresses: List[str]
        :param type: The type of content in the shield list., defaults to ShieldListContentEmailV2025R0TypeField.EMAIL
        :type type: ShieldListContentEmailV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.email_addresses = email_addresses
        self.type = type
