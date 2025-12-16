from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputEmailValidationValidationTypeField(str, Enum):
    EMAIL = 'email'


class SignRequestSignerInputEmailValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: SignRequestSignerInputEmailValidationValidationTypeField = SignRequestSignerInputEmailValidationValidationTypeField.EMAIL,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input is an email address., defaults to SignRequestSignerInputEmailValidationValidationTypeField.EMAIL
        :type validation_type: SignRequestSignerInputEmailValidationValidationTypeField, optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
