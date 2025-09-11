from box_sdk_gen.internal.base_object import BaseObject

from box_sdk_gen.schemas.integration_mapping_partner_item_teams_create_request import (
    IntegrationMappingPartnerItemTeamsCreateRequest,
)

from box_sdk_gen.schemas.folder_reference import FolderReference

from box_sdk_gen.box.errors import BoxSDKError


class IntegrationMappingTeamsCreateRequest(BaseObject):
    def __init__(
        self,
        partner_item: IntegrationMappingPartnerItemTeamsCreateRequest,
        box_item: FolderReference,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.partner_item = partner_item
        self.box_item = box_item
