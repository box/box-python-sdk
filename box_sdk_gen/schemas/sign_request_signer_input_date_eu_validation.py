from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputDateEuValidationValidationTypeField(str, Enum):
    DATE_EU = 'date_eu'


class SignRequestSignerInputDateEuValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: Optional[
            SignRequestSignerInputDateEuValidationValidationTypeField
        ] = None,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input uses the European date format `DD/MM/YYYY`., defaults to None
        :type validation_type: Optional[SignRequestSignerInputDateEuValidationValidationTypeField], optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
