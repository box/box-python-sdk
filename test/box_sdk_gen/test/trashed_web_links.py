from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.managers.web_links import CreateWebLinkParent

from box_sdk_gen.schemas.trash_web_link import TrashWebLink

from box_sdk_gen.schemas.trash_web_link_restored import TrashWebLinkRestored

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

client: BoxClient = get_default_client()


def testTrashedWebLinks():
    url: str = 'https://www.box.com'
    parent: FolderFull = client.folders.get_folder_by_id('0')
    name: str = get_uuid()
    description: str = 'Weblink description'
    weblink: WebLink = client.web_links.create_web_link(
        url, CreateWebLinkParent(id=parent.id), name=name, description=description
    )
    client.web_links.delete_web_link_by_id(weblink.id)
    from_trash: TrashWebLink = client.trashed_web_links.get_trashed_web_link_by_id(
        weblink.id
    )
    assert from_trash.id == weblink.id
    assert from_trash.name == weblink.name
    from_api_after_trashed: WebLink = client.web_links.get_web_link_by_id(weblink.id)
    assert to_string(from_api_after_trashed.item_status) == 'trashed'
    restored_weblink: TrashWebLinkRestored = (
        client.trashed_web_links.restore_weblink_from_trash(weblink.id)
    )
    from_api: WebLink = client.web_links.get_web_link_by_id(weblink.id)
    assert restored_weblink.id == from_api.id
    assert restored_weblink.name == from_api.name
    client.web_links.delete_web_link_by_id(weblink.id)
    client.trashed_web_links.delete_trashed_web_link_by_id(weblink.id)
    with pytest.raises(Exception):
        client.trashed_web_links.get_trashed_web_link_by_id(weblink.id)
