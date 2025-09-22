from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.managers.folders import CreateFolderParent

from box_sdk_gen.managers.shared_links_folders import AddShareLinkToFolderSharedLink

from box_sdk_gen.managers.shared_links_folders import (
    AddShareLinkToFolderSharedLinkAccessField,
)

from box_sdk_gen.managers.shared_links_folders import UpdateSharedLinkOnFolderSharedLink

from box_sdk_gen.managers.shared_links_folders import (
    UpdateSharedLinkOnFolderSharedLinkAccessField,
)

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from box_sdk_gen.internal.utils import create_null

client: BoxClient = get_default_client()


def testSharedLinksFolders():
    folder: FolderFull = client.folders.create_folder(
        get_uuid(), CreateFolderParent(id='0')
    )
    client.shared_links_folders.add_share_link_to_folder(
        folder.id,
        'shared_link',
        shared_link=AddShareLinkToFolderSharedLink(
            access=AddShareLinkToFolderSharedLinkAccessField.OPEN, password='Secret123@'
        ),
    )
    folder_from_api: FolderFull = (
        client.shared_links_folders.get_shared_link_for_folder(folder.id, 'shared_link')
    )
    assert to_string(folder_from_api.shared_link.access) == 'open'
    user_id: str = get_env_var('USER_ID')
    user_client: BoxClient = get_default_client_with_user_subject(user_id)
    folder_from_shared_link_password: FolderFull = (
        user_client.shared_links_folders.find_folder_for_shared_link(
            ''.join(
                [
                    'shared_link=',
                    folder_from_api.shared_link.url,
                    '&shared_link_password=Secret123@',
                ]
            )
        )
    )
    assert folder.id == folder_from_shared_link_password.id
    with pytest.raises(Exception):
        user_client.shared_links_folders.find_folder_for_shared_link(
            ''.join(
                [
                    'shared_link=',
                    folder_from_api.shared_link.url,
                    '&shared_link_password=incorrectPassword',
                ]
            )
        )
    updated_folder: FolderFull = (
        client.shared_links_folders.update_shared_link_on_folder(
            folder.id,
            'shared_link',
            shared_link=UpdateSharedLinkOnFolderSharedLink(
                access=UpdateSharedLinkOnFolderSharedLinkAccessField.COLLABORATORS
            ),
        )
    )
    assert to_string(updated_folder.shared_link.access) == 'collaborators'
    client.shared_links_folders.remove_shared_link_from_folder(
        folder.id, 'shared_link', shared_link=create_null()
    )
    folder_from_api_after_remove: FolderFull = (
        client.shared_links_folders.get_shared_link_for_folder(folder.id, 'shared_link')
    )
    assert folder_from_api_after_remove.shared_link == None
    client.folders.delete_folder_by_id(folder.id)
