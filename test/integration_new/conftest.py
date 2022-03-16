import pytest


@pytest.fixture()
def small_file_name():
    return 'small.pdf'


@pytest.fixture()
def large_file_name():
    return 'large.pdf'

