import pytest

from test.integration_new.context_managers.box_test_folder import BoxTestFolder


FILE_TESTS_DIRECTORY_NAME = 'file-integration-tests'


@pytest.fixture(scope="module", autouse=True)
def parent_folder():
    with BoxTestFolder(name=FILE_TESTS_DIRECTORY_NAME) as folder:
        yield folder
