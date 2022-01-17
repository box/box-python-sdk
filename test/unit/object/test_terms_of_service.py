# coding: utf-8
import json

from boxsdk.exception import BoxAPIException
from boxsdk.config import API
from boxsdk.object.terms_of_service import TermsOfService
from boxsdk.object.terms_of_service_user_status import TermsOfServiceUserStatus


def test_get(test_terms_of_service, mock_box_session):
    created_at = '2016-05-18T17:38:03-07:00'
    expected_url = f'{API.BASE_API_URL}/terms_of_services/{test_terms_of_service.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'terms_of_service',
        'id': test_terms_of_service.object_id,
        'created_at': created_at,
    }
    terms_of_service = test_terms_of_service.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(terms_of_service, TermsOfService)
    assert terms_of_service.created_at == created_at
    assert terms_of_service.id == test_terms_of_service.object_id
    assert terms_of_service.type == test_terms_of_service.object_type


def test_update(test_terms_of_service, mock_box_session):
    new_text = 'This is new text'
    expected_url = f'{API.BASE_API_URL}/terms_of_services/{test_terms_of_service.object_id}'
    mock_box_session.put.return_value.json.return_value = {
        'type': 'terms_of_service',
        'id': test_terms_of_service.object_id,
        'text': new_text,
    }
    data = {
        'text': new_text,
    }
    updated_terms_of_service = test_terms_of_service.update_info(data=data)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert isinstance(updated_terms_of_service, TermsOfService)
    assert updated_terms_of_service.text == new_text
    assert updated_terms_of_service.id == test_terms_of_service.object_id
    assert updated_terms_of_service.type == test_terms_of_service.object_type


def test_accept_terms_of_service(test_terms_of_service, test_terms_of_service_user_status, mock_user, mock_box_session):
    # pylint:disable=redefined-outer-name
    expected_url = f"{API.BASE_API_URL}/terms_of_service_user_statuses"
    created_at = '2016-05-18T17:38:03-07:00'
    value = json.dumps({
        'tos': {
            'type': 'terms_of_service',
            'id': test_terms_of_service.object_id,
        },
        'is_accepted': True,
        'user': {
            'type': mock_user.object_type,
            'id': mock_user.object_id,
        },
    })
    mock_box_session.post.return_value.json.return_value = {
        'type': 'terms_of_service_user_status',
        'id': test_terms_of_service_user_status.object_id,
        'created_at': created_at,
    }
    new_terms_of_service_user_status = test_terms_of_service.accept(mock_user)
    mock_box_session.post.assert_called_once_with(expected_url, data=value)
    assert isinstance(new_terms_of_service_user_status, TermsOfServiceUserStatus)
    assert new_terms_of_service_user_status.id == test_terms_of_service_user_status.object_id
    assert new_terms_of_service_user_status.type == test_terms_of_service_user_status.object_type
    assert new_terms_of_service_user_status.created_at == created_at


def test_reject_terms_of_service(test_terms_of_service, test_terms_of_service_user_status, mock_user, mock_box_session):
    # pylint:disable=redefined-outer-name
    expected_url = f"{API.BASE_API_URL}/terms_of_service_user_statuses"
    created_at = '2016-05-18T17:38:03-07:00'
    value = json.dumps({
        'tos': {
            'type': 'terms_of_service',
            'id': test_terms_of_service.object_id,
        },
        'is_accepted': False,
        'user': {
            'type': mock_user.object_type,
            'id': mock_user.object_id,
        },
    })
    mock_box_session.post.return_value.json.return_value = {
        'type': 'terms_of_service_user_status',
        'id': test_terms_of_service_user_status.object_id,
        'created_at': created_at,
    }
    new_terms_of_service_user_status = test_terms_of_service.reject(mock_user)
    mock_box_session.post.assert_called_once_with(expected_url, data=value)
    assert isinstance(new_terms_of_service_user_status, TermsOfServiceUserStatus)
    assert new_terms_of_service_user_status.id == test_terms_of_service_user_status.object_id
    assert new_terms_of_service_user_status.type == test_terms_of_service_user_status.object_type
    assert new_terms_of_service_user_status.created_at == created_at


def test_get_user_status(test_terms_of_service, mock_user, test_terms_of_service_user_status, mock_box_session):
    expected_url = f"{API.BASE_API_URL}/terms_of_service_user_statuses"
    created_at = '2016-05-18T17:38:03-07:00'
    expected_params = {
        'tos_id': test_terms_of_service.object_id,
        'user_id': mock_user.object_id,
    }
    mock_user_status = {
        'type': 'terms_of_service_user_status',
        'id': test_terms_of_service_user_status.object_id,
        'created_at': created_at,
    }
    mock_box_session.get.return_value.json.return_value = {
        'limit': 500,
        'entries': [mock_user_status],
    }
    new_terms_of_service_user_status = test_terms_of_service.get_user_status(user=mock_user)
    mock_box_session.get.assert_called_once_with(expected_url, params=expected_params)
    assert isinstance(new_terms_of_service_user_status, TermsOfServiceUserStatus)
    assert new_terms_of_service_user_status.type == 'terms_of_service_user_status'
    assert new_terms_of_service_user_status.id == test_terms_of_service_user_status.object_id
    assert new_terms_of_service_user_status.created_at == created_at


def test_set_user_status(test_terms_of_service, mock_user, mock_box_session):
    expected_post_url = f"{API.BASE_API_URL}/terms_of_service_user_statuses"
    expected_put_url = f"{API.BASE_API_URL}/terms_of_service_user_statuses/{test_terms_of_service.object_id}"
    post_value = json.dumps({
        'tos': {
            'type': test_terms_of_service.object_type,
            'id': test_terms_of_service.object_id,
        },
        'is_accepted': True,
        'user': {
            'type': mock_user.object_type,
            'id': mock_user.object_id,
        },
    })
    put_value = json.dumps({
        'is_accepted': True
    })
    mock_box_session.post.side_effect = [BoxAPIException(status=409, message="Conflict")]
    mock_box_session.get.return_value.json.return_value = {
        'entries': [
            {
                'type': 'terms_of_service_user_status',
                'id': '42',
            },
        ],
    }
    mock_box_session.put.return_value.json.return_value = {
        'type': 'terms_of_service_user_status',
        'id': '12345',
        'tos': {
            'type': test_terms_of_service.object_type,
            'id': test_terms_of_service.object_id,
        },
        'is_accepted': True,
    }
    new_terms_of_service_user_status = test_terms_of_service.set_user_status(True, mock_user)
    mock_box_session.post.assert_called_once_with(expected_post_url, data=post_value)
    mock_box_session.put.assert_called_once_with(expected_put_url, data=put_value, headers=None, params=None)
    assert isinstance(new_terms_of_service_user_status, TermsOfServiceUserStatus)
    assert new_terms_of_service_user_status.type == 'terms_of_service_user_status'
    assert new_terms_of_service_user_status.id == '12345'
    assert new_terms_of_service_user_status.tos['type'] == test_terms_of_service.object_type
    assert new_terms_of_service_user_status.tos['id'] == test_terms_of_service.object_id
    assert new_terms_of_service_user_status.is_accepted is True
