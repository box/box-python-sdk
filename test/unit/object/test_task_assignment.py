import json
import pytest

from mock import Mock
from boxsdk.config import API
from boxsdk.object.task_assignment import TaskAssignment, ResolutionState
from boxsdk.network.default_network import DefaultNetworkResponse


@pytest.fixture(scope='module')
def delete_task_assignment_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    return mock_network_response


def test_get_assignment(test_task_assignment, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/task_assignments/{test_task_assignment.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': test_task_assignment.object_type,
        'id': test_task_assignment.object_id,
        'assigned_to': {
            'type': 'user',
            'id': '11111',
        },
    }
    retrieved_task = test_task_assignment.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(retrieved_task, TaskAssignment)
    assert retrieved_task.object_type == test_task_assignment.object_type
    assert retrieved_task.object_id == test_task_assignment.object_id
    assert retrieved_task.assigned_to['type'] == 'user'
    assert retrieved_task.assigned_to['id'] == '11111'


def test_delete_policy_return_the_correct_response(
        test_task_assignment,
        mock_box_session,
        delete_task_assignment_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value = delete_task_assignment_response
    response = test_task_assignment.delete()
    # pylint:disable=protected-access
    expected_url = f'{API.BASE_API_URL}/task_assignments/{test_task_assignment.object_id}'
    # pylint:enable = protected-access
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)
    assert response is True


def test_update(test_task_assignment, mock_box_session):
    new_message = 'New Message'
    resolution_state = ResolutionState.APPROVED
    expected_url = f'{API.BASE_API_URL}/task_assignments/{test_task_assignment.object_id}'
    mock_box_session.put.return_value.json.return_value = {
        'type': 'task_assignment',
        'id': test_task_assignment.object_id,
        'message': new_message,
        'resolution_state': resolution_state,
    }
    expected_body = {
        'message': new_message,
        'resolution_state': resolution_state,
    }
    updated_task_assignment = test_task_assignment.update_info(data={'message': new_message, 'resolution_state': resolution_state})
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_body), headers=None, params=None)
    assert isinstance(updated_task_assignment, TaskAssignment)
    assert updated_task_assignment.message == new_message
    assert updated_task_assignment.object_type == test_task_assignment.object_type
    assert updated_task_assignment.object_id == test_task_assignment.object_id
    assert updated_task_assignment.resolution_state == resolution_state
