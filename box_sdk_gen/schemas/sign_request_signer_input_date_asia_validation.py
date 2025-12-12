from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputDateAsiaValidationValidationTypeField(str, Enum):
    DATE_ASIA = 'date_asia'


class SignRequestSignerInputDateAsiaValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: Optional[
            SignRequestSignerInputDateAsiaValidationValidationTypeField
        ] = None,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input uses the Asian date format `YYYY/MM/DD`., defaults to None
        :type validation_type: Optional[SignRequestSignerInputDateAsiaValidationValidationTypeField], optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
