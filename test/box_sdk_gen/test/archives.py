from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.v2025_r0.archive_v2025_r0 import ArchiveV2025R0

from box_sdk_gen.schemas.v2025_r0.archives_v2025_r0 import ArchivesV2025R0

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject

user_id: str = get_env_var('USER_ID')

client: BoxClient = get_default_client_with_user_subject(user_id)


def testArchivesCreateListDelete():
    archive_name: str = get_uuid()
    archive_description: str = 'Test Archive Description'
    archive: ArchiveV2025R0 = client.archives.create_archive_v2025_r0(
        archive_name, description=archive_description
    )
    assert to_string(archive.type) == 'archive'
    assert archive.name == archive_name
    assert archive.description == archive_description
    new_archive_name: str = get_uuid()
    new_archive_description: str = 'Updated Archive Description'
    updated_archive: ArchiveV2025R0 = client.archives.update_archive_by_id_v2025_r0(
        archive.id, name=new_archive_name, description=new_archive_description
    )
    assert updated_archive.name == new_archive_name
    assert updated_archive.description == new_archive_description
    archives: ArchivesV2025R0 = client.archives.get_archives_v2025_r0(limit=100)
    assert len(archives.entries) > 0
    client.archives.delete_archive_by_id_v2025_r0(archive.id)
    with pytest.raises(Exception):
        client.archives.delete_archive_by_id_v2025_r0(archive.id)
