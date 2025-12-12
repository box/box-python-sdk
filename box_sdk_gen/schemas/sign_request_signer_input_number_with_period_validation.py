from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputNumberWithPeriodValidationValidationTypeField(str, Enum):
    NUMBER_WITH_PERIOD = 'number_with_period'


class SignRequestSignerInputNumberWithPeriodValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: Optional[
            SignRequestSignerInputNumberWithPeriodValidationValidationTypeField
        ] = None,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input uses a number format with a period as the decimal separator (for example, 1.23)., defaults to None
        :type validation_type: Optional[SignRequestSignerInputNumberWithPeriodValidationValidationTypeField], optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
