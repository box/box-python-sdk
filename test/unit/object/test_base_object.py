# coding: utf-8

from itertools import product
import json
import pytest
from boxsdk.config import API
from boxsdk.object.base_object import BaseObject
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.object.user import User


@pytest.fixture(params=('file', 'folder', 'user'))
def test_object_and_response(
        test_file, test_folder, mock_user,
        mock_file_response, mock_folder_response, mock_user_response,
        request):
    test_objects_and_responses = {
        'file': (test_file, mock_file_response),
        'folder': (test_folder, mock_folder_response),
        'user': (mock_user, mock_user_response),
    }
    return test_objects_and_responses[request.param]


@pytest.fixture(params=('same_file', 'same_folder', 'same_user', 'against_none', 'different_ids', 'different_types'))
def objects_for_comparison(test_file, test_folder, mock_user, request, mock_box_session):
    cases = {
        'identical_object': (test_file, test_file, True),
        'same_file': (test_file, File(mock_box_session, test_file.object_id), True),
        'same_folder': (test_folder, Folder(mock_box_session, test_folder.object_id), True),
        'same_user': (mock_user, User(mock_box_session, mock_user.object_id), True),
        'against_none': (test_file, None, False),
        'different_ids': (File(mock_box_session, '1'), File(mock_box_session, '2'), False),
        'different_types': (File(mock_box_session, '1'), Folder(mock_box_session, '1'), False),
        'not_api_object': (test_file, {'id': test_file.object_id, 'type': 'file'}, False),
    }
    return cases[request.param]


@pytest.mark.parametrize('params,headers', product(*([[None, {}, {'foo': 'bar'}, {'foo': 'bar', 'num': 4}]] * 2)))
def test_update_info(test_object_and_response, mock_box_session, params, headers):
    # pylint:disable=redefined-outer-name, protected-access
    test_object, mock_object_response = test_object_and_response
    expected_url = test_object.get_url()
    mock_box_session.put.return_value = mock_object_response
    data = {'foo': 'bar', 'baz': {'foo': 'bar'}, 'num': 4}
    update_response = BaseObject.update_info(test_object, data=data, params=params, headers=headers)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), params=params, headers=headers)
    assert isinstance(update_response, test_object.__class__)
    assert update_response.object_id == test_object.object_id


@pytest.mark.parametrize('params, headers, success', [
    (None, None, True),
    ({'a': 'b'}, {'10': '20'}, True),
    ({'a': 'b'}, None, False),
])
def test_delete_handles_params_and_headers_correctly(mock_box_session, make_mock_box_request, params, headers, success):
    # pylint:disable=redefined-outer-name, protected-access
    fake_id = 'a_fake_id'
    base_object = BaseObject(mock_box_session, fake_id)

    mock_box_response, _ = make_mock_box_request(response_ok=success)
    mock_box_session.delete.return_value = mock_box_response
    expected_url = f'{API.BASE_API_URL}/{None}s/{fake_id}'
    update_response = base_object.delete(params=params, headers=headers)
    mock_box_session.delete.assert_called_once_with(
        expected_url,
        expect_json_response=False,
        params=params or {},
        headers=headers,
    )
    assert update_response is success


def test_getattr_and_getitem(test_object_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_object, mock_object_response = test_object_and_response
    mock_box_session.put.return_value = mock_object_response
    update_response = BaseObject.update_info(test_object, data={})
    assert isinstance(update_response, test_object.__class__)
    assert update_response.object_id == update_response.id == update_response['id']  # pylint:disable=no-member


def test_get_url(test_object_and_response):
    # pylint:disable=redefined-outer-name, protected-access
    test_object, _ = test_object_and_response
    url = test_object.get_url()
    assert test_object.object_id in url
    assert test_object._item_type in url


def test_get_type_url(test_object_and_response):
    # pylint:disable=redefined-outer-name, protected-access
    test_object, _ = test_object_and_response
    url = test_object.get_type_url()
    assert url.endswith(f'{test_object._item_type}s')


def test_eq(objects_for_comparison):
    # pylint:disable=redefined-outer-name
    obj1, obj2, expected_value = objects_for_comparison
    assert (obj1 == obj2) == expected_value


def test_ne(objects_for_comparison):
    # pylint:disable=redefined-outer-name
    obj1, obj2, are_equal = objects_for_comparison
    expected_value = not are_equal
    assert (obj1 != obj2) == expected_value


def test_hash(objects_for_comparison):
    # pylint:disable=redefined-outer-name
    obj1, obj2, are_equal = objects_for_comparison

    # Set a value in the dict such that it will be overridden to True iff the objects hash identically (are equal)
    test_dict = {}
    test_dict[obj1] = False
    test_dict[obj2] = True

    assert test_dict[obj1] == are_equal
