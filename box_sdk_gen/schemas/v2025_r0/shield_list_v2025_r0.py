from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import List

from box_sdk_gen.schemas.v2025_r0.shield_list_content_country_v2025_r0 import (
    ShieldListContentCountryV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_domain_v2025_r0 import (
    ShieldListContentDomainV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_email_v2025_r0 import (
    ShieldListContentEmailV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_ip_v2025_r0 import (
    ShieldListContentIpV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_integration_v2025_r0 import (
    ShieldListContentIntegrationV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.enterprise_reference_v2025_r0 import (
    EnterpriseReferenceV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.shield_list_content_v2025_r0 import (
    ShieldListContentV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.internal.utils import DateTime


class ShieldListV2025R0(BaseObject):
    def __init__(
        self,
        id: str,
        type: str,
        name: str,
        enterprise: EnterpriseReferenceV2025R0,
        created_at: DateTime,
        updated_at: DateTime,
        content: ShieldListContentV2025R0,
        *,
        description: Optional[str] = None,
        **kwargs
    ):
        """
        :param id: Unique identifier for the shield list.
        :type id: str
        :param type: Type of the object.
        :type type: str
        :param name: Name of the shield list.
        :type name: str
        :param created_at: ISO date time string when this shield list object was created.
        :type created_at: DateTime
        :param updated_at: ISO date time string when this shield list object was updated.
        :type updated_at: DateTime
        :param description: Description of Shield List., defaults to None
        :type description: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.name = name
        self.enterprise = enterprise
        self.created_at = created_at
        self.updated_at = updated_at
        self.content = content
        self.description = description
