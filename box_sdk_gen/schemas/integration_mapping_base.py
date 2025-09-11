from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class IntegrationMappingBaseTypeField(str, Enum):
    INTEGRATION_MAPPING = 'integration_mapping'


class IntegrationMappingBase(BaseObject):
    _discriminator = 'type', {'integration_mapping'}

    def __init__(
        self,
        id: str,
        *,
        type: IntegrationMappingBaseTypeField = IntegrationMappingBaseTypeField.INTEGRATION_MAPPING,
        **kwargs
    ):
        """
                :param id: A unique identifier of a folder mapping
        (part of a composite key together
        with `integration_type`).
                :type id: str
                :param type: Mapping type., defaults to IntegrationMappingBaseTypeField.INTEGRATION_MAPPING
                :type type: IntegrationMappingBaseTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
