from typing import Union

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

from box_sdk_gen.box.errors import BoxSDKError

ShieldListContentV2025R0 = Union[
    ShieldListContentCountryV2025R0,
    ShieldListContentDomainV2025R0,
    ShieldListContentEmailV2025R0,
    ShieldListContentIpV2025R0,
    ShieldListContentIntegrationV2025R0,
]
