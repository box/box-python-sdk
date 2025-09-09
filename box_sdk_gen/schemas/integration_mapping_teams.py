from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.integration_mapping_base import IntegrationMappingBaseTypeField

from box_sdk_gen.schemas.integration_mapping_base import IntegrationMappingBase

from box_sdk_gen.schemas.integration_mapping_partner_item_teams import (
    IntegrationMappingPartnerItemTeams,
)

from box_sdk_gen.schemas.folder_reference import FolderReference

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class IntegrationMappingTeamsIntegrationTypeField(str, Enum):
    TEAMS = 'teams'


class IntegrationMappingTeams(IntegrationMappingBase):
    def __init__(
        self,
        partner_item: IntegrationMappingPartnerItemTeams,
        box_item: FolderReference,
        id: str,
        *,
        integration_type: Optional[IntegrationMappingTeamsIntegrationTypeField] = None,
        is_overridden_by_manual_mapping: Optional[bool] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        type: IntegrationMappingBaseTypeField = IntegrationMappingBaseTypeField.INTEGRATION_MAPPING,
        **kwargs
    ):
        """
                :param partner_item: Mapped item object for Teams.
                :type partner_item: IntegrationMappingPartnerItemTeams
                :param id: A unique identifier of a folder mapping
        (part of a composite key together
        with `integration_type`).
                :type id: str
                :param integration_type: Identifies the Box partner app,
        with which the mapping is associated.
        Supports Slack and Teams.
        (part of the composite key together with `id`)., defaults to None
                :type integration_type: Optional[IntegrationMappingTeamsIntegrationTypeField], optional
                :param is_overridden_by_manual_mapping: Identifies whether the mapping has
        been manually set by the team owner from UI for channels
        (as opposed to being automatically created)., defaults to None
                :type is_overridden_by_manual_mapping: Optional[bool], optional
                :param created_at: When the integration mapping object was created., defaults to None
                :type created_at: Optional[DateTime], optional
                :param modified_at: When the integration mapping object was last modified., defaults to None
                :type modified_at: Optional[DateTime], optional
                :param type: Mapping type., defaults to IntegrationMappingBaseTypeField.INTEGRATION_MAPPING
                :type type: IntegrationMappingBaseTypeField, optional
        """
        super().__init__(id=id, type=type, **kwargs)
        self.partner_item = partner_item
        self.box_item = box_item
        self.integration_type = integration_type
        self.is_overridden_by_manual_mapping = is_overridden_by_manual_mapping
        self.created_at = created_at
        self.modified_at = modified_at
