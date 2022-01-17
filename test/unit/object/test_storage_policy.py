# coding: utf-8

import json
from boxsdk.config import API
from boxsdk.object.storage_policy import StoragePolicy
from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment


def test_get(test_storage_policy, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/storage_policies/{test_storage_policy.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': test_storage_policy.object_type,
        'id': test_storage_policy.object_id,
    }
    storage_policy = test_storage_policy.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(storage_policy, StoragePolicy)


def test_assign_with_same_assignment(test_storage_policy, test_storage_policy_assignment, mock_user, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/storage_policy_assignments'
    additional_params = {
        'resolved_for_type': mock_user.object_type,
        'resolved_for_id': mock_user.object_id,
    }
    mock_box_session.get.return_value.json.return_value = {
        'next_marker': None,
        'limit': 1,
        'entries': [
            {
                'type': test_storage_policy_assignment.object_type,
                'id': test_storage_policy_assignment.object_id,
                'storage_policy': {
                    'type': test_storage_policy.object_type,
                    'id': test_storage_policy.object_id,
                },
            },
        ],
    }
    assignment = test_storage_policy.assign(mock_user)
    mock_box_session.get.assert_called_once_with(expected_url, params=additional_params)
    assert isinstance(assignment, StoragePolicyAssignment)
    assert assignment.type == test_storage_policy_assignment.object_type
    assert assignment.id == test_storage_policy_assignment.object_id
    assert assignment.storage_policy['type'] == test_storage_policy.object_type
    assert assignment.storage_policy['id'] == test_storage_policy.object_id


def test_assign_with_assigned_enterprise(test_storage_policy, test_storage_policy_assignment, mock_user, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/storage_policy_assignments'
    additional_params = {
        'resolved_for_type': mock_user.object_type,
        'resolved_for_id': mock_user.object_id,
    }
    expected_data = {
        'storage_policy': {
            'type': test_storage_policy.object_type,
            'id': test_storage_policy.object_id,
        },
        'assigned_to': {
            'type': mock_user.object_type,
            'id': mock_user.object_id,
        },
    }
    mock_box_session.get.return_value.json.return_value = {
        'next_marker': None,
        'limit': 1,
        'entries': [
            {
                'type': test_storage_policy_assignment.object_type,
                'id': '11111',
                'storage_policy': {
                    'type': test_storage_policy.object_type,
                    'id': '22222',
                },
                'assigned_to': {
                    'type': 'enterprise',
                    'id': '12345',
                },
            },
        ],
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': test_storage_policy_assignment.object_type,
        'id': test_storage_policy_assignment.object_id,
        'storage_policy': {
            'type': test_storage_policy.object_type,
            'id': test_storage_policy.object_id
        }
    }
    assignment = test_storage_policy.assign(mock_user)
    mock_box_session.get.assert_called_once_with(expected_url, params=additional_params)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert isinstance(assignment, StoragePolicyAssignment)
    assert assignment.type == test_storage_policy_assignment.object_type
    assert assignment.id == test_storage_policy_assignment.object_id
    assert assignment.storage_policy['type'] == test_storage_policy.object_type
    assert assignment.storage_policy['id'] == test_storage_policy.object_id


def test_assign_with_update(test_storage_policy, test_storage_policy_assignment, mock_user, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/storage_policy_assignments'
    expected_put_url = f'{API.BASE_API_URL}/storage_policy_assignments/11111'
    additional_params = {
        'resolved_for_type': mock_user.object_type,
        'resolved_for_id': mock_user.object_id,
    }
    expected_data = {
        'storage_policy': {
            'type': test_storage_policy.object_type,
            'id': '42',
        },
    }
    mock_box_session.get.return_value.json.return_value = {
        'next_marker': None,
        'limit': 1,
        'entries': [
            {
                'type': test_storage_policy_assignment.object_type,
                'id': '11111',
                'storage_policy': {
                    'type': test_storage_policy.object_type,
                    'id': '22222',
                },
                'assigned_to': {
                    'type': 'user',
                    'id': '12345',
                },
            },
        ],
    }
    mock_box_session.put.return_value.json.return_value = {
        'type': test_storage_policy_assignment.object_type,
        'id': test_storage_policy_assignment.object_id,
        'storage_policy': {
            'type': test_storage_policy.object_type,
            'id': '42'
        }
    }
    assignment = test_storage_policy.assign(mock_user)
    mock_box_session.get.assert_called_once_with(expected_url, params=additional_params)
    mock_box_session.put.assert_called_once_with(expected_put_url, data=json.dumps(expected_data), headers=None, params=None)
    assert isinstance(assignment, StoragePolicyAssignment)
    assert assignment.type == test_storage_policy_assignment.object_type
    assert assignment.id == test_storage_policy_assignment.object_id
    assert assignment.storage_policy['type'] == test_storage_policy.object_type
    assert assignment.storage_policy['id'] == '42'


def test_create_assignment(test_storage_policy, mock_user, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/storage_policy_assignments'
    expected_data = {
        'storage_policy': {
            'type': 'storage_policy',
            'id': '42',
        },
        'assigned_to': {
            'type': 'user',
            'id': 'fake-user-100',
        },
    }
    mock_assignment = {
        'type': 'storage_policy_assignment',
        'id': '1234',
        'storage_policy': {
            'type': test_storage_policy.object_type,
            'id': test_storage_policy.object_id,
        },
    }
    mock_box_session.post.return_value.json.return_value = mock_assignment
    assignment = test_storage_policy.create_assignment(mock_user)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert assignment.id == mock_assignment['id']
    assert assignment.storage_policy['id'] == mock_assignment['storage_policy']['id']
