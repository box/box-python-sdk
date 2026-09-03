from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputZipjpValidationValidationTypeField(str, Enum):
    ZIP_JP = 'zip_jp'


class SignRequestSignerInputZipjpValidation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: SignRequestSignerInputZipjpValidationValidationTypeField = SignRequestSignerInputZipjpValidationValidationTypeField.ZIP_JP,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input is a Japanese ZIP code., defaults to SignRequestSignerInputZipjpValidationValidationTypeField.ZIP_JP
        :type validation_type: SignRequestSignerInputZipjpValidationValidationTypeField, optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
