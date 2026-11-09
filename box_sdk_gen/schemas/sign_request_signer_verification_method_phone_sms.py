from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerVerificationMethodPhoneSmsTypeField(str, Enum):
    PHONE = 'phone'


class SignRequestSignerVerificationMethodPhoneSms(BaseObject):
    _discriminator = 'type', {'phone'}

    def __init__(
        self,
        phone_number: str,
        *,
        type: SignRequestSignerVerificationMethodPhoneSmsTypeField = SignRequestSignerVerificationMethodPhoneSmsTypeField.PHONE,
        **kwargs
    ):
        """
        :param phone_number: The phone number to where the message will be sent.
        :type phone_number: str
        :param type: The type of verification method., defaults to SignRequestSignerVerificationMethodPhoneSmsTypeField.PHONE
        :type type: SignRequestSignerVerificationMethodPhoneSmsTypeField, optional
        """
        super().__init__(**kwargs)
        self.phone_number = phone_number
        self.type = type
