from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.app_item import AppItem

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testSharedLinksAppItems():
    app_item_shared_link: str = get_env_var('APP_ITEM_SHARED_LINK')
    app_item: AppItem = client.shared_links_app_items.find_app_item_for_shared_link(
        ''.join(['shared_link=', app_item_shared_link])
    )
    assert to_string(app_item.type) == 'app_item'
    assert app_item.application_type == 'hubs'
