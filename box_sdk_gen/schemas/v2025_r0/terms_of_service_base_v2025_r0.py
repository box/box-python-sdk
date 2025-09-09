from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class TermsOfServiceBaseV2025R0TypeField(str, Enum):
    TERMS_OF_SERVICE = 'terms_of_service'


class TermsOfServiceBaseV2025R0(BaseObject):
    _discriminator = 'type', {'terms_of_service'}

    def __init__(
        self,
        id: str,
        *,
        type: TermsOfServiceBaseV2025R0TypeField = TermsOfServiceBaseV2025R0TypeField.TERMS_OF_SERVICE,
        **kwargs
    ):
        """
        :param id: The unique identifier for this terms of service.
        :type id: str
        :param type: The value will always be `terms_of_service`., defaults to TermsOfServiceBaseV2025R0TypeField.TERMS_OF_SERVICE
        :type type: TermsOfServiceBaseV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
