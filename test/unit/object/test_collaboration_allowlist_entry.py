# coding: utf-8

from boxsdk.config import API


def test_get(mock_box_session, test_collaboration_allowlist_entry):
    entry_id = test_collaboration_allowlist_entry.object_id
    expected_url = f'{API.BASE_API_URL}/collaboration_whitelist_entries/{entry_id}'
    mock_entry = {
        'type': 'collaboration_whitelist_entry',
        'id': '98765',
        'domain': 'example.com',
        'direction': 'inbound'
    }
    mock_box_session.get.return_value.json.return_value = mock_entry
    entry = test_collaboration_allowlist_entry.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert entry.id == mock_entry['id']
    assert entry.domain == mock_entry['domain']
    assert entry.direction == mock_entry['direction']


def test_delete(mock_box_session, test_collaboration_allowlist_entry):
    entry_id = test_collaboration_allowlist_entry.object_id
    expected_url = f'{API.BASE_API_URL}/collaboration_whitelist_entries/{entry_id}'
    test_collaboration_allowlist_entry.delete()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})
