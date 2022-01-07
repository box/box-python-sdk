# coding: utf-8

import json
import pytest

from boxsdk.config import API
from boxsdk.object.enterprise import Enterprise
from boxsdk.object.invite import Invite


@pytest.fixture()
def test_enterprise(mock_box_session):
    return Enterprise(
        session=mock_box_session,
        object_id='test_enterprise_id',
    )


def test_invite_user(test_enterprise, mock_box_session):
    # pylint:disable=redefined-outer-name
    expected_url = f'{API.BASE_API_URL}/invites'
    test_user_login = 'test@user.com'
    expected_body = json.dumps({
        'enterprise': {
            'id': test_enterprise.object_id,
        },
        'actionable_by': {
            'login': test_user_login,
        },
    })
    invite_json = {
        'type': 'invite',
        'id': '11111',
        'status': 'pending',
    }
    mock_box_session.post.return_value.json.return_value = invite_json
    new_invite = test_enterprise.invite_user(test_user_login)
    mock_box_session.post.assert_called_once_with(expected_url, data=expected_body)
    assert isinstance(new_invite, Invite)
    assert new_invite.object_id == invite_json['id']
    assert new_invite._session == mock_box_session  # pylint: disable=protected-access
    assert new_invite.status == invite_json['status']
