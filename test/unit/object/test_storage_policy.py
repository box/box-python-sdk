# coding: utf-8
from __future__ import unicode_literals

import json
from boxsdk.config import API
from boxsdk.object.storage_policy import StoragePolicy


def test_get(test_storage_policy, mock_box_session):
    expected_url = '{0}/storage_policies/{1}'.format(API.BASE_API_URL, test_storage_policy.object_id)
    mock_box_session.get.return_value.json.return_value = {
        'type': 'storage_policy',
        'id': test_storage_policy.object_id,
    }
    storage_policy = test_storage_policy.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(storage_policy, StoragePolicy)


def test_assign(test_storage_policy, mock_user, mock_box_session):
    expected_url = '{0}/storage_policy_assignments'.format(API.BASE_API_URL)
    expected_data = {
        'storage_policy': {
            'type': 'storage_policy',
            'id': '42',
        },
        'assigned_to': {
            'type': 'user',
            'id': 'fake-user-100',
        }
    }
    mock_assignment = {
        'type': 'storage_policy_assignment',
        'id': '1234',
        'storage_policy': {
            'type': 'storage_policy',
            'id': '1111',
        }
    }
    mock_box_session.post.return_value.json.return_value = mock_assignment
    assignment = test_storage_policy.assign(mock_user)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_data))
    assert assignment.id == mock_assignment['id']
    assert assignment.storage_policy['id'] == mock_assignment['storage_policy']['id']
