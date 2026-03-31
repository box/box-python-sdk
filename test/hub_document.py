from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.v2025_r0.hub_v2025_r0 import HubV2025R0

from box_sdk_gen.schemas.v2025_r0.hub_document_pages_v2025_r0 import (
    HubDocumentPagesV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_document_page_v2025_r0 import (
    HubDocumentPageV2025R0,
)

from box_sdk_gen.schemas.v2025_r0.hub_document_blocks_v2025_r0 import (
    HubDocumentBlocksV2025R0,
)

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

from box_sdk_gen.schemas.v2025_r0.hub_document_block_entry_v2025_r0 import (
    HubDocumentBlockEntryV2025R0,
)

from test.commons import get_default_client_with_user_subject

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))


def testGetHubDocumentPagesAndBlocks():
    hub_title: str = get_uuid()
    created_hub: HubV2025R0 = client.hubs.create_hub_v2025_r0(hub_title)
    hub_id: str = created_hub.id
    pages: HubDocumentPagesV2025R0 = (
        client.hub_document.get_hub_document_pages_v2025_r0(hub_id)
    )
    assert len(pages.entries) > 0
    assert to_string(pages.type) == 'document_pages'
    first_page: HubDocumentPageV2025R0 = pages.entries[0]
    assert to_string(first_page.type) == 'page'
    page_id: str = first_page.id
    blocks: HubDocumentBlocksV2025R0 = (
        client.hub_document.get_hub_document_blocks_v2025_r0(hub_id, page_id)
    )
    assert to_string(blocks.type) == 'document_blocks'
    assert len(blocks.entries) > 0
    first_block: HubDocumentBlockEntryV2025R0 = blocks.entries[0]
    assert to_string(first_block.type) == 'item_list'
    client.hubs.delete_hub_by_id_v2025_r0(hub_id)
