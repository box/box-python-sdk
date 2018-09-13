# coding: utf-8
from __future__ import unicode_literals

import json

from boxsdk.config import API
from boxsdk.object.terms_of_service import TermsOfService
from boxsdk.object.terms_of_service_user_status import TermsOfServiceUserStatus


def test_get(test_terms_of_service, mock_box_session):
    created_at = '2016-05-18T17:38:03-07:00',
    expected_url = '{0}/terms_of_services/{1}'.format(API.BASE_API_URL, test_terms_of_service.object_id)
    mock_box_session.get.return_value.json.return_value = {
        'type': 'terms_of_service',
        'id': test_terms_of_service.object_id,
        'created_at': created_at,
    }
    terms_of_service = test_terms_of_service.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(terms_of_service, TermsOfService)
    assert terms_of_service.created_at == created_at


def test_update(test_terms_of_service, mock_box_session):
    new_text = 'This is new text'
    expected_url = '{0}/terms_of_services/{1}'.format(API.BASE_API_URL, test_terms_of_service.object_id)
    mock_box_session.put.return_value.json.return_value = {
        'type': 'terms_of_service',
        'id': test_terms_of_service.object_id,
        'text': new_text,
    }
    data = {
        'text': new_text,
    }
    updated_terms_of_service = test_terms_of_service.update_info(data)
    mock_box_session.put.assert_called_once_with(expected_url, data=json.dumps(data), headers=None, params=None)
    assert isinstance(updated_terms_of_service, TermsOfService)
    assert updated_terms_of_service.text == new_text


def test_create_user_status(test_terms_of_service, test_terms_of_service_user_status, mock_user, mock_box_session):
    #pylint:disable=redefined-outer-name
    created_at = '2016-05-18T17:38:03-07:00',
    value = json.dumps({
        'tos':{
            'type': 'terms_of_service',
            'id': test_terms_of_service.object_id,
        },
        'is_accepted': True,
        'user':{
            'type': 'user',
            'id': 'fake-user-100',
        },
    })
    mock_box_session.post.return_value.json.return_value = {
        'type': 'terms_of_service_user_status',
        'id': test_terms_of_service_user_status.object_id,
        'created_at': created_at,
    }
    new_terms_of_service_user_status = test_terms_of_service.create_user_status(True, mock_user)
    assert len(mock_box_session.post.call_args_list) == 1
    assert mock_box_session.post.call_args[0] == ("{0}/terms_of_service_user_statuses".format(API.BASE_API_URL),)
    assert mock_box_session.post.call_args[1] == {'data': value}
    assert isinstance(new_terms_of_service_user_status, TermsOfServiceUserStatus)


def test_get_user_status(test_terms_of_service, test_terms_of_service_user_status, mock_box_session):
    created_at = '2016-05-18T17:38:03-07:00'
    mock_box_session.post.return_value.json.return_value = {
        'type': 'terms_of_service_user_status',
        'id': test_terms_of_service_user_status.object_id,
        'created_at': created_at,
    }
    new_terms_of_service_user_status = test_terms_of_service.get_user_status('42')
    assert len(mock_box_session.get.call_args_list) == 1
    assert mock_box_session.get.call_args[0] == ("{0}/terms_of_service_user_statuses".format(API.BASE_API_URL),)
    assert isinstance(new_terms_of_service_user_status, TermsOfServiceUserStatus)
