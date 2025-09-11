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

from box_sdk_gen.schemas.v2025_r0.shield_list_content_request_v2025_r0 import (
    ShieldListContentRequestV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError


class ShieldListsUpdateV2025R0(BaseObject):
    def __init__(
        self,
        name: str,
        content: ShieldListContentRequestV2025R0,
        *,
        description: Optional[str] = None,
        **kwargs
    ):
        """
        :param name: The name of the shield list.
        :type name: str
        :param description: Optional description of Shield List., defaults to None
        :type description: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.name = name
        self.content = content
        self.description = description
