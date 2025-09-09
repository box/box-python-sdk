from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.box.errors import BoxSDKError


class IntegrationMappingPartnerItemSlackTypeField(str, Enum):
    CHANNEL = 'channel'


class IntegrationMappingPartnerItemSlack(BaseObject):
    _discriminator = 'type', {'channel'}

    def __init__(
        self,
        id: str,
        *,
        type: IntegrationMappingPartnerItemSlackTypeField = IntegrationMappingPartnerItemSlackTypeField.CHANNEL,
        slack_workspace_id: Optional[str] = None,
        slack_org_id: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: ID of the mapped item (of type referenced in `type`).
        :type id: str
        :param type: Type of the mapped item referenced in `id`., defaults to IntegrationMappingPartnerItemSlackTypeField.CHANNEL
        :type type: IntegrationMappingPartnerItemSlackTypeField, optional
        :param slack_workspace_id: ID of the Slack workspace with which the item is associated. Use this parameter if Box for Slack is installed at a workspace level. Do not use `slack_org_id` at the same time., defaults to None
        :type slack_workspace_id: Optional[str], optional
        :param slack_org_id: ID of the Slack org with which the item is associated. Use this parameter if Box for Slack is installed at the org level. Do not use `slack_workspace_id` at the same time., defaults to None
        :type slack_org_id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.slack_workspace_id = slack_workspace_id
        self.slack_org_id = slack_org_id
