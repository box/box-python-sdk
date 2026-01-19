from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputCustomValidationValidationTypeField(str, Enum):
    CUSTOM = 'custom'


class SignRequestSignerInputCustomValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: SignRequestSignerInputCustomValidationValidationTypeField = SignRequestSignerInputCustomValidationValidationTypeField.CUSTOM,
        custom_regex: Optional[str] = None,
        custom_error_message: Optional[str] = None,
        **kwargs
    ):
        """
                :param validation_type: Defines the validation format for the text input as custom.
        A custom regular expression is used for validation., defaults to SignRequestSignerInputCustomValidationValidationTypeField.CUSTOM
                :type validation_type: SignRequestSignerInputCustomValidationValidationTypeField, optional
                :param custom_regex: Regular expression used for validation., defaults to None
                :type custom_regex: Optional[str], optional
                :param custom_error_message: Error message shown if input fails custom regular expression validation., defaults to None
                :type custom_error_message: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
        self.custom_regex = custom_regex
        self.custom_error_message = custom_error_message
