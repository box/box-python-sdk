# coding: utf-8

import json
import pytest
from boxsdk.object.metadata import MetadataUpdate
from boxsdk.exception import BoxAPIException


@pytest.fixture
def metadata_response():
    return {
        '$id': 'c79896a0-a33f-11e3-a5e2-0800200c9a66',
        '$type': 'properties',
        '$parent': 'file_552345101',
        'client_number': '820183',
        'client_name': 'Biomedical Corp',
        'case_reference': 'A83JAA',
        'case_type': 'Employment Litigation',
        'assigned_attorney': 'Francis Burke',
        'case_status': 'in-progress',
    }


@pytest.fixture(params=['enterprise', 'global'])
def metadata_scope(request):
    return request.param


@pytest.fixture(params=['properties', 'custom'])
def metadata_template(request):
    return request.param


@pytest.fixture(params=['file', 'folder'])
def test_object(test_file, test_folder, request):
    if request.param == 'file':
        return test_file
    return test_folder


@pytest.mark.parametrize('success', [True, False])
def test_delete(mock_box_session, make_mock_box_request, test_object, metadata_scope, metadata_template, success):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value, _ = make_mock_box_request(response_ok=success)
    metadata = test_object.metadata(metadata_scope, metadata_template)
    assert metadata.delete() is success
    mock_box_session.delete.assert_called_once_with(metadata.get_url())


def test_create(
        mock_box_session,
        make_mock_box_request,
        test_object,
        metadata_scope,
        metadata_template,
        metadata_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.post.return_value, _ = make_mock_box_request(response=metadata_response)
    metadata = test_object.metadata(metadata_scope, metadata_template)
    response = metadata.create(metadata_response)
    assert response is metadata_response
    mock_box_session.post.assert_called_once_with(
        metadata.get_url(),
        data=json.dumps(metadata_response),
        headers={b'Content-Type': b'application/json'},
    )


def test_set(
        mock_box_session,
        test_object,
        metadata_scope,
        metadata_template,
        metadata_response,
):
    post_data = {
        'case_status': 'in-progress',
    }
    post_value = json.dumps(post_data)
    put_value = json.dumps([{
        'op': 'add',
        'path': '/case_status',
        'value': 'in-progress',
    }])
    mock_box_session.post.side_effect = [BoxAPIException(status=409, message="Conflict")]
    mock_box_session.put.return_value.json.return_value = metadata_response
    metadata = test_object.metadata(metadata_scope, metadata_template)
    response = metadata.set(post_data)
    assert response is metadata_response
    mock_box_session.post.assert_called_once_with(metadata.get_url(), data=post_value, headers={b'Content-Type': b'application/json'})
    mock_box_session.put.assert_called_once_with(metadata.get_url(), data=put_value, headers={b'Content-Type': b'application/json-patch+json'})


def test_get(
        mock_box_session,
        make_mock_box_request,
        test_object,
        metadata_scope,
        metadata_template,
        metadata_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value, _ = make_mock_box_request(response=metadata_response)
    metadata = test_object.metadata(metadata_scope, metadata_template)
    response = metadata.get()
    assert response is metadata_response
    mock_box_session.get.assert_called_once_with(metadata.get_url())


@pytest.fixture
def metadata_update():
    update = MetadataUpdate()
    update.add('path', 'value')
    update.remove('path', 'value')
    update.test('path', 'value')
    update.update('path', 'value', 'value')
    return update


def test_update(
        mock_box_session,
        make_mock_box_request,
        test_object,
        metadata_scope,
        metadata_template,
        metadata_response,
        metadata_update,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.put.return_value, _ = make_mock_box_request(response=metadata_response)
    metadata = test_object.metadata(metadata_scope, metadata_template)
    response = metadata.update(metadata_update)
    assert response is metadata_response
    mock_box_session.put.assert_called_once_with(
        metadata.get_url(),
        data=json.dumps(metadata_update.ops),
        headers={b'Content-Type': b'application/json-patch+json'},
    )


def test_start_update(test_object):
    update = test_object.metadata().start_update()
    assert isinstance(update, MetadataUpdate)
