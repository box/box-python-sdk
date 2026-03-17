from typing import Union

from box_sdk_gen.schemas.v2025_r0.hub_paragraph_text_block_v2025_r0 import (
    HubParagraphTextBlockV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_section_title_text_block_v2025_r0 import (
    HubSectionTitleTextBlockV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_callout_box_text_block_v2025_r0 import (
    HubCalloutBoxTextBlockV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_item_list_block_v2025_r0 import (
    HubItemListBlockV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_divider_block_v2025_r0 import (
    HubDividerBlockV2025R0,
)

from box_sdk_gen.box.errors import BoxSDKError

HubDocumentBlockEntryV2025R0 = Union[
    HubParagraphTextBlockV2025R0,
    HubSectionTitleTextBlockV2025R0,
    HubCalloutBoxTextBlockV2025R0,
    HubItemListBlockV2025R0,
    HubDividerBlockV2025R0,
]
