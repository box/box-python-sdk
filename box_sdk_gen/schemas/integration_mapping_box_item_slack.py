from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class IntegrationMappingBoxItemSlackTypeField(str, Enum):
    FOLDER = 'folder'


class IntegrationMappingBoxItemSlack(BaseObject):
    _discriminator = 'type', {'folder'}

    def __init__(
        self,
        id: str,
        *,
        type: IntegrationMappingBoxItemSlackTypeField = IntegrationMappingBoxItemSlackTypeField.FOLDER,
        **kwargs
    ):
        """
        :param id: ID of the mapped item (of type referenced in `type`).
        :type id: str
        :param type: Type of the mapped item referenced in `id`., defaults to IntegrationMappingBoxItemSlackTypeField.FOLDER
        :type type: IntegrationMappingBoxItemSlackTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
