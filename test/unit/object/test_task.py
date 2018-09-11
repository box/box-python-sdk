from __future__ import unicode_literals

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
    expected_url = '{0}/tasks/{1}'.format(API.BASE_API_URL, test_task.object_id)
    mock_box_session.get.return_value.json.return_value = {
        'type': 'task',
        'id': test_task.object_id,
    }
    retrieved_task = test_task.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(retrieved_task, Task)


def test_update(test_task, mock_box_session):
    new_message = 'New Message'
    expected_url = '{0}/tasks/{1}'.format(API.BASE_API_URL, test_task.object_id)
    mock_box_session.put.return_value.json.return_value = {
        'type': 'task',
        'id': test_task.object_id,
        'message': new_message,
    }
    expected_body = {
        'message': new_message,
    }
    updated_task = test_task.update_info({'message': new_message})
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(expected_body), headers=None, params=None)
    assert isinstance(updated_task, Task)
    assert updated_task.message == new_message


def test_delete_policy_return_the_correct_response(
        test_task,
        mock_box_session,
        delete_task_response,
):
    # pylint:disable=redefined-outer-name
    mock_box_session.delete.return_value = delete_task_response
    response = test_task.delete()
    # pylint:disable=protected-access
    expected_url = test_task.get_url()
    # pylint:enable = protected-access
    mock_box_session.delete.assert_called_once_with(expected_url, params={}, expect_json_response=False, headers=None)
    assert response is True


def test_assign(test_task, mock_box_session, mock_user):
    expected_url = '{0}/task_assignments'.format(API.BASE_API_URL)
    expected_body = {
        'task': {
            'type': 'task',
            'id': test_task.object_id,
        },
        'assign_to': {
            'id': mock_user.object_id,
            'login': None,
        },
    }
    mock_box_session.post.return_value.json.return_value = {
        'type': 'task_assignment',
        'id': 42,
    }
    new_legal_hold_assignment = test_task.assign(assign_to_id=mock_user.object_id)
    mock_box_session.post.assert_called_once_with(expected_url, data=json.dumps(expected_body))
    assert isinstance(new_legal_hold_assignment, TaskAssignment)


def test_assignments(test_task, mock_box_session):
    expected_url = test_task.get_url('assignments')
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
    assignments = test_task.assignments()
    assignment = assignments.next()
    mock_box_session.get.assert_called_once_with(expected_url, params={})
    assert isinstance(assignment, TaskAssignment)
    assert assignment.id == mock_assignment['id']
    assert assignment.item['id'] == mock_assignment['item']['id']
