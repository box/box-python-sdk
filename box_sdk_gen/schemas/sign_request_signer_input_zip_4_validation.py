from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerInputZip4ValidationValidationTypeField(str, Enum):
    ZIP_4 = 'zip_4'


class SignRequestSignerInputZip4Validation(BaseObject):
    def __init__(
        self,
        *,
        validation_type: SignRequestSignerInputZip4ValidationValidationTypeField = SignRequestSignerInputZip4ValidationValidationTypeField.ZIP_4,
        **kwargs
    ):
        """
        :param validation_type: Validates that the text input is a ZIP+4 code., defaults to SignRequestSignerInputZip4ValidationValidationTypeField.ZIP_4
        :type validation_type: SignRequestSignerInputZip4ValidationValidationTypeField, optional
        """
        super().__init__(**kwargs)
        self.validation_type = validation_type
