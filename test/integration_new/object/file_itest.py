import io
import os
import urllib.request
from datetime import datetime, timedelta
from dateutil import parser
import pytest
import pytz

from boxsdk import BoxAPIException
from test.integration_new.context_managers.box_retention_policy import BoxRetentionPolicy
from test.integration_new import util
from test.integration_new.context_managers.box_test_file import BoxTestFile
from test.integration_new.context_managers.box_test_folder import BoxTestFolder


FILE_TESTS_DIRECTORY_NAME = 'file-integration-tests'


@pytest.fixture(scope="module", autouse=True)
def parent_folder():
    with BoxTestFolder(name=f'{FILE_TESTS_DIRECTORY_NAME} {datetime.now()}') as folder:
        yield folder


@pytest.fixture(scope="module", autouse=True)
def test_file(parent_folder, small_file_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        yield file


def test_preflight_check(test_file):
    file_size = 1213
    accelerator_url = test_file.preflight_check(size=file_size, name=util.random_name())

    assert accelerator_url


def test_create_upload_session_for_file_version(test_file):
    file_size = 26000000
    upload_session = test_file.create_upload_session(file_size=file_size)

    assert upload_session.id
    assert upload_session.type == 'upload_session'


def test_get_chuncked_uploader_for_file_version(test_file, large_file):
    total_size = os.stat(large_file.path).st_size

    chunked_uploader = test_file.get_chunked_uploader(file_path=large_file.path)

    assert chunked_uploader._file_size == total_size
    assert chunked_uploader._upload_session


def test_content(test_file, small_file_path):
    file_content = test_file.content()

    with open(small_file_path, 'rb') as expected_file:
        assert expected_file.read() == file_content


def test_download_to(test_file, small_file_path):
    output_file_name = util.random_name()

    with open(output_file_name, 'wb') as output_file:
        test_file.download_to(writeable_stream=output_file)

    with open(output_file_name, 'rb') as downloaded_file:
        with open(small_file_path, 'rb') as expected_file:
            assert downloaded_file.read() == expected_file.read()

    os.remove(output_file_name)


def test_get_download_url(test_file, small_file_path):
    download_url = test_file.get_download_url()

    with open(small_file_path, 'rb') as expected_file:
        with urllib.request.urlopen(download_url) as downloaded_file:
            assert downloaded_file.read() == expected_file.read()


def test_update_contents_with_stream(parent_folder, small_file_path, small_file_v2_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        with open(small_file_v2_path, 'rb') as file_v2:
            updated_file = file.update_contents_with_stream(file_stream=file_v2)

        with open(small_file_v2_path, 'rb') as file_v2:
            assert updated_file.content() == file_v2.read()


def test_update_contents(parent_folder, small_file_path, small_file_v2_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        updated_file = file.update_contents(small_file_v2_path)

        with open(small_file_v2_path, 'rb') as file_v2:
            assert updated_file.content() == file_v2.read()


def test_lock_and_unlock(parent_folder, small_file_path, small_file_v2_path, other_user, other_client):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        file.collaborate(accessible_by=other_user, role='editor')

        file.lock(prevent_download=True)

        assert file.get(fields=('lock',)).lock

        with pytest.raises(BoxAPIException):
            other_client.file(file.object_id).update_contents(small_file_v2_path)

        with pytest.raises(BoxAPIException):
            other_client.file(file.object_id).download_to(io.BytesIO())

        file.unlock()

        assert file.get(fields=('lock',)).lock is None


def test_get_shared_link(parent_folder, small_file_path, other_user, other_client):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        file.collaborate(accessible_by=other_user, role='editor')

        shared_link = other_client.file(file.object_id).get_shared_link(allow_edit=True, allow_preview=True, allow_download=True)

        result_permissions = file.get().shared_link['permissions']
        assert result_permissions == {'can_preview': True, 'can_download': True, 'can_edit': True}
        assert other_client.get_shared_item(shared_link).id == file.id


def test_get_shared_link_download_url(parent_folder, small_file_path, other_user, other_client):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        file.collaborate(accessible_by=other_user, role='editor')

        shared_link_download_url = other_client.file(file.object_id).get_shared_link_download_url()

        with open(small_file_path, 'rb') as expected_file:
            with urllib.request.urlopen(shared_link_download_url) as downloaded_file:
                assert downloaded_file.read() == expected_file.read()


def test_add_and_get_comments(parent_folder, small_file_path):
    test_comment = 'this is a test comment'
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        file.add_comment(message=test_comment)
        comment = list(file.get_comments())[0]

        assert comment.id
        assert comment.message == test_comment


def test_and_get_task(parent_folder, small_file_path):
    test_task_action = 'review'
    test_task_message = 'this is a test task message'
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        file.create_task(message=test_task_message, action=test_task_action)
        task = list(file.get_tasks())[0]

        assert task.id
        assert task.message == test_task_message
        assert task.action == test_task_action


def test_get_previous_versions(parent_folder, small_file_path, small_file_v2_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as test_file:
        test_file_version = test_file.file_version

        assert not list(test_file.get_previous_versions())

        updated_test_file = test_file.update_contents(small_file_v2_path)
        updated_file_version = updated_test_file.file_version

        previous_version = list(updated_test_file.get_previous_versions())[0]

        assert previous_version != updated_file_version
        assert previous_version == test_file_version
        assert previous_version.type == 'file_version'


def test_promote_version(parent_folder, small_file_path, small_file_v2_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as test_file:
        test_file_version = test_file.file_version

        updated_test_file = test_file.update_contents(small_file_v2_path)
        updated_file_version = updated_test_file.file_version

        assert updated_file_version != test_file_version

        promoted_file_version = updated_test_file.promote_version(file_version=test_file_version)

        assert test_file.get(fields=('file_version',)).file_version == promoted_file_version
        assert set(updated_test_file.get_previous_versions()) == {test_file_version, updated_file_version}

        with open(small_file_path, 'rb') as expected_file_v1:
            assert expected_file_v1.read() == test_file.content()


def test_delete_version(parent_folder, small_file_path, small_file_v2_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as test_file:
        updated_test_file = test_file.update_contents(small_file_v2_path)

        previous_version = list(updated_test_file.get_previous_versions())[0]
        assert previous_version.trashed_at is None

        was_deletion_successs = updated_test_file.delete_version(file_version=previous_version)

        assert was_deletion_successs
        assert list(test_file.get_previous_versions())[0].trashed_at


def test_get_embed_url(parent_folder, image_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=image_path) as test_file:
        embed_url = test_file.get_embed_url()

        assert embed_url


def test_get_representation_info(parent_folder, image_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=image_path) as test_file:
        representation_info = test_file.get_representation_info(rep_hints='[png]')

        assert representation_info


def test_get_thumbnail(parent_folder, image_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=image_path) as test_file:
        thumbnail = test_file.get_thumbnail(extension='jpg', min_width=32, max_width=32, min_height=32, max_height=32)

        assert thumbnail


def test_get_thumbnail_representation(parent_folder, image_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=image_path) as test_file:
        thumbnail_representation = test_file.get_thumbnail_representation(extension='jpg', dimensions='32x32')

        assert thumbnail_representation


def test_copy(test_file, parent_folder):
    copied_file_name = util.random_name()
    copied_file = test_file.copy(parent_folder=parent_folder, name=copied_file_name)

    assert copied_file.id != test_file
    assert copied_file.name == copied_file_name
    assert test_file.content() == copied_file.content()

    util.permanently_delete(copied_file)


def test_set_disposition_at(parent_folder, small_file_path):
    with BoxRetentionPolicy(disposition_action='permanently_delete', retention_length=1) as retention_policy:
        with BoxTestFolder(name=f'{FILE_TESTS_DIRECTORY_NAME} {datetime.now()}') as folder_under_retention:
            retention_policy.assign(folder_under_retention)

            with BoxTestFile(parent_folder=folder_under_retention, file_path=small_file_path) as file_under_retention:
                old_disposition_str = file_under_retention.get(fields=('disposition_at',)).disposition_at
                old_disposition_datetime = parser.parse(old_disposition_str)

                new_disposition_date = datetime.now().replace(microsecond=0).astimezone(pytz.utc) + timedelta(days=2)
                file_under_retention.set_disposition_at(new_disposition_date)

                updated_disposition_str = file_under_retention.get(fields=('disposition_at',)).disposition_at
                updated_disposition_datetime = parser.parse(updated_disposition_str)

                assert updated_disposition_datetime.astimezone(pytz.utc) == new_disposition_date
                assert updated_disposition_datetime.astimezone(pytz.utc) != old_disposition_datetime.astimezone(pytz.utc)
