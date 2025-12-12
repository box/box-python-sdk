from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputDateUsValidationValidationTypeField(str, Enum):
    DATE_US = 'date_us'


class SignRequestSignerInputDateUsValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: Optional[
            SignRequestSignerInputDateUsValidationValidationTypeField
        ] = None,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input uses the US date format `MM/DD/YYYY`., defaults to None
        :type validation_type: Optional[SignRequestSignerInputDateUsValidationValidationTypeField], optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
