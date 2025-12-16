from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputZipValidationValidationTypeField(str, Enum):
    ZIP = 'zip'


class SignRequestSignerInputZipValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: SignRequestSignerInputZipValidationValidationTypeField = SignRequestSignerInputZipValidationValidationTypeField.ZIP,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input is a ZIP code., defaults to SignRequestSignerInputZipValidationValidationTypeField.ZIP
        :type validation_type: SignRequestSignerInputZipValidationValidationTypeField, optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
