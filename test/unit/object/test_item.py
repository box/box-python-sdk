# coding: utf-8

from __future__ import unicode_literals
import json
import pytest

from boxsdk.object.collaboration import Collaboration

@pytest.fixture(params=('file', 'folder'))
def test_item_and_response(test_file, test_folder, mock_file_response, mock_folder_response, request):
    if request.param == 'file':
        return test_file, mock_file_response
    elif request.param == 'folder':
        return test_folder, mock_folder_response


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


def test_collaborate(test_item_and_response, test_group, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = test_item.get_url('collaborations')
    expected_data = {
        'item': {
            'type': test_item.object_type,
            'id': test_item.object_id
        },
        'accessible_by': {
            'type': test_group.object_type,
            'id': test_group.object_id
        },
        'role': 'editor'
    }
    mock_collaboration = {
        'type': 'collaboration',
        'id': '1234',
        'created_by': {
            'type': 'user',
            'id': '1111'
        }
    }
    mock_box_session.post.return_value.json.return_value = mock_collaboration
    collaboration = test_item.collaborate('editor', test_group)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert collaboration.id == mock_collaboration['id']
    assert collaboration['type'] == mock_collaboration['type']

def test_collaborate_with_login(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = mock_box_session.get_url('collaborations')
    expected_data = {
        'item': {
            'type': test_item.object_type,
            'id': test_item.object_id
        },
        'accessible_by': {
            'type': 'user',
            'login': 'test@example.com'
        },
        'role': 'editor'
    }
    mock_collaboration = {
        'type': 'collaboration',
        'id': '1234',
        'created_by': {
            'type': 'user',
            'id': '1111'
        }
    }
    mock_box_session.post.return_value.json.return_value = mock_collaboration
    collaboration = test_item.collaborate_with_login('editor', 'test@example.com')
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data), params={})
    assert collaboration.id == mock_collaboration['id']
    assert collaboration['type'] == mock_collaboration['type']


def test_collaborations(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = test_item.get_url('collaborations')
    mock_collaboration = {
        'type': 'collaboration',
        'id': '12345',
        'created_by': {
            'type': 'user',
            'id': '33333'
        }
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 500,
        'entries': [mock_collaboration]
    }

    collaborations = test_item.collaborations()
    collaboration = collaborations.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'limit': 500})
    assert isinstance(collaboration, Collaboration)
    assert collaboration.id == mock_collaboration['id']
    assert collaboration.type == mock_collaboration['type']


def test_pending_collaborations(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = mock_box_session.get_url('collaborations')
    mock_collaboration = {
        'type': 'collaboration',
        'id': '12345',
        'created_by': {
            'type': 'user',
            'id': '33333'
        }
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 500,
        'entries': [mock_collaboration],
        'total_count': 1,
        'offset': 0
    }

    collaborations = test_item.pending_collaborations('pending')
    collaboration = collaborations.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'status': 'pending', 'offset': None})
    assert isinstance(collaboration, Collaboration)
    assert collaboration.id == mock_collaboration['id']
    assert collaboration.type == mock_collaboration['type']


 