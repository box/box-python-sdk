from datetime import datetime

import pytest

from boxsdk.object.collaboration import CollaborationRole

from test.integration_new.context_managers.box_test_file import BoxTestFile
from test.integration_new.context_managers.box_test_folder import BoxTestFolder

FILE_TESTS_DIRECTORY_NAME = 'collaboration-integration-tests'


@pytest.fixture(scope="module", autouse=True)
def parent_folder():
    with BoxTestFolder(name=f'{FILE_TESTS_DIRECTORY_NAME} {datetime.now()}') as folder:
        yield folder


def test_collaboration(parent_folder, small_file_path, other_user,):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as test_file:
        collaboration = test_file.collaborate(other_user, CollaborationRole.VIEWER)
        try:
            assert collaboration.item.id == test_file.id
            assert collaboration.accessible_by.id == other_user.id
            assert collaboration.role == CollaborationRole.VIEWER

            updated_expiration_date = '2088-01-01T00:00:00-08:00'
            collaboration_update = {'role': CollaborationRole.EDITOR, 'expires_at': updated_expiration_date}
            updated_collaboration = collaboration.update_info(data=collaboration_update)

            assert updated_collaboration.role == CollaborationRole.EDITOR
            assert updated_collaboration.expires_at != collaboration.expires_at
            assert updated_collaboration.expires_at == updated_expiration_date
        finally:
            collaboration.delete()
