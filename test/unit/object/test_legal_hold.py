# coding: utf-8

from boxsdk.object.legal_hold import LegalHold
from boxsdk.config import API


def test_get(test_legal_hold, mock_box_session):
    file_version_id = '1234'
    expected_url = f'{API.BASE_API_URL}/file_version_legal_holds/{test_legal_hold.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'legal_hold',
        'id': test_legal_hold.object_id,
        'file_version': {
            'type': 'file_version',
            'id': file_version_id,
        },
    }
    file_version_legal_hold = test_legal_hold.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(file_version_legal_hold, LegalHold)
    assert file_version_legal_hold['file_version']['id'] == file_version_id
    assert file_version_legal_hold.type == 'legal_hold'
    assert file_version_legal_hold.id == test_legal_hold.object_id
