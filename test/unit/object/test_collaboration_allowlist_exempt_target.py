# coding: utf-8

from boxsdk.config import API


def test_get(mock_box_session, test_collaboration_allowlist_exemption):
    exemption_id = test_collaboration_allowlist_exemption.object_id
    expected_url = f'{API.BASE_API_URL}/collaboration_whitelist_exempt_targets/{exemption_id}'
    mock_exemption = {
        'type': 'collaboration_whitelist_entry',
        'id': '98765',
        'domain': 'example.com',
        'direction': 'inbound'
    }
    mock_box_session.get.return_value.json.return_value = mock_exemption
    exemption = test_collaboration_allowlist_exemption.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert exemption.id == mock_exemption['id']
    assert exemption.domain == mock_exemption['domain']
    assert exemption.direction == mock_exemption['direction']


def test_delete(mock_box_session, test_collaboration_allowlist_exemption):
    exemption_id = test_collaboration_allowlist_exemption.object_id
    expected_url = mock_box_session.get_url('collaboration_whitelist_exempt_targets', exemption_id)
    test_collaboration_allowlist_exemption.delete()
    mock_box_session.delete.assert_called_once_with(expected_url, expect_json_response=False, headers=None, params={})
