from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class TemplateSignerVerificationMethodPhoneSmsTypeField(str, Enum):
    PHONE = 'phone'


class TemplateSignerVerificationMethodPhoneSms(BaseObject):
    _discriminator = 'type', {'phone'}

    def __init__(
        self,
        *,
        type: TemplateSignerVerificationMethodPhoneSmsTypeField = TemplateSignerVerificationMethodPhoneSmsTypeField.PHONE,
        **kwargs
    ):
        """
        :param type: The type of verification method., defaults to TemplateSignerVerificationMethodPhoneSmsTypeField.PHONE
        :type type: TemplateSignerVerificationMethodPhoneSmsTypeField, optional
        """
        super().__init__(**kwargs)
        self.type = type
