# coding: utf-8

from __future__ import unicode_literals
import json
import pytest

from mock import Mock
from boxsdk.object.legal_hold_policy import LegalHoldPolicy
from boxsdk.object.legal_hold_policy_assignment import LegalHoldPolicyAssignment
from boxsdk.config import API
from boxsdk.session.box_session import BoxResponse 
from boxsdk.network.default_network import DefaultNetworkResponse

@pytest.fixture(scope='module')
def policy_id_1():
    return 101


@pytest.fixture(scope='module')
def policy_id_2():
    return 202


@pytest.fixture(scope='module')
def policies_response(policy_id_1, policy_id_2):
    # pylint disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.json.return_value = {
        'entries': [
            {'type': 'legal_hold_policy', 'id': policy_id_1, 'name': 'Test Policy 1'},
            {'type': 'legal_hold_policy', 'id': policy_id_2, 'name': 'Test Policy 2'}
        ],
        'limit': 5,
    }
    return mock_network_response

def test_assign(test_legal_hold_policy, mock_box_session, test_file):
    assignment_id = '12345'
    assigned_at = '2016-05-18T17:38:03-07:00',
    expected_url = '{0}/legal_hold_policy_assignments'.format(API.BASE_API_URL)
    expected_body = {
        'policy_id': test_legal_hold_policy.object_id,
        'assign_to': {
            'type': 'file',
            'id': test_file.object_id
        }
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': 'legal_hold_policy_assignment',
        'id': assignment_id,
        'assigned_at': assigned_at,
    }
    new_legal_hold_assignment = test_legal_hold_policy.assign(test_file)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert isinstance(new_legal_hold_assignment, LegalHoldPolicyAssignment)
    assert new_legal_hold_assignment.assigned_at == assigned_at
    assert new_legal_hold_assignment.id == assignment_id

def test_get(test_legal_hold_policy, mock_box_session): 
    created_at = '2016-05-18T17:38:03-07:00',
    expected_url = '{0}/legal_hold_policies/{1}'.format(API.BASE_API_URL, test_legal_hold_policy.object_id)
    mock_box_session.get.return_value.json.return_value = {
        'type': 'legal_hold_policy',
        'id': test_legal_hold_policy.object_id,
        'created_at': created_at
    }
    legal_hold_policy = test_legal_hold_policy.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(legal_hold_policy, LegalHoldPolicy)
    assert legal_hold_policy.created_at == created_at


@pytest.fixture(scope='module')
def delete_policy_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    return mock_network_response


def test_delete_policy_return_the_correct_response(
    test_legal_hold_policy,
    mock_box_session,
    delete_policy_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value = delete_policy_response
    response = test_legal_hold_policy.delete()

    # pylint:disable=protected-access
    expected_url = test_legal_hold_policy.get_url()
    # pylint:enable = protected-access
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)

    assert response is True


def test_get_assignments(
    test_legal_hold_policy,
    mock_box_session,
    policies_response,
    policy_id_1,
    policy_id_2,
): 
    # pylint:disable=redefined-outer-name
    mock_box_session.get.return_value = policies_response
    assignments = test_legal_hold_policy.get_assignments()
    for assignment, expected_id in zip(assignments, [policy_id_1, policy_id_2]):
        assert assignment.object_id == expected_id
        # pylint:disable=protected-access
        assert assignment._session == mock_box_session

