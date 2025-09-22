from box_sdk_gen.internal.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.file_request import FileRequest

from box_sdk_gen.managers.file_requests import CreateFileRequestCopyFolder

from box_sdk_gen.managers.file_requests import CreateFileRequestCopyFolderTypeField

from box_sdk_gen.internal.utils import get_env_var

from test.box_sdk_gen.test.commons import get_default_client_with_user_subject


def testGetCopyUpdateDeleteFileRequest():
    file_request_id: str = get_env_var('BOX_FILE_REQUEST_ID')
    user_id: str = get_env_var('USER_ID')
    client: BoxClient = get_default_client_with_user_subject(user_id)
    file_request: FileRequest = client.file_requests.get_file_request_by_id(
        file_request_id
    )
    assert file_request.id == file_request_id
    assert to_string(file_request.type) == 'file_request'
    copied_file_request: FileRequest = client.file_requests.create_file_request_copy(
        file_request_id,
        CreateFileRequestCopyFolder(
            id=file_request.folder.id, type=CreateFileRequestCopyFolderTypeField.FOLDER
        ),
    )
    assert not copied_file_request.id == file_request_id
    assert copied_file_request.title == file_request.title
    assert copied_file_request.description == file_request.description
    updated_file_request: FileRequest = client.file_requests.update_file_request_by_id(
        copied_file_request.id, title='updated title', description='updated description'
    )
    assert updated_file_request.id == copied_file_request.id
    assert updated_file_request.title == 'updated title'
    assert updated_file_request.description == 'updated description'
    client.file_requests.delete_file_request_by_id(updated_file_request.id)
    with pytest.raises(Exception):
        client.file_requests.get_file_request_by_id(updated_file_request.id)
