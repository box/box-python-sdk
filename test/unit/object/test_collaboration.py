# coding: utf-8

import json
import pytest

from boxsdk.config import API
from boxsdk.object.collaboration import CollaborationRole, CollaborationStatus


@pytest.mark.parametrize('data', [
    {},
    {'role': CollaborationRole.EDITOR},
    {'role': CollaborationRole.VIEWER},
    {'status': CollaborationStatus.ACCEPTED},
    {'status': CollaborationStatus.REJECTED},
    {'role': CollaborationRole.EDITOR, 'status': CollaborationStatus.ACCEPTED},
])
def test_update_info_returns_the_correct_response(
        test_collaboration,
        mock_box_session,
        mock_collab_response,
        data):
    # pylint:disable=protected-access
    expected_url = test_collaboration.get_url()
    mock_box_session.put.return_value = mock_collab_response
    update_response = test_collaboration.update_info(**data)
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(data),
        headers=None,
        params=None,
    )
    assert isinstance(update_response, test_collaboration.__class__)
    assert update_response.object_id == test_collaboration.object_id


def test_update_info_returns_204(
        test_collaboration,
        mock_box_session):
    # pylint:disable=protected-access
    data = {'role': CollaborationRole.OWNER, 'status': CollaborationStatus.ACCEPTED}
    expected_url = test_collaboration.get_url()
    mock_box_session.put.return_value.ok = True
    is_success = test_collaboration.update_info(**data)
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(data),
        expect_json_response=False,
        headers=None,
        params=None,
    )
    assert is_success is True


def test_accept_pending_collaboration(test_collaboration, mock_box_session):
    # pylint:disable=protected-access
    new_status = 'accepted'
    expected_url = f'{API.BASE_API_URL}/collaborations/{test_collaboration.object_id}'
    mock_collab_response = {
        'type': 'collaboration',
        'id': '1234',
        'status': 'accepted',
    }
    mock_box_session.put.return_value.json.return_value = mock_collab_response
    response = test_collaboration.accept()
    update_body = {
        'status': 'accepted'
    }
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(update_body),
        headers=None,
        params=None,
    )
    assert isinstance(response, test_collaboration.__class__)
    assert response.status == new_status


def test_reject_pending_collaboration(test_collaboration, mock_box_session):
    # pylint:disable=protected-access
    new_status = 'rejected'
    expected_url = f'{API.BASE_API_URL}/collaborations/{test_collaboration.object_id}'
    mock_collab_response = {
        'type': 'collaboration',
        'id': '1234',
        'status': 'rejected',
    }
    mock_box_session.put.return_value.json.return_value = mock_collab_response
    response = test_collaboration.reject()
    update_body = {
        'status': 'rejected'
    }
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(update_body),
        headers=None,
        params=None,
    )
    assert isinstance(response, test_collaboration.__class__)
    assert response.status == new_status
