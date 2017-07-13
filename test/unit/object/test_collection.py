# coding: utf-8

from __future__ import unicode_literals
import json
from mock import Mock
import pytest
from six.moves import zip  # pylint:disable=redefined-builtin,import-error
from boxsdk.network.default_network import DefaultNetworkResponse
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.session.box_session import BoxResponse


# pylint:disable=protected-access
# pylint:disable=redefined-outer-name


@pytest.fixture()
def mock_items(mock_box_session, mock_object_id):
    return [
        {'type': 'file', 'id': mock_object_id},
        {'type': 'folder', 'id': mock_object_id},
        {'type': 'file', 'id': mock_object_id},
    ], [
        File(mock_box_session, mock_object_id),
        Folder(mock_box_session, mock_object_id),
        File(mock_box_session, mock_object_id),
    ]


@pytest.fixture()
def mock_items_response(mock_items):
    # pylint:disable=redefined-outer-name
    def get_response(limit, offset):
        items_json, items = mock_items
        mock_box_response = Mock(BoxResponse)
        mock_network_response = Mock(DefaultNetworkResponse)
        mock_box_response.network_response = mock_network_response
        mock_box_response.json.return_value = mock_json = {'entries': items_json[offset:limit + offset]}
        mock_box_response.content = json.dumps(mock_json).encode()
        mock_box_response.status_code = 200
        mock_box_response.ok = True
        return mock_box_response, items[offset:limit + offset]
    return get_response


@pytest.mark.parametrize('limit,offset,fields', [(1, 0, None), (100, 0, ['foo', 'bar']), (1, 1, None)])
def test_get_items(test_collection, mock_box_session, mock_items_response, limit, offset, fields):
    # pylint:disable=redefined-outer-name
    expected_url = test_collection.get_url('items')
    mock_box_session.get.return_value, expected_items = mock_items_response(limit, offset)
    items = test_collection.get_items(limit, offset, fields)
    expected_params = {'limit': limit, 'offset': offset}
    if fields:
        expected_params['fields'] = ','.join(fields)
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params)
    assert items == expected_items
    assert all([i.id == e.object_id for i, e in zip(items, expected_items)])


def test_add_item(test_collection, test_file, mock_box_session, mock_object_id, mock_file_response):
    expected_url = test_file.get_url()
    mock_box_session.put.return_value = mock_file_response
    new_file = test_collection.add_item(test_file)
    data = json.dumps({'collections': [{'id': test_collection.object_id}]})
    mock_box_session.put.assert_called_once_with(expected_url, data=data, headers=None, params=None)
    assert isinstance(new_file, File)
    assert new_file.object_id == mock_object_id


def test_remove_item(test_collection, test_file, mock_box_session, mock_object_id, mock_file_response):
    expected_url = test_file.get_url()
    mock_box_session.put.return_value = mock_file_response
    new_file = test_collection.remove_item(test_file)
    data = json.dumps({'collections': []})
    mock_box_session.put.assert_called_once_with(expected_url, data=data, headers=None, params=None)
    assert isinstance(new_file, File)
    assert new_file.object_id == mock_object_id
