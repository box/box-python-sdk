from boxsdk.config import API
from boxsdk.object.file_version_retention import FileVersionRetention


def test_get(test_file_version_retention, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/file_version_retentions/{test_file_version_retention.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'file_version_retention',
        'id': test_file_version_retention.object_id,
    }
    file_version_retention = test_file_version_retention.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(file_version_retention, FileVersionRetention)
