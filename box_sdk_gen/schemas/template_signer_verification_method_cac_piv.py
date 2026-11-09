from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class TemplateSignerVerificationMethodCacPivTypeField(str, Enum):
    CAC_PIV = 'cac_piv'


class TemplateSignerVerificationMethodCacPiv(BaseObject):
    _discriminator = 'type', {'cac_piv'}

    def __init__(
        self,
        *,
        type: TemplateSignerVerificationMethodCacPivTypeField = TemplateSignerVerificationMethodCacPivTypeField.CAC_PIV,
        **kwargs
    ):
        """
        :param type: The type of verification method., defaults to TemplateSignerVerificationMethodCacPivTypeField.CAC_PIV
        :type type: TemplateSignerVerificationMethodCacPivTypeField, optional
        """
        super().__init__(**kwargs)
        self.type = type
