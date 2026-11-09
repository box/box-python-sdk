from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerVerificationMethodCacPivTypeField(str, Enum):
    CAC_PIV = 'cac_piv'


class SignRequestSignerVerificationMethodCacPiv(BaseObject):
    _discriminator = 'type', {'cac_piv'}

    def __init__(
        self,
        *,
        type: SignRequestSignerVerificationMethodCacPivTypeField = SignRequestSignerVerificationMethodCacPivTypeField.CAC_PIV,
        **kwargs
    ):
        """
        :param type: The type of verification method., defaults to SignRequestSignerVerificationMethodCacPivTypeField.CAC_PIV
        :type type: SignRequestSignerVerificationMethodCacPivTypeField, optional
        """
        super().__init__(**kwargs)
        self.type = type
