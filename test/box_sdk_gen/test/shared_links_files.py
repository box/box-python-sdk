from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.managers.shared_links_files import AddShareLinkToFileSharedLink

from box_sdk_gen.managers.shared_links_files import (
    AddShareLinkToFileSharedLinkAccessField,
)

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.managers.shared_links_files import UpdateSharedLinkOnFileSharedLink

from box_sdk_gen.managers.shared_links_files import (
    UpdateSharedLinkOnFileSharedLinkAccessField,
)

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

from box_sdk_gen.internal.utils import create_null

client: BoxClient = get_default_client()


def testSharedLinksFiles():
    uploaded_files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=get_uuid(), parent=UploadFileAttributesParentField(id='0')
        ),
        generate_byte_stream(10),
    )
    file_id: str = uploaded_files.entries[0].id
    client.shared_links_files.add_share_link_to_file(
        file_id,
        'shared_link',
        shared_link=AddShareLinkToFileSharedLink(
            access=AddShareLinkToFileSharedLinkAccessField.OPEN, password='Secret123@'
        ),
    )
    file_from_api: FileFull = client.shared_links_files.get_shared_link_for_file(
        file_id, 'shared_link'
    )
    assert to_string(file_from_api.shared_link.access) == 'open'
    user_id: str = get_env_var('USER_ID')
    user_client: BoxClient = get_default_client_with_user_subject(user_id)
    file_from_shared_link_password: FileFull = (
        user_client.shared_links_files.find_file_for_shared_link(
            ''.join(
                [
                    'shared_link=',
                    file_from_api.shared_link.url,
                    '&shared_link_password=Secret123@',
                ]
            )
        )
    )
    assert file_id == file_from_shared_link_password.id
    with pytest.raises(Exception):
        user_client.shared_links_files.find_file_for_shared_link(
            ''.join(
                [
                    'shared_link=',
                    file_from_api.shared_link.url,
                    '&shared_link_password=incorrectPassword',
                ]
            )
        )
    updated_file: FileFull = client.shared_links_files.update_shared_link_on_file(
        file_id,
        'shared_link',
        shared_link=UpdateSharedLinkOnFileSharedLink(
            access=UpdateSharedLinkOnFileSharedLinkAccessField.COLLABORATORS
        ),
    )
    assert to_string(updated_file.shared_link.access) == 'collaborators'
    client.shared_links_files.remove_shared_link_from_file(
        file_id, 'shared_link', shared_link=create_null()
    )
    file_from_api_after_remove: FileFull = (
        client.shared_links_files.get_shared_link_for_file(file_id, 'shared_link')
    )
    assert file_from_api_after_remove.shared_link == None
    client.files.delete_file_by_id(file_id)
