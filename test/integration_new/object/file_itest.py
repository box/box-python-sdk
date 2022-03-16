import os
import urllib.request

import pytest

from test.integration_new import util
from test.integration_new.context_managers.box_test_file import BoxTestFile
from test.integration_new.context_managers.box_test_folder import BoxTestFolder


FILE_TESTS_DIRECTORY_NAME = 'file-integration-tests'


@pytest.fixture(scope="module", autouse=True)
def parent_folder():
    with BoxTestFolder(name=FILE_TESTS_DIRECTORY_NAME) as folder:
        yield folder


@pytest.fixture(scope="module", autouse=True)
def test_file(parent_folder, small_file_path):
    with BoxTestFile(parent_folder=parent_folder, file_path=small_file_path) as file:
        yield file


def test_preflight_check(test_file):
    file_size = 1213
    accelerator_url = test_file.preflight_check(size=file_size, name=util.random_name())

    assert accelerator_url is not None


def test_create_upload_session_for_file_version(test_file):
    file_size = 26000000
    upload_session = test_file.create_upload_session(file_size=file_size)

    assert upload_session.id is not None
    assert upload_session.type == 'upload_session'


def test_get_chuncked_uploader_for_file_version(test_file, large_file_path):
    total_size = os.stat(large_file_path).st_size

    chunked_uploader = test_file.get_chunked_uploader(file_path=large_file_path)

    assert chunked_uploader._file_size == total_size
    assert chunked_uploader._upload_session is not None


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
