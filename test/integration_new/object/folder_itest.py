from datetime import datetime

import pytest
import hashlib
import os

from pytest_lazyfixture import lazy_fixture

from boxsdk.exception import BoxAPIException
from boxsdk.object.collaboration import CollaborationRole
from test.integration_new.context_managers.box_metadata_template import BoxTestMetadataTemplate
from test.integration_new.context_managers.box_test_group import BoxTestGroup
from test.integration_new.context_managers.box_test_web_link import BoxTestWebLink
from test.integration_new import CLIENT
from test.integration_new import util
from test.integration_new.context_managers.box_test_file import BoxTestFile
from test.integration_new.context_managers.box_test_folder import BoxTestFolder

FOLDER_TESTS_DIRECTORY_NAME = 'folder-integration-tests'


@pytest.fixture(scope="module", autouse=True)
def parent_folder():
    with BoxTestFolder(name=f'{FOLDER_TESTS_DIRECTORY_NAME} {datetime.now()}') as folder:
        yield folder


@pytest.fixture(scope="module")
def group():
    with BoxTestGroup() as group:
        yield group


def test_preflight_check(parent_folder):
    file_size = 1213
    accelerator_url = parent_folder.preflight_check(file_size, util.random_name())

    assert accelerator_url


def test_manual_chunked_upload(parent_folder, large_file, large_file_name):
    total_size = os.stat(large_file.path).st_size
    sha1 = hashlib.sha1()
    with open(large_file.path, 'rb') as content_stream:
        upload_session = parent_folder.create_upload_session(file_size=total_size, file_name=large_file_name)
        part_array = []
        for part_num in range(upload_session.total_parts):

            copied_length = 0
            chunk = b''
            while copied_length < upload_session.part_size:
                bytes_read = content_stream.read(upload_session.part_size - copied_length)
                if bytes_read is None:
                    continue
                if len(bytes_read) == 0:
                    break
                chunk += bytes_read
                copied_length += len(bytes_read)

            uploaded_part = upload_session.upload_part_bytes(chunk, part_num * upload_session.part_size, total_size)
            part_array.append(uploaded_part)
            sha1.update(chunk)
        content_sha1 = sha1.digest()
        uploaded_file = upload_session.commit(content_sha1=content_sha1, parts=part_array)

        assert uploaded_file.id
        assert uploaded_file.name == large_file_name
        assert uploaded_file.parent == parent_folder
        assert uploaded_file.size == total_size

        util.permanently_delete(uploaded_file)


def test_auto_chunked_upload(parent_folder, large_file, large_file_name):
    total_size = os.stat(large_file.path).st_size
    chunked_uploader = parent_folder.get_chunked_uploader(large_file.path)

    uploaded_file = chunked_uploader.start()

    assert uploaded_file.id
    assert uploaded_file.name == large_file_name
    assert uploaded_file.parent == parent_folder
    assert uploaded_file.size == total_size

    util.permanently_delete(uploaded_file)


def test_get_items(parent_folder, small_file_path):
    with BoxTestFolder(parent_folder=parent_folder) as subfolder,\
            BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file,\
            BoxTestWebLink(parent_folder=parent_folder, url='https://box.com') as web_link:

        assert set(parent_folder.get_items()) == {subfolder, file, web_link}


def test_upload_stream_to_folder(parent_folder, small_file_name, small_file_path):
    with open(small_file_path, 'rb') as stream_to_be_uploaded:
        uploaded_file = parent_folder.upload_stream(file_stream=stream_to_be_uploaded, file_name=small_file_name)

    assert uploaded_file.id
    assert uploaded_file.parent == parent_folder

    util.permanently_delete(uploaded_file)


def test_upload_small_file_to_folder(parent_folder, small_file_name, small_file_path):
    uploaded_file = parent_folder.upload(file_path=small_file_path, file_name=small_file_name)

    assert uploaded_file.id
    assert uploaded_file.parent == parent_folder

    util.permanently_delete(uploaded_file)


def test_create_subfolder(parent_folder):
    created_subfolder = parent_folder.create_subfolder(name=util.random_name())

    assert created_subfolder.id
    assert created_subfolder.parent == parent_folder

    util.permanently_delete(created_subfolder)


def test_get_shared_link(parent_folder, other_user, other_client):
    with BoxTestFolder(parent_folder=parent_folder) as folder:
        folder.collaborate(accessible_by=other_user, role='editor')

        shared_link = other_client.folder(folder.object_id).get_shared_link(allow_preview=True, allow_download=True)

        result_permissions = folder.get().shared_link['permissions']
        assert result_permissions == {'can_preview': True, 'can_download': True, 'can_edit': False}
        assert other_client.get_shared_item(shared_link).id == folder.id


@pytest.mark.parametrize(
    'collaborator', [
        lazy_fixture('user'),
        lazy_fixture('group'),
    ]
)
def test_add_collaborator(parent_folder, collaborator):
    with BoxTestFolder(parent_folder=parent_folder) as folder:
        folder.add_collaborator(collaborator=collaborator, role=CollaborationRole.EDITOR)
        assert list(folder.get_collaborations())[0].accessible_by == collaborator


def test_add_collaborator_using_email(parent_folder, user):
    user_email = user.login
    with BoxTestFolder(parent_folder=parent_folder) as folder:
        folder.add_collaborator(collaborator=user_email, role=CollaborationRole.VIEWER)
        assert list(folder.get_collaborations())[0].accessible_by == user


def test_invite_collaboratur_using_when_nonexistent_user_email_provided(parent_folder, user):
    nonexistent_user_email = 'non-existant-user-email@box.com'
    with BoxTestFolder(parent_folder=parent_folder) as folder:
        folder.add_collaborator(collaborator=nonexistent_user_email, role=CollaborationRole.VIEWER)
        assert list(folder.get_collaborations())[0].invite_email == nonexistent_user_email


def test_create_web_link(parent_folder):
    created_web_link = parent_folder.create_web_link(target_url="https://box.com")

    assert created_web_link.id
    assert created_web_link.parent == parent_folder

    util.permanently_delete(created_web_link)


def test_delete_folder(parent_folder):
    with BoxTestFolder(parent_folder=parent_folder) as folder:
        created_subfolder = folder.create_subfolder(name=util.random_name())
        created_subfolder.create_subfolder(name=util.random_name())

        assert list(folder.get_items())
        created_subfolder.delete(recursive=True)
        assert not list(folder.get_items())

        CLIENT.trash().permanently_delete_item(created_subfolder)


def test_cascade_and_get_metadata_cascade_policies(parent_folder):
    with BoxTestMetadataTemplate(display_name="test_template") as metadata_template,\
            BoxTestFolder(parent_folder=parent_folder) as folder:
        folder.cascade_metadata(metadata_template)

        policy_applied_to_folder = list(folder.get_metadata_cascade_policies())[0]

        assert policy_applied_to_folder.scope == metadata_template.scope
        assert policy_applied_to_folder.templateKey == metadata_template.template_key
        assert policy_applied_to_folder.parent == folder


def test_create_and_get_lock(parent_folder):
    with BoxTestFolder(parent_folder=parent_folder) as folder:
        folder.create_lock()

        lock = list(folder.get_locks())[0]
        assert lock.id
        assert lock.folder == folder

        with pytest.raises(BoxAPIException):
            folder.delete()

        with pytest.raises(BoxAPIException):
            folder.move(parent_folder=CLIENT.root_folder())

        lock.delete()
