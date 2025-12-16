from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputCustomValidationValidationTypeField(str, Enum):
    CUSTOM = 'custom'


class SignRequestSignerInputCustomValidation(BaseObject):
    def __init__(
        self,
        custom_regex: str,
        custom_error_message: str,
        *,
        validation_type: SignRequestSignerInputCustomValidationValidationTypeField = SignRequestSignerInputCustomValidationValidationTypeField.CUSTOM,
        **kwargs
    ):
        """
                :param custom_regex: Regular expression used for validation.
                :type custom_regex: str
                :param custom_error_message: Error message shown if input fails custom regular expression validation.
                :type custom_error_message: str
                :param validation_type: Defines the validation format for the text input as custom.
        A custom regular expression is used for validation., defaults to SignRequestSignerInputCustomValidationValidationTypeField.CUSTOM
                :type validation_type: SignRequestSignerInputCustomValidationValidationTypeField, optional
        """
        super().__init__(**kwargs)
        self.custom_regex = custom_regex
        self.custom_error_message = custom_error_message
        self.validation_type = validation_type
