from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputSsnValidationValidationTypeField(str, Enum):
    SSN = 'ssn'


class SignRequestSignerInputSsnValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: SignRequestSignerInputSsnValidationValidationTypeField = SignRequestSignerInputSsnValidationValidationTypeField.SSN,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input is a Social Security Number (SSN)., defaults to SignRequestSignerInputSsnValidationValidationTypeField.SSN
        :type validation_type: SignRequestSignerInputSsnValidationValidationTypeField, optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
