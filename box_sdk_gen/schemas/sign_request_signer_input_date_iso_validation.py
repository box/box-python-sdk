from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputDateIsoValidationValidationTypeField(str, Enum):
    DATE_ISO = 'date_iso'


class SignRequestSignerInputDateIsoValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: Optional[
            SignRequestSignerInputDateIsoValidationValidationTypeField
        ] = None,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input uses the ISO date format `YYYY-MM-DD`., defaults to None
        :type validation_type: Optional[SignRequestSignerInputDateIsoValidationValidationTypeField], optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
