from box_sdk_gen.internal.utils import to_string

from typing import Optional

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.user_full import UserFull

from box_sdk_gen.schemas.folder_full import FolderFull

from box_sdk_gen.schemas.collaboration import Collaboration

from box_sdk_gen.managers.user_collaborations import CreateCollaborationItem

from box_sdk_gen.managers.user_collaborations import CreateCollaborationItemTypeField

from box_sdk_gen.managers.user_collaborations import CreateCollaborationAccessibleBy

from box_sdk_gen.managers.user_collaborations import (
    CreateCollaborationAccessibleByTypeField,
)

from box_sdk_gen.managers.user_collaborations import CreateCollaborationRole

from box_sdk_gen.managers.user_collaborations import UpdateCollaborationByIdRole

from box_sdk_gen.schemas.collaborations import Collaborations

from box_sdk_gen.internal.utils import get_uuid

from test.box_sdk_gen.test.commons import get_default_client

from test.box_sdk_gen.test.commons import create_new_folder

client: BoxClient = get_default_client()


def testUserCollaborations():
    user_name: str = get_uuid()
    user_login: str = ''.join([get_uuid(), '@gmail.com'])
    user: UserFull = client.users.create_user(
        user_name, login=user_login, is_platform_access_only=True
    )
    folder: FolderFull = create_new_folder()
    collaboration: Collaboration = client.user_collaborations.create_collaboration(
        CreateCollaborationItem(
            type=CreateCollaborationItemTypeField.FOLDER, id=folder.id
        ),
        CreateCollaborationAccessibleBy(
            type=CreateCollaborationAccessibleByTypeField.USER, id=user.id
        ),
        CreateCollaborationRole.EDITOR,
    )
    assert to_string(collaboration.role) == 'editor'
    collaboration_id: str = collaboration.id
    collaboration_from_api: Collaboration = (
        client.user_collaborations.get_collaboration_by_id(collaboration_id)
    )
    assert collaboration_id == collaboration_from_api.id
    assert to_string(collaboration_from_api.status) == 'accepted'
    assert to_string(collaboration_from_api.type) == 'collaboration'
    assert collaboration_from_api.invite_email == None
    updated_collaboration: Optional[Collaboration] = (
        client.user_collaborations.update_collaboration_by_id(
            collaboration_id, role=UpdateCollaborationByIdRole.VIEWER
        )
    )
    assert to_string(updated_collaboration.role) == 'viewer'
    client.user_collaborations.delete_collaboration_by_id(collaboration_id)
    with pytest.raises(Exception):
        client.user_collaborations.get_collaboration_by_id(collaboration_id)
    client.folders.delete_folder_by_id(folder.id)
    client.users.delete_user_by_id(user.id)


def testConvertingUserCollaborationToOwnership():
    user_name: str = get_uuid()
    user_login: str = ''.join([get_uuid(), '@gmail.com'])
    user: UserFull = client.users.create_user(
        user_name, login=user_login, is_platform_access_only=True
    )
    folder: FolderFull = create_new_folder()
    collaboration: Collaboration = client.user_collaborations.create_collaboration(
        CreateCollaborationItem(
            type=CreateCollaborationItemTypeField.FOLDER, id=folder.id
        ),
        CreateCollaborationAccessibleBy(
            type=CreateCollaborationAccessibleByTypeField.USER, id=user.id
        ),
        CreateCollaborationRole.EDITOR,
    )
    assert to_string(collaboration.role) == 'editor'
    owner_collaboration: Optional[Collaboration] = (
        client.user_collaborations.update_collaboration_by_id(
            collaboration.id, role=UpdateCollaborationByIdRole.OWNER
        )
    )
    assert owner_collaboration == None
    folder_collaborations: Collaborations = (
        client.list_collaborations.get_folder_collaborations(folder.id)
    )
    folder_collaboration: Collaboration = folder_collaborations.entries[0]
    client.user_collaborations.delete_collaboration_by_id(folder_collaboration.id)
    user_client: BoxClient = client.with_as_user_header(user.id)
    user_client.folders.delete_folder_by_id(folder.id)
    user_client.trashed_folders.delete_trashed_folder_by_id(folder.id)
    client.users.delete_user_by_id(user.id)


def testExternalUserCollaborations():
    user_name: str = get_uuid()
    user_login: str = ''.join([get_uuid(), '@boxdemo.com'])
    folder: FolderFull = create_new_folder()
    collaboration: Collaboration = client.user_collaborations.create_collaboration(
        CreateCollaborationItem(
            type=CreateCollaborationItemTypeField.FOLDER, id=folder.id
        ),
        CreateCollaborationAccessibleBy(
            type=CreateCollaborationAccessibleByTypeField.USER, login=user_login
        ),
        CreateCollaborationRole.EDITOR,
    )
    assert to_string(collaboration.role) == 'editor'
    collaboration_id: str = collaboration.id
    collaboration_from_api: Collaboration = (
        client.user_collaborations.get_collaboration_by_id(collaboration_id)
    )
    assert collaboration_id == collaboration_from_api.id
    assert to_string(collaboration_from_api.status) == 'pending'
    assert to_string(collaboration_from_api.type) == 'collaboration'
    assert collaboration_from_api.invite_email == user_login
    updated_collaboration: Optional[Collaboration] = (
        client.user_collaborations.update_collaboration_by_id(
            collaboration_id, role=UpdateCollaborationByIdRole.VIEWER
        )
    )
    assert to_string(updated_collaboration.role) == 'viewer'
    client.user_collaborations.delete_collaboration_by_id(collaboration_id)
    with pytest.raises(Exception):
        client.user_collaborations.get_collaboration_by_id(collaboration_id)
    client.folders.delete_folder_by_id(folder.id)
