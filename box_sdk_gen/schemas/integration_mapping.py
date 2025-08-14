from enum import Enum

from typing import Optional

from box_sdk_gen.schemas.integration_mapping_base import IntegrationMappingBaseTypeField

from box_sdk_gen.schemas.integration_mapping_base import IntegrationMappingBase

from box_sdk_gen.schemas.integration_mapping_slack_options import (
    IntegrationMappingSlackOptions,
)

from box_sdk_gen.schemas.user_integration_mappings import UserIntegrationMappings

from box_sdk_gen.schemas.integration_mapping_partner_item_slack import (
    IntegrationMappingPartnerItemSlack,
)

from box_sdk_gen.schemas.folder_mini import FolderMini

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class IntegrationMappingIntegrationTypeField(str, Enum):
    SLACK = 'slack'


class IntegrationMapping(IntegrationMappingBase):
    def __init__(
        self,
        partner_item: IntegrationMappingPartnerItemSlack,
        box_item: FolderMini,
        id: str,
        *,
        integration_type: Optional[IntegrationMappingIntegrationTypeField] = None,
        is_manually_created: Optional[bool] = None,
        options: Optional[IntegrationMappingSlackOptions] = None,
        created_by: Optional[UserIntegrationMappings] = None,
        modified_by: Optional[UserIntegrationMappings] = None,
        created_at: Optional[DateTime] = None,
        modified_at: Optional[DateTime] = None,
        type: IntegrationMappingBaseTypeField = IntegrationMappingBaseTypeField.INTEGRATION_MAPPING,
        **kwargs
    ):
        """
                :param partner_item: Mapped item object for Slack.
                :type partner_item: IntegrationMappingPartnerItemSlack
                :param box_item: The Box folder, to which the object from the
        partner app domain (referenced in `partner_item_id`) is mapped.
                :type box_item: FolderMini
                :param id: A unique identifier of a folder mapping
        (part of a composite key together
        with `integration_type`).
                :type id: str
                :param integration_type: Identifies the Box partner app,
        with which the mapping is associated.
        Currently only supports Slack.
        (part of the composite key together with `id`)., defaults to None
                :type integration_type: Optional[IntegrationMappingIntegrationTypeField], optional
                :param is_manually_created: Identifies whether the mapping has
        been manually set
        (as opposed to being automatically created)., defaults to None
                :type is_manually_created: Optional[bool], optional
                :param created_by: An object representing the user who
        created the integration mapping., defaults to None
                :type created_by: Optional[UserIntegrationMappings], optional
                :param modified_by: The user who
        last modified the integration mapping., defaults to None
                :type modified_by: Optional[UserIntegrationMappings], optional
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
        self.is_manually_created = is_manually_created
        self.options = options
        self.created_by = created_by
        self.modified_by = modified_by
        self.created_at = created_at
        self.modified_at = modified_at
