from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.schemas.group_full import GroupFull

from box_sdk_gen.schemas.collaboration import Collaboration

from box_sdk_gen.managers.user_collaborations import CreateCollaborationItem

from box_sdk_gen.managers.user_collaborations import CreateCollaborationItemTypeField

from box_sdk_gen.managers.user_collaborations import CreateCollaborationAccessibleBy

from box_sdk_gen.managers.user_collaborations import (
    CreateCollaborationAccessibleByTypeField,
)

from box_sdk_gen.managers.user_collaborations import CreateCollaborationRole

from box_sdk_gen.schemas.collaborations import Collaborations

from box_sdk_gen.schemas.collaborations_offset_paginated import (
    CollaborationsOffsetPaginated,
)

from box_sdk_gen.managers.list_collaborations import GetCollaborationsStatus

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import create_new_folder

from test.box_sdk_gen.test.commons import upload_new_file


def testListCollaborations():
    client: BoxClient = get_default_client()
    folder: FolderFull = create_new_folder()
    file: FileFull = upload_new_file()
    group: GroupFull = client.groups.create_group(get_uuid())
    group_collaboration: Collaboration = (
        client.user_collaborations.create_collaboration(
            CreateCollaborationItem(
                type=CreateCollaborationItemTypeField.FOLDER, id=folder.id
            ),
            CreateCollaborationAccessibleBy(
                type=CreateCollaborationAccessibleByTypeField.GROUP, id=group.id
            ),
            CreateCollaborationRole.EDITOR,
        )
    )
    file_collaboration: Collaboration = client.user_collaborations.create_collaboration(
        CreateCollaborationItem(type=CreateCollaborationItemTypeField.FILE, id=file.id),
        CreateCollaborationAccessibleBy(
            type=CreateCollaborationAccessibleByTypeField.USER,
            id=get_env_var('USER_ID'),
        ),
        CreateCollaborationRole.EDITOR,
    )
    assert to_string(group_collaboration.role) == 'editor'
    assert to_string(group_collaboration.type) == 'collaboration'
    file_collaborations: Collaborations = (
        client.list_collaborations.get_file_collaborations(file.id)
    )
    assert len(file_collaborations.entries) > 0
    folder_collaborations: Collaborations = (
        client.list_collaborations.get_folder_collaborations(folder.id)
    )
    assert len(folder_collaborations.entries) > 0
    pending_collaborations: CollaborationsOffsetPaginated = (
        client.list_collaborations.get_collaborations(GetCollaborationsStatus.PENDING)
    )
    assert len(pending_collaborations.entries) >= 0
    group_collaborations: CollaborationsOffsetPaginated = (
        client.list_collaborations.get_group_collaborations(group.id)
    )
    assert len(group_collaborations.entries) > 0
    client.user_collaborations.delete_collaboration_by_id(group_collaboration.id)
    client.files.delete_file_by_id(file.id)
    client.folders.delete_folder_by_id(folder.id)
    client.groups.delete_group_by_id(group.id)
