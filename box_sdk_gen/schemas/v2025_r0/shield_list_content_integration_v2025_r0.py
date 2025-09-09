from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.box.errors import BoxSDKError


class ShieldListContentIntegrationV2025R0TypeField(str, Enum):
    INTEGRATION = 'integration'


class ShieldListContentIntegrationV2025R0IntegrationsField(BaseObject):
    def __init__(self, *, id: Optional[str] = None, **kwargs):
        """
        :param id: The ID of the integration., defaults to None
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id


class ShieldListContentIntegrationV2025R0(BaseObject):
    _discriminator = 'type', {'integration'}

    def __init__(
        self,
        integrations: List[ShieldListContentIntegrationV2025R0IntegrationsField],
        *,
        type: ShieldListContentIntegrationV2025R0TypeField = ShieldListContentIntegrationV2025R0TypeField.INTEGRATION,
        **kwargs
    ):
        """
        :param integrations: List of integration.
        :type integrations: List[ShieldListContentIntegrationV2025R0IntegrationsField]
        :param type: The type of content in the shield list., defaults to ShieldListContentIntegrationV2025R0TypeField.INTEGRATION
        :type type: ShieldListContentIntegrationV2025R0TypeField, optional
        """
        super().__init__(**kwargs)
        self.integrations = integrations
        self.type = type
