# coding: utf-8

from __future__ import unicode_literals

from boxsdk.object.terms_of_service_user_status import TermsOfServiceUserStatus
from boxsdk.config import API



def test_get(test_terms_of_service_user_status, mock_box_session):
    created_at = '2016-05-18T17:38:03-07:00',
    expected_url = '{0}/terms_of_service_user_statuses/{1}'.format(API.BASE_API_URL, test_terms_of_service_user_status.object_id)
    mock_box_session.get.return_value.json.return_value = {
        'type': 'terms_of_service_user_status',
        'id': test_terms_of_service_user_status.object_id,
        'created_at': created_at
    }
    terms_of_service = test_terms_of_service_user_status.get()
    mock_box_session.get.assert_called_once_with(expected_url, headers=None, params=None)
    assert isinstance(terms_of_service, TermsOfServiceUserStatus)
    assert terms_of_service.created_at == created_at
