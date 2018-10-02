# coding: utf-8

from __future__ import absolute_import, unicode_literals

from itertools import product

import pytest

from boxsdk.object.base_object import BaseObject
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.object.group import Group
from boxsdk.object.user import User
from boxsdk.util.translator import Translator


_response_to_class_mapping = {}


@pytest.fixture
def bookmark_response(make_mock_box_request, mock_object_id):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'bookmark', 'id': mock_object_id},
    )
    return mock_box_response


@pytest.fixture
def box_note_response(make_mock_box_request, mock_object_id):
    # pylint:disable=redefined-outer-name
    mock_box_response, _ = make_mock_box_request(
        response={'type': 'boxnote', 'id': mock_object_id},
    )
    return mock_box_response


@pytest.fixture(autouse=True)
def translator_response(
        bookmark_response,
        box_note_response,
        mock_file_response,
        mock_folder_response,
        mock_group_response,
        mock_user_response,
):
    # pylint:disable=redefined-outer-name
    _response_to_class_mapping['bookmark'] = (bookmark_response, BaseObject)
    _response_to_class_mapping['box_note'] = (box_note_response, BaseObject)
    _response_to_class_mapping['file'] = (mock_file_response, File)
    _response_to_class_mapping['folder'] = (mock_folder_response, Folder)
    _response_to_class_mapping['group'] = (mock_group_response, Group)
    _response_to_class_mapping['user'] = (mock_user_response, User)


@pytest.mark.parametrize('response_type', ['bookmark', 'box_note', 'file', 'folder', 'group', 'user'])
def test_translator_converts_response_to_correct_type(response_type):
    response, object_class = _response_to_class_mapping[response_type]
    assert type(Translator().get(response.json()['type']) == object_class)


def test_default_translator():
    assert isinstance(Translator._default_translator, Translator)   # pylint:disable=protected-access


@pytest.mark.parametrize(('extend_default_translator', 'new_child'), list(product([None, True], [False, True])))
def test_with_extend_default_translator(default_translator, extend_default_translator, new_child):
    item_type = 'foo'

    class Foo(object):
        pass

    kwargs = {}
    if extend_default_translator is not None:
        kwargs['extend_default_translator'] = extend_default_translator
    translator = Translator({item_type: Foo}, new_child=new_child, **kwargs)
    assert set(translator.items()).issuperset(default_translator.items())


@pytest.mark.parametrize('new_child', [False, True])
def test_without_extend_default_translator(new_child):
    item_type = 'foo'

    class Foo(object):
        pass

    mapping = {item_type: Foo}

    translator = Translator(mapping, extend_default_translator=False, new_child=new_child)
    assert translator == mapping


@pytest.mark.parametrize(('new_child', 'extend_default_translator'), list(product([None, True], [False, True])))
def test_with_new_child(new_child, extend_default_translator):
    item_type = 'foo'

    class Foo(object):
        pass

    mapping = {item_type: Foo}

    kwargs = {}
    if new_child is not None:
        kwargs['new_child'] = new_child

    translator = Translator(mapping, extend_default_translator=extend_default_translator, **kwargs)
    assert item_type in translator
    assert translator.maps[0] == {}
    with pytest.raises(KeyError):
        del translator[item_type]

    class Bar(Foo):
        pass

    translator.register(item_type, Bar)
    assert translator.get(item_type) is Bar
    assert mapping == {item_type: Foo}


@pytest.mark.parametrize('extend_default_translator', [False, True])
def test_without_new_child(extend_default_translator):
    item_type = 'foo'

    class Foo(object):
        pass

    mapping = {item_type: Foo}

    translator = Translator(mapping, new_child=False, extend_default_translator=extend_default_translator)
    assert item_type in translator
    assert translator.maps[0] is mapping

    class Bar(Foo):
        pass

    translator.register(item_type, Bar)
    assert translator.get(item_type) is Bar
    assert mapping == {item_type: Bar}

    del translator[item_type]
    assert not mapping


def test_translate(default_translator, mock_box_session):
    response_object = {
        'entries': [
            {
                'type': 'folder',
                'id': '11111',
                'name': 'Test Folder',
                'created_by': {
                    'type': 'user',
                    'id': '33333',
                    'name': 'Test User',
                },
            },
            {
                'type': 'file',
                'id': '22222',
                'name': 'Test File',
                'modified_by': {
                    'type': 'user',
                    'id': '33333',
                    'name': 'Test User',
                },
            },
        ],
    }

    results = default_translator.translate(mock_box_session, response_object=response_object)
    test_folder = results['entries'][0]
    test_file = results['entries'][1]

    assert isinstance(test_folder, Folder)
    assert isinstance(test_file, File)
    assert test_folder.object_id == '11111'
    assert test_folder.name == 'Test Folder'
    assert test_file.object_id == '22222'
    assert test_file.name == 'Test File'

    user_1 = test_folder.created_by
    user_2 = test_file.modified_by
    assert isinstance(user_1, User)
    assert isinstance(user_2, User)
    assert user_1 == user_2

    assert test_folder._session == mock_box_session  # pylint:disable=protected-access
    assert test_file._session == mock_box_session  # pylint:disable=protected-access
    assert user_1._session == mock_box_session  # pylint:disable=protected-access
    assert user_2._session == mock_box_session  # pylint:disable=protected-access
