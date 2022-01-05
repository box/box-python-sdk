# coding: utf-8

import pytest

from boxsdk.config import API
from boxsdk.object.sign_request import SignRequest


@pytest.fixture(scope='module')
def mock_sign_request_response():
    # pylint:disable=redefined-outer-name
    mock_sign_request = {
        'id': '42',
        'type': 'sign-request',
        'are_reminders_enabled': 'true',
        'are_text_signatures_enabled': 'true',
        'auto_expire_at': '2021-04-26T08:12:13.982Z',
        'days_valid': '2',
        'email_message': 'Hello! Please sign the document below',
        'email_subject': 'Sign Request from Acme',
        'external_id': '123',
        'is_document_preparation_needed': 'true',
        'parent_folder': {
            'id': '12345',
            'type': 'folder',
            'etag': '1',
            'name': 'Contracts',
            'sequence_id': '3'
        },
        'prefill_tags': [
            {
                'document_tag_id': '1234',
                'text_value': 'text',
                'checkbox_value': 'true',
                'date_value': '2021-04-26T08:12:13.982Z'
            }
        ],
        'prepare_url': 'https://prepareurl.com',
        'sign_files': {
            'files': [
                {
                    'id': '12345',
                    'etag': '1',
                    'type': 'file',
                    'sequence_id': '3',
                    'name': 'Contract.pdf',
                    'sha1': '85136C79CBF9FE36BB9D05D0639C70C265C18D37',
                    'file_version': {
                        'id': '12345',
                        'type': 'file_version',
                        'sha1': '134b65991ed521fcfe4724b7d814ab8ded5185dc'
                    }
                }
            ],
            'is_ready_for_download': 'true'
        },
        'signers': [
            {
                'email': 'example@gmail.com',
                'role': 'signer',
                'is_in_person': 'true',
                'order': '2',
                'embed_url_external_user_id': '1234',
                'has_viewed_document': 'true',
                'signer_decision': {
                    'type': 'signed',
                    'finalized_at': '2021-04-26T08:12:13.982Z'
                },
                'inputs': [
                    {
                        'document_tag_id': '1234',
                        'text_value': 'text',
                        'checkbox_value': 'true',
                        'date_value': '2021-04-26T08:12:13.982Z',
                        'type': 'text',
                        'page_index': '4'
                    }
                ],
                'embed_url': 'https://example.com'
            }
        ],
        'signing_log': {
            'id': '12345',
            'type': 'file',
            'etag': '1',
            'file_version': {
                'id': '12345',
                'type': 'file_version',
                'sha1': '134b65991ed521fcfe4724b7d814ab8ded5185dc'
            },
            'name': 'Contract.pdf',
            'sequence_id': '3',
            'sha1': '85136C79CBF9FE36BB9D05D0639C70C265C18D37'
        },
        'source_files': [
            {
                'id': '12345',
                'etag': '1',
                'type': 'file',
                'sequence_id': '3',
                'name': 'Contract.pdf',
                'sha1': '85136C79CBF9FE36BB9D05D0639C70C265C18D37',
                'file_version': {
                    'id': '12345',
                    'type': 'file_version',
                    'sha1': '134b65991ed521fcfe4724b7d814ab8ded5185dc'
                }
            }
        ],
        'status': 'cancelled'
    }
    return mock_sign_request


def test_get_sign_request(test_sign_request, mock_box_session, mock_sign_request_response):
    expected_url = f'{API.BASE_API_URL}/sign_requests/{test_sign_request.object_id}'
    mock_box_session.get.return_value.json.return_value = mock_sign_request_response

    sign_request = test_sign_request.get()

    mock_box_session.get.assert_called_once_with(
        expected_url, headers=None, params=None)
    assert isinstance(sign_request, SignRequest)
    assert sign_request['id'] == test_sign_request.object_id


def test_cancel_sign_request(test_sign_request, mock_box_session, mock_sign_request_response):
    expected_url = f'{API.BASE_API_URL}/sign_requests/{test_sign_request.object_id}/cancel'
    mock_box_session.post.return_value.json.return_value = mock_sign_request_response

    sign_request = test_sign_request.cancel()

    mock_box_session.post.assert_called_once_with(expected_url)
    assert isinstance(sign_request, SignRequest)
    assert sign_request['id'] == test_sign_request.object_id
    assert sign_request['status'] == mock_sign_request_response['status']


def test_resend_sign_request(test_sign_request, mock_box_session):
    expected_url = f'{API.BASE_API_URL}/sign_requests/{test_sign_request.object_id}/resend'

    test_sign_request.resend()

    mock_box_session.post.assert_called_once_with(
        expected_url, expect_json_response=False, skip_retry_codes=set([202]))
