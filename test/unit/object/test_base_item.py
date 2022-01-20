# coding: utf-8

import json
import pytest


@pytest.fixture(params=('file', 'folder', 'web_link'))
def test_base_item_and_response(
        test_file, test_folder, test_web_link, mock_file_response, mock_folder_response, mock_web_link_response, request):
    if request.param == 'file':
        return test_file, mock_file_response
    if request.param == 'folder':
        return test_folder, mock_folder_response

    return test_web_link, mock_web_link_response


@pytest.fixture(params=('empty', 'same', 'other'))
def test_collections_for_addition(mock_collection_id, request):
    """Fixture returning a tuple of the expected collections values before and after addition"""
    other_collection_id = mock_collection_id + '2'
    if request.param == 'empty':
        return [], [{'id': mock_collection_id}]
    if request.param == 'same':
        # Adding a second instance of the same collection is handled correctly by the API,
        # so for simplicity we do not check for an existing copy of the collection and just append
        return [{'id': mock_collection_id}], [{'id': mock_collection_id}, {'id': mock_collection_id}]
    if request.param == 'other':
        return [{'id': other_collection_id}], [{'id': other_collection_id}, {'id': mock_collection_id}]

    raise NotImplementedError(f"Forgot to implement {request.param}")


@pytest.fixture(params=('empty', 'only_removed', 'only_other', 'other_and_removed'))
def test_collections_for_removal(mock_collection_id, request):
    """Fixture returning a tuple of the expected collections values before and after removal"""
    other_collection_id = mock_collection_id + '2'
    if request.param == 'empty':
        return [], []
    if request.param == 'only_removed':
        return [{'id': mock_collection_id}], []
    if request.param == 'only_other':
        return [{'id': other_collection_id}], [{'id': other_collection_id}]
    if request.param == 'other_and_removed':
        return [{'id': mock_collection_id}, {'id': other_collection_id}], [{'id': other_collection_id}]

    raise NotImplementedError(f"Forgot to implement {request.param}")


@pytest.mark.parametrize('params, expected_data', [
    ({}, {}),
    ({'name': 'New name.pdf'}, {'name': 'New name.pdf'})
])
def test_copy_base_item(test_base_item_and_response, mock_box_session, test_folder, mock_object_id, params, expected_data):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_base_item_and_response
    expected_url = test_item.get_url('copy')
    expected_body = {
        'parent': {'id': mock_object_id},
    }
    expected_body.update(expected_data)
    mock_box_session.post.return_value = mock_item_response
    copy_response = test_item.copy(parent_folder=test_folder, **params)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert isinstance(copy_response, test_item.__class__)


@pytest.mark.parametrize(
    'params, expected_data', [
        ({}, {}),
        ({'name': 'New name.pdf'}, {'name': 'New name.pdf'})
    ]
)
def test_move_base_item(test_base_item_and_response, mock_box_session, test_folder, mock_object_id, params, expected_data):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_base_item_and_response
    expected_url = test_item.get_url()
    expected_body = {
        'parent': {'id': mock_object_id},
    }
    expected_body.update(expected_data)
    mock_box_session.put.return_value = mock_item_response
    move_response = test_item.move(test_folder, **params)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_body), params=None, headers=None)
    assert isinstance(move_response, test_item.__class__)


def test_rename_base_item(test_base_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_base_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.put.return_value = mock_item_response
    rename_response = test_item.rename('new name')
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps({'name': 'new name'}), params=None, headers=None)
    assert isinstance(rename_response, test_item.__class__)


def test_add_to_collection(test_base_item_and_response, mock_box_session, mock_collection, test_collections_for_addition):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_base_item_and_response
    current_collections, expected_collections = test_collections_for_addition
    expected_url = test_item.get_url()
    expected_params = {'fields': 'collections'}
    expected_data = {
        'collections': expected_collections
    }
    mock_response = {
        'type': test_item.object_type,
        'id': test_item.object_id,
        'collections': current_collections,
    }
    mock_box_session.get.return_value.json.return_value = mock_response
    mock_box_session.put.return_value = mock_item_response

    test_item.add_to_collection(mock_collection)

    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=expected_params)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=None, params=None)


def test_remove_from_collection(test_base_item_and_response, mock_box_session, mock_collection, test_collections_for_removal):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_base_item_and_response
    current_collections, expected_collections = test_collections_for_removal
    expected_url = test_item.get_url()
    expected_params = {'fields': 'collections'}
    expected_data = {
        'collections': expected_collections
    }
    mock_response = {
        'type': test_item.object_type,
        'id': test_item.object_id,
        'collections': current_collections,
    }
    mock_box_session.get.return_value.json.return_value = mock_response
    mock_box_session.put.return_value = mock_item_response

    test_item.remove_from_collection(mock_collection)

    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=expected_params)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=None, params=None)
