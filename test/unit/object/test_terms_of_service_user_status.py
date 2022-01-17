# coding: utf-8
import json

from boxsdk.object.terms_of_service_user_status import TermsOfServiceUserStatus
from boxsdk.config import API


def test_get(test_terms_of_service_user_status, mock_box_session):
    created_at = '2016-05-18T17:38:03-07:00'
    expected_url = f'{API.BASE_API_URL}/terms_of_service_user_statuses/{test_terms_of_service_user_status.object_id}'
    mock_box_session.get.return_value.json.return_value = {
        'type': 'terms_of_service_user_status',
        'id': test_terms_of_service_user_status.object_id,
        'created_at': created_at
    }
    terms_of_service = test_terms_of_service_user_status.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(terms_of_service, TermsOfServiceUserStatus)
    assert terms_of_service.type == test_terms_of_service_user_status.object_type
    assert terms_of_service.id == test_terms_of_service_user_status.object_id
    assert terms_of_service.created_at == created_at


def test_accept(test_terms_of_service_user_status, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/terms_of_service_user_statuses/{test_terms_of_service_user_status.object_id}'
    mock_box_session.put.return_value.json.return_value = {
        'type': test_terms_of_service_user_status.object_type,
        'id': test_terms_of_service_user_status.object_id,
        'is_accepted': True
    }
    data = {'is_accepted': True}
    terms_of_service_user_status = test_terms_of_service_user_status.accept()
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert isinstance(terms_of_service_user_status, TermsOfServiceUserStatus)
    assert terms_of_service_user_status.type == test_terms_of_service_user_status.object_type
    assert terms_of_service_user_status.id == test_terms_of_service_user_status.object_id
    assert terms_of_service_user_status.is_accepted is True


def test_reject(test_terms_of_service_user_status, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/terms_of_service_user_statuses/{test_terms_of_service_user_status.object_id}'
    mock_box_session.put.return_value.json.return_value = {
        'type': 'terms_of_service_user_status',
        'id': test_terms_of_service_user_status.object_id,
        'is_accepted': False
    }
    data = {'is_accepted': False}
    terms_of_service_user_status = test_terms_of_service_user_status.reject()
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert isinstance(terms_of_service_user_status, TermsOfServiceUserStatus)
    assert terms_of_service_user_status.type == test_terms_of_service_user_status.object_type
    assert terms_of_service_user_status.id == test_terms_of_service_user_status.object_id
    assert terms_of_service_user_status.is_accepted is False
