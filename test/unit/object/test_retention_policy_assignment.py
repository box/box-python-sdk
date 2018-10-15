from __future__ import unicode_literals, absolute_import

from boxsdk.config import API
from boxsdk.object.retention_policy_assignment import RetentionPolicyAssignment


def test_get_assignment(test_retention_policy_assignment, mock_box_session):
    expected_url = '{0}/retention_policy_assignments/{1}'.format(API.BASE_API_URL, test_retention_policy_assignment.object_id)
    mock_box_session.get.return_value.json.return_value = {
        'type': test_retention_policy_assignment.object_type,
        'id': test_retention_policy_assignment.object_id,
    }
    retention_policy_assignment = test_retention_policy_assignment.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(retention_policy_assignment, RetentionPolicyAssignment)
    assert retention_policy_assignment['type'] == test_retention_policy_assignment.object_type
    assert retention_policy_assignment['id'] == test_retention_policy_assignment.object_id
