from boxsdk.config import API
from boxsdk.object.file import File
from boxsdk.object.file_version import FileVersion
from boxsdk.object.retention_policy_assignment import RetentionPolicyAssignment


def test_get_assignment(test_retention_policy_assignment, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/retention_policy_assignments/{test_retention_policy_assignment.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': test_retention_policy_assignment.object_type,
        'id': test_retention_policy_assignment.object_id,
    }
    retention_policy_assignment = test_retention_policy_assignment.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(retention_policy_assignment, RetentionPolicyAssignment)
    assert retention_policy_assignment['type'] == test_retention_policy_assignment.object_type
    assert retention_policy_assignment['id'] == test_retention_policy_assignment.object_id


def test_get_files_under_retention(test_retention_policy_assignment, test_file, mock_box_session):
    # given:
    test_marker = 'test_marker'
    test_limit = 50
    target_url = f"{API.BASE_API_URL}/retention_policy_assignments/{test_retention_policy_assignment.object_id}/files_under_retention"

    mock_box_session.get.return_value.json.return_value = {
        'limit': test_limit,
        'entries': [test_file],
        'next_marker': test_marker,
    }

    # when:
    files_under_retention = test_retention_policy_assignment.get_files_under_retention(
        limit=test_limit,
        marker=test_marker
    )
    file_under_retention = files_under_retention.next()

    # then:
    params = {
        'limit': test_limit,
        'marker': test_marker,
    }
    mock_box_session.get.assert_called_once_with(target_url, params=params)
    assert isinstance(file_under_retention, File)
    assert file_under_retention.object_id == test_file.object_id


def test_get_file_versions_under_retention(test_retention_policy_assignment, test_file_version, mock_box_session):
    # given:
    test_marker = 'test_marker'
    test_limit = 50
    target_url = f"{API.BASE_API_URL}/retention_policy_assignments/{test_retention_policy_assignment.object_id}/file_versions_under_retention"

    mock_box_session.get.return_value.json.return_value = {
        'limit': test_limit,
        'entries': [test_file_version],
        'next_marker': test_marker,
    }

    # when:
    file_versions_under_retention = test_retention_policy_assignment.get_file_versions_under_retention(
        limit=test_limit,
        marker=test_marker
    )
    file_version_under_retention = file_versions_under_retention.next()

    # then:
    params = {
        'limit': test_limit,
        'marker': test_marker,
    }
    mock_box_session.get.assert_called_once_with(target_url, params=params)
    assert isinstance(file_version_under_retention, FileVersion)
    assert file_version_under_retention.object_id == test_file_version.object_id
