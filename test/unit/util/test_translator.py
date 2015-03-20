# coding: utf-8

from __future__ import unicode_literals
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
    assert type(Translator().translate(response.json()['type']) == object_class)
