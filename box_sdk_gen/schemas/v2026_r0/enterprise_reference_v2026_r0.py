from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class EnterpriseReferenceV2026R0TypeField(str, Enum):
    ENTERPRISE = 'enterprise'


class EnterpriseReferenceV2026R0(BaseObject):
    _discriminator = 'type', {'enterprise'}

    def __init__(
        self,
        id: str,
        *,
        type: EnterpriseReferenceV2026R0TypeField = EnterpriseReferenceV2026R0TypeField.ENTERPRISE,
        **kwargs
    ):
        """
        :param id: The unique identifier for this enterprise.
        :type id: str
        :param type: The value will always be `enterprise`., defaults to EnterpriseReferenceV2026R0TypeField.ENTERPRISE
        :type type: EnterpriseReferenceV2026R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
