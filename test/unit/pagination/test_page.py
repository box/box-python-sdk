# coding: utf-8

from mock import Mock, PropertyMock
import pytest

from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.pagination.page import Page
from boxsdk.session.session import Session
from boxsdk.util.translator import Translator


@pytest.fixture()
def translator():
    return Translator()


@pytest.fixture()
def mock_session(translator):
    mock_box_session = Mock(Session)
    type(mock_box_session).translator = PropertyMock(
        return_value=translator
    )
    return mock_box_session


@pytest.fixture()
def page_builder(mock_session):
    def factory_function(response):
        return Page(
            session=mock_session,
            response_object=response
        )
    return factory_function


@pytest.fixture()
def item_checker(mock_session):
    def item_checker_function(item_type, response_object, item):
        assert item.id == response_object['id']
        assert isinstance(item, item_type)
        assert item.response_object == response_object
        assert item.session is mock_session

    return item_checker_function


def test_response_property(page_builder):
    response = {1: 10, 2: 20, 3: 30}
    page = page_builder(response)
    assert response == page.response_object


def test_getitem(page_builder, item_checker):
    entry_1 = {
        "type": "folder",
        "id": "192429928",
        "sequence_id": "1",
        "etag": "1",
        "name": "Stephen Curry Three Pointers"
    }
    entry_2 = {
        "type": "file",
        "id": "818853862",
        "sequence_id": "0",
        "etag": "0",
        "name": "Warriors.jpg"
    }
    response_entries = [entry_1, entry_2]
    response = {"entries": response_entries}
    page = page_builder(response)

    item_checker(Folder, entry_1, page[0])
    item_checker(File, entry_2, page[1])
    assert page[1] == page[-1]


def test_getitem_past_length_raises(page_builder):
    length = 7
    response_entries = [object() for _ in range(length)]
    response = {"entries": response_entries}
    page = page_builder(response=response)

    with pytest.raises(IndexError):
        page[length]  # pylint:disable=pointless-statement


@pytest.mark.parametrize('length', (0, 1, 10))
def test_len(page_builder, length):
    response_entries = [object() for _ in range(length)]
    response = {
        "entries": response_entries
    }
    page = page_builder(response=response)
    assert len(page) == length


def test_translation_of_page_entries(page_builder, mock_session, item_checker):
    tested_item_types = ['folder', 'file', 'user', 'collaboration', 'group', 'foobar']
    response_entries = [{'type': item_type_string, 'id': str(i)} for i, item_type_string in enumerate(tested_item_types)]
    response = {"entries": response_entries}
    page = page_builder(response=response)
    for i, item in enumerate(page):
        item_checker(mock_session.translator.get(response_entries[i]['type']), response_entries[i], item)
