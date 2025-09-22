from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.web_link import WebLink

from box_sdk_gen.managers.web_links import CreateWebLinkParent

from box_sdk_gen.managers.shared_links_web_links import AddShareLinkToWebLinkSharedLink

from box_sdk_gen.managers.shared_links_web_links import (
    AddShareLinkToWebLinkSharedLinkAccessField,
)

from box_sdk_gen.managers.shared_links_web_links import (
    UpdateSharedLinkOnWebLinkSharedLink,
)

from box_sdk_gen.managers.shared_links_web_links import (
    UpdateSharedLinkOnWebLinkSharedLinkAccessField,
)

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from box_sdk_gen.internal.utils import create_null

client: BoxClient = get_default_client()


def testSharedLinksWebLinks():
    parent: FolderFull = client.folders.get_folder_by_id('0')
    web_link: WebLink = client.web_links.create_web_link(
        'https://www.box.com',
        CreateWebLinkParent(id=parent.id),
        name=get_uuid(),
        description='Weblink description',
    )
    web_link_id: str = web_link.id
    client.shared_links_web_links.add_share_link_to_web_link(
        web_link_id,
        'shared_link',
        shared_link=AddShareLinkToWebLinkSharedLink(
            access=AddShareLinkToWebLinkSharedLinkAccessField.OPEN,
            password='Secret123@',
        ),
    )
    web_link_from_api: WebLink = (
        client.shared_links_web_links.get_shared_link_for_web_link(
            web_link_id, 'shared_link'
        )
    )
    assert to_string(web_link_from_api.shared_link.access) == 'open'
    user_id: str = get_env_var('USER_ID')
    user_client: BoxClient = get_default_client_with_user_subject(user_id)
    web_link_from_shared_link_password: WebLink = (
        user_client.shared_links_web_links.find_web_link_for_shared_link(
            ''.join(
                [
                    'shared_link=',
                    web_link_from_api.shared_link.url,
                    '&shared_link_password=Secret123@',
                ]
            )
        )
    )
    assert web_link_id == web_link_from_shared_link_password.id
    with pytest.raises(Exception):
        user_client.shared_links_web_links.find_web_link_for_shared_link(
            ''.join(
                [
                    'shared_link=',
                    web_link_from_api.shared_link.url,
                    '&shared_link_password=incorrectPassword',
                ]
            )
        )
    updated_web_link: WebLink = (
        client.shared_links_web_links.update_shared_link_on_web_link(
            web_link_id,
            'shared_link',
            shared_link=UpdateSharedLinkOnWebLinkSharedLink(
                access=UpdateSharedLinkOnWebLinkSharedLinkAccessField.COLLABORATORS
            ),
        )
    )
    assert to_string(updated_web_link.shared_link.access) == 'collaborators'
    client.shared_links_web_links.remove_shared_link_from_web_link(
        web_link_id, 'shared_link', shared_link=create_null()
    )
    web_link_from_api_after_remove: WebLink = (
        client.shared_links_web_links.get_shared_link_for_web_link(
            web_link_id, 'shared_link'
        )
    )
    assert web_link_from_api_after_remove.shared_link == None
    client.web_links.delete_web_link_by_id(web_link_id)
