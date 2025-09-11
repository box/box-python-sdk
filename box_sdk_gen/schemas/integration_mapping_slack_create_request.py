from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.integration_mapping_partner_item_slack import (
    IntegrationMappingPartnerItemSlack,
)

from box_sdk_gen.schemas.integration_mapping_box_item_slack import (
    IntegrationMappingBoxItemSlack,
)

from box_sdk_gen.schemas.integration_mapping_slack_options import (
    IntegrationMappingSlackOptions,
)

from box_sdk_gen.box.errors import BoxSDKError


class IntegrationMappingSlackCreateRequest(BaseObject):
    def __init__(
        self,
        partner_item: IntegrationMappingPartnerItemSlack,
        box_item: IntegrationMappingBoxItemSlack,
        *,
        options: Optional[IntegrationMappingSlackOptions] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.partner_item = partner_item
        self.box_item = box_item
        self.options = options
