# coding: utf-8

from __future__ import unicode_literals

import json

import pytest

from boxsdk.object.collaboration import CollaborationRole, CollaborationStatus


@pytest.mark.parametrize('data', [
    {},
    {'role': CollaborationRole.EDITOR},
    {'role': CollaborationRole.VIEWER},
    {'status': CollaborationStatus.ACCEPTED},
    {'status': CollaborationStatus.REJECTED},
    {'role': CollaborationRole.EDITOR, 'status': CollaborationStatus.ACCEPTED},
])
def test_update_info_returns_the_correct_response(
        test_collaboration,
        mock_box_session,
        mock_collab_response,
        data):
    # pylint:disable=protected-access
    expected_url = test_collaboration.get_url()
    mock_box_session.put.return_value = mock_collab_response
    update_response = test_collaboration.update_info(**data)
    mock_box_session.put.assert_called_once_with(
        expected_url,
        data=json.dumps(data),
        headers=None,
        params=None,
    )
    assert isinstance(update_response, test_collaboration.__class__)
    assert update_response.object_id == test_collaboration.object_id
