from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class SignRequestSignerVerificationMethodLoginTypeField(str, Enum):
    LOGIN = 'login'


class SignRequestSignerVerificationMethodLogin(BaseObject):
    _discriminator = 'type', {'login'}

    def __init__(
        self,
        *,
        type: SignRequestSignerVerificationMethodLoginTypeField = SignRequestSignerVerificationMethodLoginTypeField.LOGIN,
        **kwargs
    ):
        """
        :param type: The type of verification method., defaults to SignRequestSignerVerificationMethodLoginTypeField.LOGIN
        :type type: SignRequestSignerVerificationMethodLoginTypeField, optional
        """
        super().__init__(**kwargs)
        self.type = type
