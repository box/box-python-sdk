from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class IntegrationMappingPartnerItemTeamsTypeField(str, Enum):
    CHANNEL = 'channel'
    TEAM = 'team'


class IntegrationMappingPartnerItemTeams(BaseObject):
    _discriminator = 'type', {'channel', 'team'}

    def __init__(
        self,
        type: IntegrationMappingPartnerItemTeamsTypeField,
        id: str,
        tenant_id: str,
        **kwargs
    ):
        """
        :param type: Type of the mapped item referenced in `id`.
        :type type: IntegrationMappingPartnerItemTeamsTypeField
        :param id: ID of the mapped item (of type referenced in `type`).
        :type id: str
        :param tenant_id: ID of the tenant that is registered with Microsoft Teams.
        :type tenant_id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.tenant_id = tenant_id
