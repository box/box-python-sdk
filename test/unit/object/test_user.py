# coding: utf-8

from __future__ import unicode_literals

from boxsdk.config import API
from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment


def test_user_url(mock_user):
    # pylint:disable=redefined-outer-name, protected-access
    assert mock_user.get_url() == '{0}/{1}/{2}'.format(API.BASE_API_URL, 'users', mock_user.object_id)


def test_get_storage_policy_assignments(mock_user, mock_box_session):
    expected_url = mock_box_session.get_url('storage_policy_assignments')
    mock_assignment = {
        'type': 'storage_policy_assignment',
        'id': '12345',
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_assignment]
    }
    expected_params = {
        'resolved_for_type': 'user',
        'resolved_for_id': mock_user.object_id,
    }
    assignment = mock_user.storage_policy_assignments()
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params)
    assert isinstance(assignment, StoragePolicyAssignment)
    assert assignment.id == mock_assignment['id']
    assert assignment.type == mock_assignment['type']
