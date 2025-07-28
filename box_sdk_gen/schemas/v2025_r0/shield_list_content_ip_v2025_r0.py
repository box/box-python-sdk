from enum import Enum

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShieldListContentIpV2025R0TypeField(str, Enum):
    IP = 'ip'


class ShieldListContentIpV2025R0(BaseObject):
    _discriminator = 'type', {'ip'}

    def __init__(
        self,
        ip_addresses: List[str],
        *,
        type: ShieldListContentIpV2025R0TypeField = ShieldListContentIpV2025R0TypeField.IP,
        **kwargs
    ):
        """
        :param ip_addresses: List of ips and cidrs.
        :type ip_addresses: List[str]
        :param type: The type of content in the shield list., defaults to ShieldListContentIpV2025R0TypeField.IP
        :type type: ShieldListContentIpV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.ip_addresses = ip_addresses
        self.type = type
