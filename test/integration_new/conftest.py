import pytest

from test.integration_new import util


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
def large_file_name():
    return 'large.pdf'


@pytest.fixture(scope='package')
def large_file_path(large_file_name):
    return util.get_file_path(large_file_name)

