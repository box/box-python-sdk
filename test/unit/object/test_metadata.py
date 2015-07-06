# coding: utf-8

from __future__ import unicode_literals
import json
import pytest
from boxsdk.object.metadata import MetadataUpdate


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


@pytest.fixture
def metadata_template():
    return 'properties'


@pytest.mark.parametrize('success', [True, False])
def test_delete(mock_box_session, make_mock_box_request, test_file, metadata_scope, metadata_template, success):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value, _ = make_mock_box_request(response_ok=success)
    metadata = test_file.metadata(metadata_scope, metadata_template)
    assert metadata.delete() is success
    mock_box_session.delete.assert_called_once_with(metadata.get_url())


def test_create(
        mock_box_session,
        make_mock_box_request,
        test_file,
        metadata_scope,
        metadata_template,
        metadata_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.post.return_value, _ = make_mock_box_request(response=metadata_response)
    metadata = test_file.metadata(metadata_scope, metadata_template)
    response = metadata.create(metadata_response)
    assert response is metadata_response
    mock_box_session.post.assert_called_once_with(
        metadata.get_url(),
        data=json.dumps(metadata_response),
        headers={b'Content-Type': b'application/json'},
    )


def test_get(
        mock_box_session,
        make_mock_box_request,
        test_file,
        metadata_scope,
        metadata_template,
        metadata_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value, _ = make_mock_box_request(response=metadata_response)
    metadata = test_file.metadata(metadata_scope, metadata_template)
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
        test_file,
        metadata_scope,
        metadata_template,
        metadata_response,
        metadata_update,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.put.return_value, _ = make_mock_box_request(response=metadata_response)
    metadata = test_file.metadata(metadata_scope, metadata_template)
    response = metadata.update(metadata_update)
    assert response is metadata_response
    mock_box_session.put.assert_called_once_with(
        metadata.get_url(),
        data=json.dumps(metadata_update.ops),
        headers={b'Content-Type': b'application/json-patch+json'},
    )


def test_start_update(test_file):
    update = test_file.metadata().start_update()
    assert isinstance(update, MetadataUpdate)
