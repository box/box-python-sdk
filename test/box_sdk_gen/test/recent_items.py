from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.recent_items import RecentItems

from box_sdk_gen.internal.utils import decode_base_64

from box_sdk_gen.internal.utils import get_env_var

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject


def testRecentItems():
    client: BoxClient = get_default_client_with_user_subject(get_env_var('USER_ID'))
    recent_items: RecentItems = client.recent_items.get_recent_items()
    assert len(recent_items.entries) >= 0
