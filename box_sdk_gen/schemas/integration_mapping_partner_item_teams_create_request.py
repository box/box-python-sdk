from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class IntegrationMappingPartnerItemTeamsCreateRequestTypeField(str, Enum):
    CHANNEL = 'channel'
    TEAM = 'team'


class IntegrationMappingPartnerItemTeamsCreateRequest(BaseObject):
    _discriminator = 'type', {'channel', 'team'}

    def __init__(
        self,
        type: IntegrationMappingPartnerItemTeamsCreateRequestTypeField,
        id: str,
        tenant_id: str,
        team_id: str,
        **kwargs
    ):
        """
        :param type: Type of the mapped item referenced in `id`.
        :type type: IntegrationMappingPartnerItemTeamsCreateRequestTypeField
        :param id: ID of the mapped item (of type referenced in `type`).
        :type id: str
        :param tenant_id: ID of the tenant that is registered with Microsoft Teams.
        :type tenant_id: str
        :param team_id: ID of the team that is registered with Microsoft Teams.
        :type team_id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id
        self.tenant_id = tenant_id
        self.team_id = team_id
