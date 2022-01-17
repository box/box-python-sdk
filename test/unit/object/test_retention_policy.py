import json

from boxsdk.config import API
from boxsdk.object.retention_policy import RetentionPolicy
from boxsdk.object.retention_policy_assignment import RetentionPolicyAssignment


def test_get(test_retention_policy, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/retention_policies/{test_retention_policy.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': test_retention_policy.object_type,
        'id': test_retention_policy.object_id,
        'policy_name': 'Policy Name',
        'policy_type': 'finite',
        'retention_length': '10',
        'disposition_action': 'permanently_delete',
    }
    retention_policy = test_retention_policy.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(retention_policy, RetentionPolicy)
    assert retention_policy['type'] == test_retention_policy.object_type
    assert retention_policy['id'] == test_retention_policy.object_id
    assert retention_policy['policy_name'] == 'Policy Name'


def test_update(test_retention_policy, mock_box_session):
    new_policy_name = 'New Name'
    expected_url = f'{API.BASE_API_URL}/retention_policies/{test_retention_policy.object_id}'
    mock_box_session.put.return_value.json.return_value = {
        'type': test_retention_policy.object_type,
        'id': test_retention_policy.object_id,
        'policy_name': new_policy_name,
        'policy_type': 'finite',
        'retention_length': '10',
    }
    data = {
        'policy_name': new_policy_name,
    }
    retention_policy = test_retention_policy.update_info(data=data)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert isinstance(retention_policy, RetentionPolicy)
    assert retention_policy['type'] == test_retention_policy.object_type
    assert retention_policy['id'] == test_retention_policy.object_id
    assert retention_policy['policy_name'] == new_policy_name


def test_assign(test_retention_policy, test_folder, mock_box_session):
    policy_id = '42'
    expected_url = mock_box_session.get_url('retention_policy_assignments')
    expected_data = {
        'policy_id': policy_id,
        'assign_to': {
            'type': test_folder.object_type,
            'id': test_folder.object_id,
        }
    }
    mock_assignment = {
        'type': 'retention_policy_assignment',
        'id': '1234',
        'retention_policy': {
            'type': 'retention_policy',
            'id': policy_id,
        }
    }
    mock_box_session.post.return_value.json.return_value = mock_assignment
    assignment = test_retention_policy.assign(test_folder)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data), params={})
    assert assignment.id == mock_assignment['id']
    assert assignment.retention_policy['id'] == mock_assignment['retention_policy']['id']
    assert isinstance(assignment, RetentionPolicyAssignment)


def test_get_assignments(test_retention_policy, mock_box_session):
    expected_url = test_retention_policy.get_url('assignments')
    mock_assignment = {
        'type': 'retention_policy_assignment',
        'id': '12345',
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_assignment],
        'next_marker': 'testMarker',
    }
    assignments = test_retention_policy.assignments()
    assignment = assignments.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(assignment, RetentionPolicyAssignment)
    assert assignment.id == mock_assignment['id']
    assert assignment.type == mock_assignment['type']
