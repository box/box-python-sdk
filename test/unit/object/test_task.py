import json
import pytest

from mock import Mock
from boxsdk.config import API
from boxsdk.object.task import Task
from boxsdk.object.task_assignment import TaskAssignment
from boxsdk.network.default_network import DefaultNetworkResponse


@pytest.fixture(scope='module')
def delete_task_response():
    # pylint:disable=redefined-outer-name
    mock_network_response = Mock(DefaultNetworkResponse)
    mock_network_response.ok = True
    return mock_network_response


def test_get(test_task, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/tasks/{test_task.object_id}'
    due_at = '2014-04-03T11:09:43-07:00'
    action = 'review'
    message = 'Test Message'
    mock_box_session.get.return_value.json.return_value = {
        'type': test_task.object_type,
        'id': test_task.object_id,
        'due_at': due_at,
        'action': action,
        'message': message,
    }
    retrieved_task = test_task.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(retrieved_task, Task)
    assert retrieved_task.object_type == test_task.object_type
    assert retrieved_task.object_id == test_task.object_id
    assert retrieved_task.due_at == due_at
    assert retrieved_task.action == action
    assert retrieved_task.message == message


def test_update(test_task, mock_box_session):
    new_message = 'New Message'
    expected_url = f'{API.BASE_API_URL}/tasks/{test_task.object_id}'
    mock_box_session.put.return_value.json.return_value = {
        'type': test_task.object_type,
        'id': test_task.object_id,
        'message': new_message,
    }
    expected_body = {
        'message': new_message,
    }
    updated_task = test_task.update_info(data={'message': new_message})
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_body), headers=None, params=None)
    assert isinstance(updated_task, Task)
    assert updated_task.message == new_message
    assert updated_task.object_type == test_task.object_type
    assert updated_task.object_id == test_task.object_id


def test_delete_policy_return_the_correct_response(
        test_task,
        mock_box_session,
        delete_task_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value = delete_task_response
    response = test_task.delete()
    # pylint:disable=protected-access
    expected_url = f'{API.BASE_API_URL}/tasks/{test_task.object_id}'
    # pylint:enable = protected-access
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)
    assert response is True


def test_assign(test_task, mock_user, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/task_assignments'
    expected_body = {
        'task': {
            'type': test_task.object_type,
            'id': test_task.object_id,
        },
        'assign_to': {
            'id': mock_user.object_id,
        },
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': 'task_assignment',
        'id': '42',
        'assigned_to': {
            'type': 'user',
            'id': '1234',
        },
        'assigned_at': '2013-05-10T11:43:41-07:00',
    }
    new_task_assignment = test_task.assign(assignee=mock_user)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert isinstance(new_task_assignment, TaskAssignment)
    assert new_task_assignment.object_type == 'task_assignment'
    assert new_task_assignment.object_id == '42'
    assert new_task_assignment.assigned_to['type'] == 'user'
    assert new_task_assignment.assigned_at == '2013-05-10T11:43:41-07:00'


def test_assign_with_login(test_task, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/task_assignments'
    expected_body = {
        'task': {
            'type': test_task.object_type,
            'id': test_task.object_id,
        },
        'assign_to': {
            'login': 'test_user@example.com',
        },
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': 'task_assignment',
        'id': '42',
        'assigned_to': {
            'type': 'user',
            'id': '1234',
        },
        'assigned_at': '2013-05-10T11:43:41-07:00',
    }
    new_task_assignment = test_task.assign_with_login(assignee_login='test_user@example.com')
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert isinstance(new_task_assignment, TaskAssignment)
    assert new_task_assignment.object_type == 'task_assignment'
    assert new_task_assignment.object_id == '42'
    assert new_task_assignment.assigned_to['type'] == 'user'
    assert new_task_assignment.assigned_at == '2013-05-10T11:43:41-07:00'


def test_get_assignments(test_task, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/tasks/{test_task.object_id}/assignments'
    mock_assignment = {
        'type': 'task_assignment',
        'id': '12345',
        'item': {
            'type': 'file',
            'id': '33333'
        }
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 100,
        'entries': [mock_assignment]
    }
    assignments = test_task.get_assignments()
    assignment = assignments.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(assignment, TaskAssignment)
    assert assignment.id == mock_assignment['id']
    assert assignment.item['id'] == mock_assignment['item']['id']
