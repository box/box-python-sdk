from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class TemplateSignerVerificationMethodLoginTypeField(str, Enum):
    LOGIN = 'login'


class TemplateSignerVerificationMethodLogin(BaseObject):
    _discriminator = 'type', {'login'}

    def __init__(
        self,
        *,
        type: TemplateSignerVerificationMethodLoginTypeField = TemplateSignerVerificationMethodLoginTypeField.LOGIN,
        **kwargs
    ):
        """
        :param type: The type of verification method., defaults to TemplateSignerVerificationMethodLoginTypeField.LOGIN
        :type type: TemplateSignerVerificationMethodLoginTypeField, optional
        """
        super().__init__(**kwargs)
        self.type = type
