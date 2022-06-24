from test.integration_new.context_managers.box_test_user import BoxTestUser
from test.integration_new.context_managers.local_large_file import LocalLargeFile
from test.integration_new import util, CLIENT
import pytest


@pytest.fixture(scope='package')
def small_file_name():
    return 'small.pdf'


@pytest.fixture(scope='package')
def small_file_path(small_file_name):
    return util.get_file_path(small_file_name)


@pytest.fixture(scope='package')
def small_file_v2_name():
    return 'small_v2.pdf'


@pytest.fixture(scope='package')
def small_file_v2_path(small_file_v2_name):
    return util.get_file_path(small_file_v2_name)


@pytest.fixture(scope='package')
def image_name():
    return 'image.png'


@pytest.fixture(scope='package')
def image_path(image_name):
    return util.get_file_path(image_name)


@pytest.fixture(scope='session')
def large_file_name():
    return f'{util.random_name()}.pdf'


@pytest.fixture(scope="session")
def large_file(large_file_name):
    with LocalLargeFile(name=large_file_name) as large_file:
        yield large_file


@pytest.fixture(scope="module")
def user():
    with BoxTestUser(login=f'{util.random_name()}@box.com') as user:
        yield user


@pytest.fixture(scope="package")
def other_user():
    with BoxTestUser(login=None) as other_user:
        yield other_user


@pytest.fixture(scope="package")
def other_client(other_user):
    yield CLIENT.as_user(other_user)
