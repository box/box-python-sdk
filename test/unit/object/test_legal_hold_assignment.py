# coding: utf-8

import pytest

from mock import Mock
from boxsdk.object.legal_hold_policy_assignment import LegalHoldPolicyAssignment
from boxsdk.config import API
from boxsdk.network.default_network import DefaultNetworkResponse


def test_get(test_legal_hold_policy_assignment, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/legal_hold_policy_assignments/{test_legal_hold_policy_assignment.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'legal_hold_policy_assignment',
        'id': test_legal_hold_policy_assignment.object_id,
        'assigned_to': {
            'type': 'user',
            'id': '1234',
        },
    }
    legal_hold_policy_assignment = test_legal_hold_policy_assignment.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(legal_hold_policy_assignment, LegalHoldPolicyAssignment)
    assert legal_hold_policy_assignment.type == 'legal_hold_policy_assignment'
    assert legal_hold_policy_assignment.object_id == test_legal_hold_policy_assignment.object_id
    assert legal_hold_policy_assignment['assigned_to']['type'] == 'user'
    assert legal_hold_policy_assignment['assigned_to']['id'] == '1234'


@pytest.fixture(scope='module')
def delete_assignment_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    return mock_network_response


def test_delete_policy_return_the_correct_response(
        test_legal_hold_policy_assignment,
        mock_box_session,
        delete_assignment_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value = delete_assignment_response
    response = test_legal_hold_policy_assignment.delete()
    # pylint:disable=protected-access
    expected_url = test_legal_hold_policy_assignment.get_url()
    # pylint:enable = protected-access
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)
    assert response is True
