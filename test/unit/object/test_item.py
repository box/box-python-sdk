# coding: utf-8

from __future__ import unicode_literals

import json
import pytest

from boxsdk.exception import BoxAPIException
from boxsdk.config import API
from boxsdk.object.watermark import Watermark
from boxsdk.object.collaboration import Collaboration
from boxsdk.util.default_arg_value import SDK_VALUE_NOT_SET
from boxsdk.exception import BoxValueError


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


@pytest.mark.parametrize('params, expected_data', [
    ({}, {}),
    ({'name': 'New name.pdf'}, {'name': 'New name.pdf'})
])
def test_copy_item(test_item_and_response, mock_box_session, test_folder, mock_object_id, params, expected_data):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url('copy')
    expected_body = {
        'parent': {'id': mock_object_id},
    }
    expected_body.update(expected_data)
    mock_box_session.post.return_value = mock_item_response
    copy_response = test_item.copy(test_folder, **params)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert isinstance(copy_response, test_item.__class__)


@pytest.mark.parametrize('params, expected_data', [
    ({}, {}),
    ({'name': 'New name.pdf'}, {'name': 'New name.pdf'})
])
def test_move_item(test_item_and_response, mock_box_session, test_folder, mock_object_id, params, expected_data):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, mock_item_response = test_item_and_response
    expected_url = test_item.get_url()
    expected_body = {
        'parent': {'id': mock_object_id},
    }
    expected_body.update(expected_data)
    mock_box_session.put.return_value = mock_item_response
    move_response = test_item.move(test_folder, **params)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_body), params=None, headers=None)
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
    mock_box_session.put.return_value.json.return_value = {
        'type': test_item.object_type,
        'id': test_item.object_id,
        'shared_link': {
            'url': test_url,
        },
    }
    expected_data = {'shared_link': {}}
    if shared_link_access is not None:
        expected_data['shared_link']['access'] = shared_link_access
    if shared_link_unshared_at is not SDK_VALUE_NOT_SET:
        expected_data['shared_link']['unshared_at'] = shared_link_unshared_at
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


def test_clear_unshared_at_for_shared_link(
        test_item_and_response,
        mock_box_session,
        test_url,
):
    test_item, _ = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.put.return_value.json.return_value = {
        'type': test_item.object_type,
        'id': test_item.object_id,
        'shared_link': {
            'url': test_url,
            'unshared_at': None,
        },
    }
    expected_data = {'shared_link': {'unshared_at': None, }, }
    shared_link = test_item.get_shared_link(unshared_at=None)
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(expected_data),
        headers=None,
        params=None,
    )
    assert shared_link is test_url


def test_remove_shared_link(test_item_and_response, mock_box_session, etag, if_match_header):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = test_item.get_url()
    mock_box_session.put.return_value.json.return_value = {
        'type': test_item.object_type,
        'id': test_item.object_id,
        'shared_link': None,
    }
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
        'type': test_item.object_type,
        'id': test_item.object_id,
        'collections': current_collections,
    }
    mock_box_session.get.return_value.json.return_value = mock_response
    mock_box_session.put.return_value = mock_item_response

    test_item.add_to_collection(mock_collection)

    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=expected_params)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=None, params=None)


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
        'type': test_item.object_type,
        'id': test_item.object_id,
        'collections': current_collections,
    }
    mock_box_session.get.return_value.json.return_value = mock_response
    mock_box_session.put.return_value = mock_item_response

    test_item.remove_from_collection(mock_collection)

    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=expected_params)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_data), headers=None, params=None)


def test_get_watermark(test_item_and_response, mock_box_session):
    test_item, _ = test_item_and_response
    created_at = '2016-10-31T15:33:33-07:00'
    modified_at = '2016-10-31T15:33:33-07:00'
    expected_url = '{0}/{1}s/{2}/watermark'.format(API.BASE_API_URL, test_item.object_type, test_item.object_id)
    mock_box_session.get.return_value.json.return_value = {
        'watermark': {
            'created_at': created_at,
            'modified_at': modified_at,
        },
    }
    watermark = test_item.get_watermark()
    mock_box_session.get.assert_called_once_with(expected_url)
    assert isinstance(watermark, Watermark)
    assert watermark['created_at'] == created_at
    assert watermark['modified_at'] == modified_at


def test_apply_watermark(test_item_and_response, mock_box_session):
    test_item, _ = test_item_and_response
    created_at = '2016-10-31T15:33:33-07:00'
    modified_at = '2016-10-31T15:33:33-07:00'
    expected_url = '{0}/{1}s/{2}/watermark'.format(API.BASE_API_URL, test_item.object_type, test_item.object_id)
    mock_box_session.put.return_value.json.return_value = {
        'watermark': {
            'created_at': created_at,
            'modified_at': modified_at,
        },
    }
    watermark = test_item.apply_watermark()
    mock_box_session.put.assert_called_once_with(expected_url, data='{"watermark": {"imprint": "default"}}')
    assert isinstance(watermark, Watermark)
    assert watermark['created_at'] == created_at
    assert watermark['modified_at'] == modified_at


def test_delete_watermark(test_item_and_response, mock_box_session):
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/watermark'.format(API.BASE_API_URL, test_item.object_type, test_item.object_id)
    mock_box_session.delete.return_value.ok = True
    is_watermark_deleted = test_item.delete_watermark()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False)
    assert is_watermark_deleted is True


def test_collaborate_with_group(test_item_and_response, test_group, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = '{0}/collaborations'.format(API.BASE_API_URL)
    expected_data = {
        'item': {
            'type': test_item.object_type,
            'id': test_item.object_id,
        },
        'accessible_by': {
            'type': test_group.object_type,
            'id': test_group.object_id,
        },
        'role': 'editor',
    }
    mock_collaboration = {
        'type': 'collaboration',
        'id': '1234',
        'created_by': {
            'type': 'user',
            'id': '1111',
        }
    }
    mock_box_session.post.return_value.json.return_value = mock_collaboration
    collaboration = test_item.collaborate(test_group, 'editor')
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data), params={})
    assert collaboration.id == mock_collaboration['id']
    assert collaboration['type'] == mock_collaboration['type']
    assert collaboration['created_by']['id'] == mock_collaboration['created_by']['id']


@pytest.mark.parametrize('can_view_path,fields,notify,data,params', [
    (None, None, None, {}, {}),
    (True, None, None, {'can_view_path': True}, {}),
    (False, None, None, {'can_view_path': False}, {}),
    (None, ['type', 'id', 'created_by'], None, {}, {'fields': 'type,id,created_by'}),
    (None, None, True, {}, {'notify': True}),
    (None, None, False, {}, {'notify': False}),
    (True, ['type', 'id', 'created_by'], False, {'can_view_path': True}, {'fields': 'type,id,created_by', 'notify': False})
])
def test_collaborate_with_user(test_item_and_response, mock_user, mock_box_session, can_view_path, fields, notify, data, params):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = '{0}/collaborations'.format(API.BASE_API_URL)
    expected_data = {
        'item': {
            'type': test_item.object_type,
            'id': test_item.object_id,
        },
        'accessible_by': {
            'type': mock_user.object_type,
            'id': mock_user.object_id,
        },
        'role': 'editor',
    }
    expected_data.update(data)
    mock_collaboration = {
        'type': 'collaboration',
        'id': '1234',
        'created_by': {
            'type': 'user',
            'id': '1111',
        }
    }
    expected_params = params
    mock_box_session.post.return_value.json.return_value = mock_collaboration
    collaboration = test_item.collaborate(mock_user, 'editor', can_view_path=can_view_path, fields=fields, notify=notify)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data), params=expected_params)
    assert collaboration.id == mock_collaboration['id']
    assert collaboration['type'] == mock_collaboration['type']
    assert collaboration['created_by']['id'] == mock_collaboration['created_by']['id']


@pytest.mark.parametrize('can_view_path,fields,notify,data,params', [
    (None, None, None, {}, {}),
    (True, None, None, {'can_view_path': True}, {}),
    (False, None, None, {'can_view_path': False}, {}),
    (None, ['type', 'id', 'created_by'], None, {}, {'fields': 'type,id,created_by'}),
    (None, None, True, {}, {'notify': True}),
    (None, None, False, {}, {'notify': False}),
    (True, ['type', 'id', 'created_by'], False, {'can_view_path': True}, {'fields': 'type,id,created_by', 'notify': False})
])
def test_collaborate_with_login(test_item_and_response, mock_box_session, can_view_path, fields, notify, data, params):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = '{0}/collaborations'.format(API.BASE_API_URL)
    expected_data = {
        'item': {
            'type': test_item.object_type,
            'id': test_item.object_id,
        },
        'accessible_by': {
            'type': 'user',
            'login': 'test@example.com',
        },
        'role': 'editor',
    }
    expected_data.update(data)
    mock_collaboration = {
        'type': 'collaboration',
        'id': '1234',
        'created_by': {
            'type': 'user',
            'id': '1111',
        }
    }
    expected_params = params
    mock_box_session.post.return_value.json.return_value = mock_collaboration
    collaboration = test_item.collaborate_with_login('test@example.com', 'editor', can_view_path=can_view_path, fields=fields, notify=notify)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data), params=expected_params)
    assert collaboration.id == mock_collaboration['id']
    assert collaboration['type'] == mock_collaboration['type']
    assert collaboration['created_by']['id'] == mock_collaboration['created_by']['id']


def test_collaborations(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/collaborations'.format(API.BASE_API_URL, test_item.object_type, test_item.object_id)
    mock_collaboration = {
        'type': 'collaboration',
        'id': '12345',
        'created_by': {
            'type': 'user',
            'id': '33333',
        },
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 500,
        'entries': [mock_collaboration]
    }
    collaborations = test_item.get_collaborations(limit=500)
    collaboration = collaborations.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={'limit': 500})
    assert isinstance(collaboration, Collaboration)
    assert collaboration.id == mock_collaboration['id']
    assert collaboration.type == mock_collaboration['type']
    assert collaboration['created_by']['type'] == 'user'
    assert collaboration['created_by']['id'] == '33333'


def test_get_all_metadata(test_item_and_response, mock_box_session):
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/metadata'.format(API.BASE_API_URL, test_item.object_type, test_item.object_id)
    mock_metadata = {
        'currentDocumentStage': 'prioritization',
        'needsApprovalFrom': 'planning team',
        '$type': 'documentFlow-452b4c9d-c3ad-4ac7-b1ad-9d5192f2fc5f',
        '$parent': 'folder_998951261',
        '$id': 'e57f90ff-0044-48c2-807d-06b908765baf',
        '$version': 1,
        '$typeVersion': 2,
        'maximumDaysAllowedInCurrentStage': 5,
        '$template': 'documentFlow',
        '$scope': 'enterprise_12345',
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_metadata]
    }

    all_metadata = test_item.get_all_metadata()
    metadata = all_metadata.next()

    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(metadata, dict)
    for key in metadata:
        assert mock_metadata[key] == mock_metadata[key]


def test_add_classification(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/metadata/enterprise/securityClassification-6VMVochwUWo'.format(
        API.BASE_API_URL,
        test_item.object_type,
        test_item.object_id,
    )
    metadata_response = {
        'Box__Security__Classification__Key': 'Public',
    }
    metadata_response = mock_box_session.post.return_value.json.return_value = metadata_response
    data = {
        'Box__Security__Classification__Key': 'Public'
    }
    headers = {
        b'Content-Type': b'application/json'
    }
    metadata = test_item.add_classification('Public')
    mock_box_session.post.assert_called_once_with(expected_url, headers=headers, data=json.dumps(data))
    assert metadata is metadata_response['Box__Security__Classification__Key']


def test_update_classification(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/metadata/enterprise/securityClassification-6VMVochwUWo'.format(
        API.BASE_API_URL,
        test_item.object_type,
        test_item.object_id,
    )
    metadata_response = {
        'Box__Security__Classification__Key': 'Internal',
    }
    metadata_response = mock_box_session.put.return_value.json.return_value = metadata_response
    data = [{
        'op': 'add',
        'path': '/Box__Security__Classification__Key',
        'value': 'Internal',
    }]
    headers = {
        b'Content-Type': b'application/json-patch+json'
    }
    metadata = test_item.update_classification('Internal')
    mock_box_session.put.assert_called_once_with(expected_url, headers=headers, data=json.dumps(data))
    assert metadata is metadata_response['Box__Security__Classification__Key']


def test_set_classification_succeeds(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    metadata_response = {
        'Box__Security__Classification__Key': 'Public',
    }
    expected_url = '{0}/{1}s/{2}/metadata/enterprise/securityClassification-6VMVochwUWo'.format(
        API.BASE_API_URL,
        test_item.object_type,
        test_item.object_id,
    )
    post_data = {
        'Box__Security__Classification__Key': 'Public',
    }
    put_data = [{
        'op': 'add',
        'path': '/Box__Security__Classification__Key',
        'value': 'Public',
    }]
    post_headers = {
        b'Content-Type': b'application/json'
    }
    put_headers = {
        b'Content-Type': b'application/json-patch+json'
    }
    mock_box_session.post.side_effect = [BoxAPIException(status=409)]
    mock_box_session.put.return_value.json.return_value = metadata_response
    metadata = test_item.set_classification('Public')
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(post_data), headers=post_headers)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(put_data), headers=put_headers)
    assert metadata is metadata_response['Box__Security__Classification__Key']


def test_set_classification_fails(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/metadata/enterprise/securityClassification-6VMVochwUWo'.format(
        API.BASE_API_URL,
        test_item.object_type,
        test_item.object_id,
    )
    post_data = {
        'Box__Security__Classification__Key': 'Public',
    }
    post_headers = {
        b'Content-Type': b'application/json'
    }
    mock_box_session.post.side_effect = [BoxAPIException(status=500)]
    with pytest.raises(BoxAPIException):
        test_item.set_classification('Public')
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(post_data), headers=post_headers)


def test_get_classification_succeeds(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/metadata/enterprise/securityClassification-6VMVochwUWo'.format(
        API.BASE_API_URL,
        test_item.object_type,
        test_item.object_id,
    )
    metadata_response = {
        'Box__Security__Classification__Key': 'Public'
    }
    mock_box_session.get.return_value.json.return_value = metadata_response
    metadata = test_item.get_classification()
    assert metadata is metadata_response['Box__Security__Classification__Key']
    mock_box_session.get.assert_called_once_with(expected_url)


def test_get_classification_not_found(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/metadata/enterprise/securityClassification-6VMVochwUWo'.format(
        API.BASE_API_URL,
        test_item.object_type,
        test_item.object_id,
    )
    mock_box_session.get.side_effect = [BoxAPIException(status=404, code="instance_not_found")]
    metadata = test_item.get_classification()
    assert metadata is None
    mock_box_session.get.assert_called_once_with(expected_url)


def test_get_classification_raises_exception(test_item_and_response, mock_box_session):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/metadata/enterprise/securityClassification-6VMVochwUWo'.format(
        API.BASE_API_URL,
        test_item.object_type,
        test_item.object_id,
    )
    mock_box_session.get.side_effect = [BoxAPIException(status=500)]
    with pytest.raises(BoxAPIException):
        test_item.get_classification()
    mock_box_session.get.assert_called_once_with(expected_url)


def test_remove_classification(test_item_and_response, mock_box_session, make_mock_box_request):
    # pylint:disable=redefined-outer-name
    test_item, _ = test_item_and_response
    expected_url = '{0}/{1}s/{2}/metadata/enterprise/securityClassification-6VMVochwUWo'.format(
        API.BASE_API_URL,
        test_item.object_type,
        test_item.object_id,
    )
    mock_box_session.delete.return_value, _ = make_mock_box_request(response_ok='success')
    is_removed = test_item.remove_classification()
    mock_box_session.delete.assert_called_once_with(expected_url)
    assert is_removed is 'success'


def test_sanitize_item_id(test_item_and_response):
    # pylint:disable=redefined-outer-name, protected-access
    test_item, _ = test_item_and_response
    assert test_item.validate_item_id(test_item._object_id) is None
    test_item._object_id = "foo"
    with pytest.raises(BoxValueError):
        test_item.validate_item_id(test_item._object_id)
