# coding: utf-8

from __future__ import unicode_literals

from boxsdk.config import API
from boxsdk.object.task_assignment import TaskAssignment

# pylint:disable=protected-access
# pylint:disable=redefined-outer-name


def test_get_assignments(test_task, mock_box_session, mock_task_assignments_response):
    expected_url = test_task.get_url('task_assignments')
    assert expected_url == '{0}/tasks/{1}/task_assignments'.format(API.BASE_API_URL, test_task.object_id)
    mock_box_session.get.return_value = mock_task_assignments_response
    task_assignments = test_task.assignments()

    assert len(task_assignments) == 1
    assert all(isinstance(m, TaskAssignment) for m in task_assignments)
