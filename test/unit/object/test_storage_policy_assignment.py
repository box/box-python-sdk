# coding: utf-8
import json
import pytest

from mock import Mock
from boxsdk.config import API
from boxsdk.object.storage_policy_assignment import StoragePolicyAssignment
from boxsdk.network.default_network import DefaultNetworkResponse


@pytest.fixture(scope='module')
def delete_assignment_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    return mock_network_response


def test_get(test_storage_policy_assignment, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/storage_policy_assignments/{test_storage_policy_assignment.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'storage_policy_assignment',
        'id': test_storage_policy_assignment.object_id,
    }
    storage_policy_assignment = test_storage_policy_assignment.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(storage_policy_assignment, StoragePolicyAssignment)


def test_update(test_storage_policy_assignment, mock_box_session):
    new_policy_id = '1234'
    expected_url = f'{API.BASE_API_URL}/storage_policy_assignments/{test_storage_policy_assignment.object_id}'
    mock_box_session.put.return_value.json.return_value = {
        'type': 'storage_policy_assignment',
        'id': new_policy_id,
    }
    storage_policy_assignment = test_storage_policy_assignment.update_info(data={
        'storage_policy': {
            'type': 'storage_policy',
            'id': new_policy_id,
        }
    })
    data = {
        'storage_policy': {
            'type': 'storage_policy',
            'id': new_policy_id,
        }
    }
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert isinstance(storage_policy_assignment, StoragePolicyAssignment)


def test_delete(test_storage_policy_assignment, delete_assignment_response, mock_box_session):
    mock_box_session.delete.return_value = delete_assignment_response
    response = test_storage_policy_assignment.delete()
    expected_url = test_storage_policy_assignment.get_url()
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)
    assert response is True
