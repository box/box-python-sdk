from enum import Enum

from typing import List

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class ShieldListContentCountryV2025R0TypeField(str, Enum):
    COUNTRY = 'country'


class ShieldListContentCountryV2025R0(BaseObject):
    _discriminator = 'type', {'country'}

    def __init__(
        self,
        country_codes: List[str],
        *,
        type: ShieldListContentCountryV2025R0TypeField = ShieldListContentCountryV2025R0TypeField.COUNTRY,
        **kwargs
    ):
        """
        :param country_codes: List of country codes values.
        :type country_codes: List[str]
        :param type: The type of content in the shield list., defaults to ShieldListContentCountryV2025R0TypeField.COUNTRY
        :type type: ShieldListContentCountryV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.country_codes = country_codes
        self.type = type
