from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputNumberWithCommaValidationValidationTypeField(str, Enum):
    NUMBER_WITH_COMMA = 'number_with_comma'


class SignRequestSignerInputNumberWithCommaValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: Optional[
            SignRequestSignerInputNumberWithCommaValidationValidationTypeField
        ] = None,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input uses a number format with a comma as the decimal separator (for example, 1,23)., defaults to None
        :type validation_type: Optional[SignRequestSignerInputNumberWithCommaValidationValidationTypeField], optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
