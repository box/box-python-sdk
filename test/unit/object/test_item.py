# coding: utf-8

from __future__ import unicode_literals
import json
import pytest


@pytest.fixture(params=('file', 'folder'))
def test_item_and_response(test_file, test_folder, mock_file_response, mock_folder_response, request):
    if request.param == 'file':
        return test_file, mock_file_response
    return test_folder, mock_folder_response


@pytest.fixture(params=('empty', 'same', 'other'))
def test_collections_for_addition(mock_collection_id, request):
    """Fixture returning a tuple of the expected collections values before and after addition"""
    other_collection_id = mock_collection_id + '2'
    if request.param == 'empty':
        return [], [{'id': mock_collection_id}]
    elif request.param == 'same':
        # Adding a second instance of the same collection is handled correctly by the API,
        # so for simplicity we do not check for an existing copy of the collection and just append
        return [{'id': mock_collection_id}], [{'id': mock_collection_id}, {'id': mock_collection_id}]
    elif request.param == 'other':
        return [{'id': other_collection_id}], [{'id': other_collection_id}, {'id': mock_collection_id}]

    raise NotImplementedError("Forgot to implement {}".format(request.param))


@pytest.fixture(params=('empty', 'only_removed', 'only_other', 'other_and_removed'))
def test_collections_for_removal(mock_collection_id, request):
    """Fixture returning a tuple of the expected collections values before and after removal"""
    other_collection_id = mock_collection_id + '2'
    if request.param == 'empty':
        return [], []
    elif request.param == 'only_removed':
        return [{'id': mock_collection_id}], []
    elif request.param == 'only_other':
        return [{'id': other_collection_id}], [{'id': other_collection_id}]
    elif request.param == 'other_and_removed':
        return [{'id': mock_collection_id}, {'id': other_collection_id}], [{'id': other_collection_id}]

    raise NotImplementedError("Forgot to implement {}".format(request.param))


def test_update_info(test_item_and_response, mock_box_session, etag, if_match_header):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.put.return_value = mock_item_response
    data = {'foo': 'bar', 'baz': {'foo': 'bar'}, 'num': 4}
    update_response = test_item.update_info(data, etag=etag)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=if_match_header, params=None)
    assert isinstance(update_response, test_item.__class__)
    assert update_response.object_id == test_item.object_id


def test_update_info_with_default_request_kwargs(test_item_and_response, mock_box_session, mock_box_session_2):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.with_default_network_request_kwargs.return_value = mock_box_session_2
    mock_box_session_2.put.return_value = mock_item_response
    data = {'foo': 'bar', 'baz': {'foo': 'bar'}, 'num': 4}
    extra_network_parameters = {'timeout': 1}
    update_response = test_item.update_info(data, extra_network_parameters=extra_network_parameters)
    mock_box_session.with_default_network_request_kwargs.assert_called_once_with({'timeout': 1})
    mock_box_session_2.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert isinstance(update_response, test_item.__class__)
    assert update_response.object_id == test_item.object_id


def test_rename_item(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.put.return_value = mock_item_response
    rename_response = test_item.rename('new name')
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps({'name': 'new name'}), params=None, headers=None)
    assert isinstance(rename_response, test_item.__class__)


def test_copy_item(test_item_and_response, mock_box_session, test_folder, mock_object_id):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url('copy')
    mock_box_session.post.return_value = mock_item_response
    copy_response = test_item.copy(test_folder)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps({'parent': {'id': mock_object_id}}))
    assert isinstance(copy_response, test_item.__class__)


def test_move_item(test_item_and_response, mock_box_session, test_folder, mock_object_id):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.put.return_value = mock_item_response
    move_response = test_item.move(test_folder)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps({'parent': {'id': mock_object_id}}), params=None, headers=None)
    assert isinstance(move_response, test_item.__class__)


def test_get_shared_link(
        test_item_and_response,
        mock_box_session,
        shared_link_access,
        shared_link_unshared_at,
        shared_link_password,
        shared_link_can_download,
        shared_link_can_preview,
        test_url,
        etag,
        if_match_header,
):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.put.return_value.json.return_value = {'shared_link': {'url': test_url}}
    expected_data = {'shared_link': {}}
    if shared_link_access is not None:
        expected_data['shared_link']['access'] = shared_link_access
    if shared_link_unshared_at is not None:
        expected_data['shared_link']['unshared_at'] = shared_link_unshared_at.isoformat()
    if shared_link_can_download is not None or shared_link_can_preview is not None:
        expected_data['shared_link']['permissions'] = permissions = {}
        if shared_link_can_download is not None:
            permissions['can_download'] = shared_link_can_download
        if shared_link_can_preview is not None:
            permissions['can_preview'] = shared_link_can_preview
    if shared_link_password is not None:
        expected_data['shared_link']['password'] = shared_link_password
    url = test_item.get_shared_link(
        etag=etag,
        access=shared_link_access,
        unshared_at=shared_link_unshared_at,
        password=shared_link_password,
        allow_download=shared_link_can_download,
        allow_preview=shared_link_can_preview,
    )
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(expected_data),
        headers=if_match_header,
        params=None,
    )
    assert url == test_url


def test_remove_shared_link(test_item_and_response, mock_box_session, etag, if_match_header):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.put.return_value.json.return_value = {'shared_link': None}
    removed = test_item.remove_shared_link(etag=etag)
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps({'shared_link': None}),
        headers=if_match_header,
        params=None,
    )
    assert removed is True


@pytest.mark.parametrize('fields', (None, ['name', 'created_at']))
def test_get(test_item_and_response, mock_box_session, fields, mock_object_id, etag, if_none_match_header):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.get.return_value = mock_item_response
    expected_params = {'fields': ','.join(fields)} if fields else None
    info = test_item.get(fields, etag=etag)
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params, headers=if_none_match_header)
    assert isinstance(info, test_item.__class__)
    assert info.id == mock_object_id


def test_add_to_collection(test_item_and_response, mock_box_session, mock_collection, test_collections_for_addition):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    current_collections, expected_collections = test_collections_for_addition
    expected_url = test_item.get_url()
    expected_params = {'fields': 'collections'}
    expected_data = {
        'collections': expected_collections
    }
    mock_response = {
        'collections': current_collections
    }
    mock_box_session.get.return_value.json.return_value = mock_response
    mock_box_session.put.return_value = mock_item_response

    test_item.add_to_collection(mock_collection)

    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=expected_params)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=None, params=None)


def test_get_from_trash(test_item_and_response, mock_box_session, mock_object_id):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url('trash')
    mock_box_session.get.return_value = mock_item_response
    info = test_item.get_from_trash()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(info, test_item.__class__)
    assert info.id == mock_object_id


def test_restore_from_trash(test_item_and_response, mock_box_session, mock_object_id):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.post.return_value = mock_item_response
    info = test_item.restore_from_trash()
    mock_box_session.post.assert_called_once_with(expected_url, data='{}', params={})
    assert isinstance(info, test_item.__class__)
    assert info.id == mock_object_id


def test_permanently_delete(test_item_and_response, mock_box_session, mock_object_id):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url('trash')
    mock_box_session.delete.return_value = mock_item_response
    info = test_item.permanently_delete()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False)
    assert info is True


def test_remove_from_collection(test_item_and_response, mock_box_session, mock_collection, test_collections_for_removal):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    current_collections, expected_collections = test_collections_for_removal
    expected_url = test_item.get_url()
    expected_params = {'fields': 'collections'}
    expected_data = {
        'collections': expected_collections
    }
    mock_response = {
        'collections': current_collections
    }
    mock_box_session.get.return_value.json.return_value = mock_response
    mock_box_session.put.return_value = mock_item_response

    test_item.remove_from_collection(mock_collection)

    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=expected_params)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=None, params=None)
